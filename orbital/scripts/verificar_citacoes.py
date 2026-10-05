#!/usr/bin/env python3
"""Confere as citações de uma análise contra as páginas reais dos PDFs.

Para cada citação no formato do extrair_pdf.py,
    [edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 7]   ou   p. 3–4
verifica:
  - o arquivo existe entre os PDFs informados e a página existe;
  - o item (e anexo/cláusula, se citados) existe e está na(s) página(s) citada(s);
  - se a citação vier logo após uma transcrição entre aspas ("..." [cit]),
    o trecho transcrito está de fato na(s) página(s) citada(s).

Uso:
    python verificar_citacoes.py analise.md edital.pdf errata.pdf
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

RE_CITACAO = re.compile(
    r"\[(?P<arq>[^\[\]\n,]+?\.pdf),(?P<meio>[^\[\]\n]*?)\bp\.\s*(?P<p1>\d+)(?:\s*[–-]\s*(?P<p2>\d+))?[^\[\]\n]*\]"
)
# Qualquer [..., p. N] — usado para achar citações fora do padrão verificável.
RE_QUALQUER_CITACAO = re.compile(r"\[[^\[\]\n]*\bp\.\s*(?:\d+|n/d)[^\[\]\n]*\]")
RE_ASPAS_ANTES = re.compile(r"[\"“](?P<q>[^\"”\n]{6,500})[\"”]\s*`?\s*$")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).casefold()
    s = s.replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def _anexo(secao: str | None) -> str | None:
    m = re.match(r"anexo\s+([ivxl]+|\d+)", secao or "", re.IGNORECASE)
    return m.group(1).upper() if m else None


def _partes(meio: str) -> dict:
    d = {"secao": None, "clausula": None, "item": None, "alinea": None}
    for parte in (p.strip() for p in meio.split(",")):
        if m := re.match(r"item\s+(\d+(?:\.\d+)*)", parte):
            d["item"] = m.group(1)
        elif m := re.match(r"al[íi]nea\s+([a-z])\b", parte, re.IGNORECASE):
            d["alinea"] = m.group(1).lower()
        elif m := re.match(r"cl[áa]usula\s+(\w+)", parte, re.IGNORECASE):
            d["clausula"] = m.group(1)
        elif parte.lower().startswith("anexo"):
            d["secao"] = parte
    return d


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


def verificar(texto: str, docs: dict) -> list[dict]:
    resultados = []
    for m in RE_QUALQUER_CITACAO.finditer(texto):
        if not RE_CITACAO.fullmatch(m.group(0)):
            resultados.append({
                "citacao": m.group(0), "nivel": "ERRO", "linha": texto.count("\n", 0, m.start()) + 1,
                "msg": ["formato não verificável: use a citação do extrair_pdf.py "
                        "([arquivo.pdf, ..., item X, p. N])"],
            })
    for m in RE_CITACAO.finditer(texto):
        cit = m.group(0)
        candidatos = []
        arq = m["arq"].strip()
        p1 = int(m["p1"])
        p2 = int(m["p2"] or p1)
        citadas = list(range(p1, p2 + 1))
        partes = _partes(m["meio"])
        antes = RE_ASPAS_ANTES.search(texto[max(0, m.start() - 520):m.start()])
        citado = antes["q"] if antes else None
        r = {"citacao": cit, "nivel": "OK", "msg": [], "linha": texto.count("\n", 0, m.start()) + 1}

        def falha(nivel, msg):
            r["msg"].append(msg)
            if nivel == "ERRO" or r["nivel"] == "OK":
                r["nivel"] = nivel

        d = docs.get(arq)
        if not d:
            falha("ERRO", f"arquivo '{arq}' não está entre os PDFs informados")
            resultados.append(r)
            continue
        if p2 > d["doc"].paginas or p1 < 1:
            falha("ERRO", f"página fora do documento ({d['doc'].paginas} p.)")
            resultados.append(r)
            continue

        if partes["item"]:
            candidatos = [
                t for t in d["trechos"] if t.item == partes["item"]
                and _anexo(t.secao) == _anexo(partes["secao"])
                and (partes["clausula"] is None or t.clausula == partes["clausula"])
                and (partes["alinea"] is None or t.alinea == partes["alinea"])
            ]
            if not candidatos:
                onde = partes["secao"] or "corpo do documento"
                alvo = f"item {partes['item']}" + (f", alínea {partes['alinea']}" if partes["alinea"] else "")
                falha("ERRO", f"{alvo} não encontrado em {onde}")
            else:
                paginas_item = sorted({t.pagina for t in candidatos})
                # Conferência independente do extrator: o número do item tem de estar
                # no texto bruto da página onde o item começa.
                inicio = min(paginas_item)
                marca = re.compile(rf"(^|\n)\s*{re.escape(partes['item'])}[.)\s]")
                if not partes["alinea"] and not marca.search(d["paginas"][inicio]):
                    falha("ERRO", f"número {partes['item']} não aparece no texto da p. {inicio}")
                if not set(citadas) & set(paginas_item):
                    falha("ERRO", f"item {partes['item']} está na(s) p. {paginas_item}, não na p. {p1}"
                                  + (f"–{p2}" if p2 != p1 else ""))
                elif set(paginas_item) - set(citadas):
                    falha("AVISO", f"item {partes['item']} ocupa as p. {paginas_item}; citação cobre só {citadas}")

        if citado:
            ocr = any(p in d["doc"].paginas_ocr for p in citadas)
            achou = _contem("\n".join(d["paginas"][p] for p in citadas), citado, ocr)
            if achou and partes["item"] and candidatos:
                no_item = _contem("\n".join(t.texto for t in candidatos), citado, ocr)
                if not no_item:
                    falha("ERRO", f"transcrição está na página, mas fora do item {partes['item']}")
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
    args = ap.parse_args(argv)

    docs = carregar(args.pdfs)
    resultados = verificar(args.analise.read_text(encoding="utf-8"), docs)
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
