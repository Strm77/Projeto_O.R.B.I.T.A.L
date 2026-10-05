#!/usr/bin/env python3
"""Confere as citações de uma análise contra as páginas reais dos PDFs.

Aceita a citação do extrair_pdf.py,
    [edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 7]   ou   p. 3–4
e a forma curta com apelidos declarados (--alias ou legenda no texto),
    [TR, 4.8.1–4.8.3, p. 7–8]  [Edital, 6.5, 6.8, 6.11, p. 9–10]  [ETP, seções 8–10, p. 8–13]
    [Minuta, cl. 4.1, p. 24]   [Edital, capa, p. 1]
Para cada citação verifica:
  - o arquivo existe entre os PDFs informados e a página existe;
  - o item (e anexo/cláusula, se citados) existe e está na(s) página(s) citada(s);
  - se a citação vier logo após uma transcrição entre aspas ("..." [cit]),
    o trecho transcrito está de fato na(s) página(s) citada(s).

Uso:
    python verificar_citacoes.py analise.md edital.pdf errata.pdf
    python verificar_citacoes.py qa.md edital.pdf tr.pdf etp.pdf \
        --alias Edital=edital.pdf --alias TR=tr.pdf --alias ETP=etp.pdf \
        --alias "Minuta=edital.pdf:Anexo II"
Apelidos também podem vir no próprio texto, numa linha:
    <!-- orbital:alias Edital=edital.pdf; TR=tr.pdf; Minuta=edital.pdf:Anexo II -->
Saída: relatório no stdout; código 1 se houver ERRO.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import extrair_pdf  # noqa: E402

# [DOC, <meio>, p. 5] · p. 3–4 · p. 5 e 12
RE_CITACAO = re.compile(
    r"\[(?P<doc>[^\[\]\n,]+?),(?P<meio>[^\[\]\n]*?)\bp\.\s*"
    r"(?P<pags>\d+(?:\s*(?:[–-]|\be\b|,)\s*\d+)*)\s*\]"
)
# Qualquer [..., p. N] — usado para achar citações fora do padrão verificável.
RE_QUALQUER_CITACAO = re.compile(r"\[[^\[\]\n]*\bp\.\s*(?:\d+|n/d)[^\[\]\n]*\]")
RE_LEGENDA = re.compile(r"<!--\s*orbital:alias\s+(?P<pares>.+?)\s*-->")
NUM = r"\d+(?:\.\d+)*"
RE_ASPAS_ANTES = re.compile(r"[\"“](?P<q>[^\"”\n]{6,500})[\"”]\s*`?\s*$")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).casefold()
    s = s.replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def _anexo(secao: str | None) -> str | None:
    m = re.match(r"anexo\s+([ivxl]+|\d+)", secao or "", re.IGNORECASE)
    return m.group(1).upper() if m else None


def _paginas(texto: str) -> list[int]:
    paginas: set[int] = set()
    for parte in re.split(r"\s*(?:,|\be\b)\s*", texto.strip()):
        if m := re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", parte):
            paginas.update(range(int(m[1]), int(m[2]) + 1))
        elif parte.isdigit():
            paginas.add(int(parte))
    return sorted(paginas)


def _itens(texto: str) -> list[str]:
    """'1.1–1.2' → [1.1, 1.2]; '4.33 e 4.35' → [4.33, 4.35]; extremos de intervalo."""
    return re.findall(NUM, texto)


def _partes(meio: str) -> dict:
    d = {"secao": None, "clausula": None, "itens": [], "alinea": None}
    for parte in (p.strip() for p in re.split(r"[,·]", meio)):
        if not parte:
            continue
        if m := re.match(rf"item\s+({NUM}(?:\s*(?:[–-]|e)\s*{NUM})*)$", parte):
            if d["itens"]:
                continue  # "9.1, item 5": linha/subitem de uma tabela do item 9.1
            d["itens"] += _itens(m[1])
        elif m := re.match(r"al[íi]nea\s+([a-z])\b", parte, re.IGNORECASE):
            d["alinea"] = m[1].lower()
        elif m := re.match(rf"cl\.\s*({NUM})", parte, re.IGNORECASE):
            d["itens"].append(m[1])  # "cl. 4.1" na minuta = item 4.1
        elif m := re.match(r"cl[áa]usula\s+(\w+)", parte, re.IGNORECASE):
            d["clausula"] = m[1]
        elif m := re.match(r"se[çc][ãaõo]e?s?\s+(.+)", parte, re.IGNORECASE):
            d["itens"] += _itens(m[1])
        elif parte.lower().startswith("anexo"):
            d["secao"] = parte
        elif re.fullmatch(rf"{NUM}(?:\s*(?:[–-]|e)\s*{NUM})*", parte):
            d["itens"] += _itens(parte)
        # demais termos (capa, preâmbulo, títulos) só conferem a página
    return d


def ler_apelidos(pares: list[str], texto: str = "") -> dict[str, tuple[str, str | None]]:
    """'TR=tr.pdf' ou 'Minuta=edital.pdf:Anexo II' → {apelido: (arquivo, seção)}."""
    for m in RE_LEGENDA.finditer(texto):
        pares = [*re.split(r"\s*;\s*", m["pares"]), *pares]
    apelidos = {}
    for par in pares:
        if "=" not in par:
            continue
        nome, alvo = (x.strip() for x in par.split("=", 1))
        arquivo, _, secao = alvo.partition(":")
        apelidos[nome] = (arquivo.strip(), secao.strip() or None)
    return apelidos


def _contem(texto_paginas: str, citado: str, ocr: bool) -> str | None:
    """'exato', 'aprox' (só OCR, ≥ 85% parecido) ou None."""
    alvo, base = _norm(citado), _norm(texto_paginas)
    if alvo in base:
        return "exato"
    if ocr and len(alvo) <= len(base):
        # Tolera erro de OCR nas letras, nunca nos números: datas, valores e
        # percentuais da transcrição têm de aparecer idênticos no trecho.
        numeros = re.findall(r"\d+", alvo)
        passo = max(1, len(alvo) // 8)
        for i in range(0, len(base) - len(alvo) + 1, passo):
            janela = base[max(0, i - passo):i + len(alvo) + passo]
            if (all(n in re.findall(r"\d+", janela) for n in numeros)
                    and SequenceMatcher(None, alvo, base[i:i + len(alvo)]).ratio() >= 0.85):
                return "aprox"
    return None


def carregar(pdfs: list[Path]):
    docs = {}
    for caminho in pdfs:
        doc, trechos = extrair_pdf.extrair(caminho)
        pdf = extrair_pdf.fitz.open(caminho)
        paginas = {}
        for n in range(1, doc.paginas + 1):
            if n in doc.paginas_ocr:
                paginas[n] = "\n".join(t.texto for t in trechos if t.pagina == n)
            else:
                paginas[n] = pdf[n - 1].get_text("text")
        docs[caminho.name] = {"doc": doc, "paginas": paginas, "trechos": trechos}
    return docs


def verificar(texto: str, docs: dict, apelidos: dict | None = None) -> list[dict]:
    apelidos = ler_apelidos([], texto) | (apelidos or {})
    resultados = []
    validas = {m.start() for m in RE_CITACAO.finditer(texto)}
    for m in RE_QUALQUER_CITACAO.finditer(texto):
        if m.start() not in validas:
            resultados.append({
                "citacao": m.group(0), "nivel": "ERRO", "linha": texto.count("\n", 0, m.start()) + 1,
                "msg": ["formato não verificável: use [arquivo.pdf, ..., item X, p. N] "
                        "ou um apelido declarado na legenda"],
            })
    for m in RE_CITACAO.finditer(texto):
        cit = m.group(0)
        r = {"citacao": cit, "nivel": "OK", "msg": [], "linha": texto.count("\n", 0, m.start()) + 1}

        def falha(nivel, msg):
            r["msg"].append(msg)
            if nivel == "ERRO" or r["nivel"] == "OK":
                r["nivel"] = nivel

        nome = m["doc"].strip()
        secao_padrao = None
        if nome.lower().endswith(".pdf"):
            arq = nome
        elif nome in apelidos:
            arq, secao_padrao = apelidos[nome]
        else:
            falha("ERRO", f"'{nome}' não é arquivo nem apelido declarado (use --alias {nome}=arquivo.pdf)")
            resultados.append(r)
            continue
        d = docs.get(arq)
        if not d:
            falha("ERRO", f"arquivo '{arq}' não está entre os PDFs informados")
            resultados.append(r)
            continue
        citadas = _paginas(m["pags"])
        if not citadas or max(citadas) > d["doc"].paginas or min(citadas) < 1:
            falha("ERRO", f"página fora do documento ({d['doc'].paginas} p.)")
            resultados.append(r)
            continue

        partes = _partes(m["meio"])
        secao = partes["secao"] or secao_padrao
        antes = RE_ASPAS_ANTES.search(texto[max(0, m.start() - 520):m.start()])
        citado = antes["q"] if antes else None
        candidatos = []
        for item in partes["itens"]:
            achados = [
                t for t in d["trechos"] if t.item == item
                and _anexo(t.secao) == _anexo(secao)
                and (partes["clausula"] is None or t.clausula == partes["clausula"])
                and (partes["alinea"] is None or t.alinea == partes["alinea"])
            ]
            if not achados:
                alvo = f"item {item}" + (f", alínea {partes['alinea']}" if partes["alinea"] else "")
                falha("ERRO", f"{alvo} não encontrado em {secao or 'corpo do documento'}")
                continue
            candidatos += achados
            paginas_item = sorted({t.pagina for t in achados})
            # Conferência independente do extrator: o número do item tem de estar
            # no texto bruto da página onde o item começa.
            inicio = min(paginas_item)
            marca = re.compile(rf"(^|\n)\s*{re.escape(item)}[.)\s]")
            if not partes["alinea"] and not marca.search(d["paginas"][inicio]):
                falha("ERRO", f"número {item} não aparece no texto da p. {inicio}")
            if not set(citadas) & set(paginas_item):
                falha("ERRO", f"item {item} está na(s) p. {paginas_item}, não na(s) p. {citadas}")

        if citado:
            ocr = any(p in d["doc"].paginas_ocr for p in citadas)
            achou = _contem("\n".join(d["paginas"][p] for p in citadas), citado, ocr)
            if achou and candidatos:
                if not _contem("\n".join(t.texto for t in candidatos), citado, ocr):
                    falha("ERRO", f"transcrição está na página, mas fora do(s) item(ns) {', '.join(partes['itens'])}")
            if achou == "aprox":
                falha("AVISO", "transcrição confere só por aproximação (página lida por OCR)")
            elif not achou:
                outras = [p for p, t in d["paginas"].items()
                          if p not in citadas and _contem(t, citado, p in d["doc"].paginas_ocr)]
                falha("ERRO", "transcrição não está na(s) página(s) citada(s)"
                              + (f"; aparece na p. {outras}" if outras else "; não encontrada no documento"))
        resultados.append(r)
    return resultados


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("analise", type=Path, help="texto da análise (Markdown)")
    ap.add_argument("pdfs", nargs="+", type=Path)
    ap.add_argument("--alias", action="append", default=[], metavar="APELIDO=arquivo.pdf[:Anexo X]",
                    help="abreviação usada nas citações (repetível)")
    args = ap.parse_args(argv)

    docs = carregar(args.pdfs)
    texto = args.analise.read_text(encoding="utf-8")
    resultados = verificar(texto, docs, ler_apelidos(args.alias))
    unicas = {}
    for r in resultados:
        unicas.setdefault((r["citacao"], r["nivel"], tuple(r["msg"])), r)
    contagem = {n: sum(r["nivel"] == n for r in resultados) for n in ("OK", "AVISO", "ERRO")}
    print(f"{len(resultados)} citações: {contagem['OK']} OK, {contagem['AVISO']} aviso(s), "
          f"{contagem['ERRO']} erro(s)")
    for r in unicas.values():
        if r["nivel"] != "OK":
            print(f"{r['nivel']:5} linha {r['linha']}: {r['citacao']}\n      " + "; ".join(r["msg"]))
    return 1 if contagem["ERRO"] else 0


if __name__ == "__main__":
    sys.exit(main())
