#!/usr/bin/env python3
"""Consulta ao PNCP (Portal Nacional de Contratações Públicas) — API pública, sem chave.

Busca contratações com proposta aberta ou publicadas num período, filtra por palavras do
objeto e baixa os arquivos (edital, TR, anexos) de uma contratação para o extrair_pdf.py.

    python pncp.py abertas --ate 2026-10-31 --modalidade pregao --palavra dados --palavra "business intelligence"
    python pncp.py publicadas --de 2026-10-01 --ate 2026-10-05 --uf DF
    python pncp.py detalhe 00394460000141-1-000123/2026
    python pncp.py arquivos 00394460000141-1-000123/2026 -o editais/

Documentação oficial: https://pncp.gov.br/api/consulta/swagger-ui/index.html
Caminhos conferidos no Swagger (05/10/2026): /v1/contratacoes/proposta, /v1/contratacoes/publicacao
e /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}. A lista de arquivos vem da API de integração
(/api/pncp/v1/.../arquivos). Nomes de parâmetros e campos seguem o Manual de Integração;
confira em /pncp-consulta/v3/api-docs se algum mudar (BASE_*, MODALIDADES).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

BASE_CONSULTA = "https://pncp.gov.br/api/consulta/v1"
BASE_PNCP = "https://pncp.gov.br/api/pncp/v1"
TAMANHO_PAGINA = 50

# Códigos de modalidade da Lei 14.133 no PNCP (tabela de domínio do Manual de Integração).
MODALIDADES = {
    "leilao-eletronico": 1, "dialogo-competitivo": 2, "concurso": 3,
    "concorrencia-eletronica": 4, "concorrencia-presencial": 5,
    "pregao": 6, "pregao-presencial": 7, "dispensa": 8, "inexigibilidade": 9,
    "manifestacao-interesse": 10, "pre-qualificacao": 11, "credenciamento": 12,
    "leilao-presencial": 13,
}

RE_CONTROLE = re.compile(r"^(?P<cnpj>\d{14})-\d-(?P<seq>\d+)/(?P<ano>\d{4})$")


class ErroPNCP(Exception):
    pass


def _get(url: str, params: dict | None = None, tentativas: int = 3) -> bytes | None:
    """GET com nova tentativa em erro 5xx/429. Devolve None em 204 (sem conteúdo)."""
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    for n in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json, */*",
                                                       "User-Agent": "orbital-pncp/0.1"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return None if r.status == 204 else r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and n < tentativas - 1:
                time.sleep(2 ** (n + 1))
                continue
            raise ErroPNCP(f"HTTP {e.code} em {url}") from e
        except urllib.error.URLError as e:
            if n < tentativas - 1:
                time.sleep(2 ** (n + 1))
                continue
            raise ErroPNCP(f"sem acesso a {url}: {e.reason}") from e
    return None


def _paginar(caminho: str, params: dict, max_paginas: int) -> list[dict]:
    registros, pagina = [], 1
    while pagina <= max_paginas:
        corpo = _get(f"{BASE_CONSULTA}/{caminho}", {**params, "pagina": pagina, "tamanhoPagina": TAMANHO_PAGINA})
        if not corpo:
            break
        dados = json.loads(corpo)
        registros += dados.get("data") or []
        if not dados.get("paginasRestantes"):
            break
        pagina += 1
    return registros


def _data(s: str) -> str:
    """'2026-10-05' ou '05/10/2026' → '20261005' (formato da API)."""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y%m%d")
        except ValueError:
            pass
    raise ErroPNCP(f"data inválida: {s}")


def _sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def filtrar(registros: list[dict], palavras: list[str]) -> list[dict]:
    """Mantém registros cujo objeto ou informação complementar contém alguma palavra (sem acento)."""
    if not palavras:
        return registros
    alvos = [_sem_acento(p) for p in palavras]
    saida = []
    for r in registros:
        texto = _sem_acento(f"{r.get('objetoCompra') or ''} {r.get('informacaoComplementar') or ''}")
        achadas = [p for p, a in zip(palavras, alvos) if a in texto]
        if achadas:
            saida.append({**r, "_palavras": achadas})
    return saida


def resumir(r: dict) -> dict:
    orgao, unidade = r.get("orgaoEntidade") or {}, r.get("unidadeOrgao") or {}
    cnpj, ano, seq = orgao.get("cnpj"), r.get("anoCompra"), r.get("sequencialCompra")
    return {
        "controle": r.get("numeroControlePNCP"),
        "orgao": orgao.get("razaoSocial"),
        "uf": unidade.get("ufSigla"),
        "municipio": unidade.get("municipioNome"),
        "modalidade": r.get("modalidadeNome"),
        "numero": r.get("numeroCompra"),
        "objeto": " ".join((r.get("objetoCompra") or "").split()),
        "valor_estimado": r.get("valorTotalEstimado"),
        "abertura_propostas": r.get("dataAberturaProposta"),
        "encerramento_propostas": r.get("dataEncerramentoProposta"),
        "situacao": r.get("situacaoCompraNome"),
        "srp": r.get("srp"),
        "link_sistema_origem": r.get("linkSistemaOrigem"),
        "link_pncp": f"https://pncp.gov.br/app/editais/{cnpj}/{ano}/{seq}" if cnpj and ano and seq else None,
        "palavras": r.get("_palavras", []),
    }


def abertas(ate: str, modalidade: int | None, uf: str | None, max_paginas: int) -> list[dict]:
    """Contratações com recebimento de propostas aberto até a data."""
    return _paginar("contratacoes/proposta", {"dataFinal": _data(ate), "codigoModalidadeContratacao": modalidade,
                                              "uf": uf}, max_paginas)


def publicadas(de: str, ate: str, modalidade: int, uf: str | None, max_paginas: int) -> list[dict]:
    """Contratações publicadas no período (a API exige a modalidade)."""
    return _paginar("contratacoes/publicacao", {"dataInicial": _data(de), "dataFinal": _data(ate),
                                                "codigoModalidadeContratacao": modalidade, "uf": uf}, max_paginas)


def _partes_controle(controle: str) -> tuple[str, str, str]:
    m = RE_CONTROLE.match(controle.strip())
    if not m:
        raise ErroPNCP(f"número de controle inválido: {controle} (ex.: 00394460000141-1-000123/2026)")
    return m["cnpj"], m["ano"], str(int(m["seq"]))


def detalhe(controle: str) -> dict:
    """Dados de uma contratação (GET /v1/orgaos/{cnpj}/compras/{ano}/{sequencial})."""
    cnpj, ano, seq = _partes_controle(controle)
    return json.loads(_get(f"{BASE_CONSULTA}/orgaos/{cnpj}/compras/{ano}/{seq}") or b"{}")


def baixar_arquivos(controle: str, destino: Path) -> list[Path]:
    """Baixa os documentos de uma contratação (edital, TR, anexos, erratas)."""
    cnpj, ano, seq = _partes_controle(controle)
    base = f"{BASE_PNCP}/orgaos/{cnpj}/compras/{ano}/{seq}/arquivos"
    lista = json.loads(_get(base) or b"[]")
    destino.mkdir(parents=True, exist_ok=True)
    salvos = []
    for arq in lista:
        if arq.get("statusAtivo") is False:
            continue
        n = arq.get("sequencialDocumento")
        nome = re.sub(r"[^\w.\-]+", "_", arq.get("titulo") or f"documento_{n}").strip("_")
        url = arq.get("url") or f"{base}/{n}"
        conteudo = _get(url) or b""
        sufixo = ".pdf" if conteudo[:4] == b"%PDF" else (".zip" if conteudo[:2] == b"PK" else "")
        caminho = destino / f"{n:02d}_{nome}" if isinstance(n, int) else destino / nome
        if sufixo and not caminho.name.lower().endswith(sufixo):
            caminho = caminho.with_name(caminho.name + sufixo)
        caminho.write_bytes(conteudo)
        salvos.append(caminho)
    (destino / "pncp_arquivos.json").write_text(json.dumps(lista, ensure_ascii=False, indent=2), encoding="utf-8")
    return salvos


def para_markdown(itens: list[dict], titulo: str) -> str:
    linhas = [f"# {titulo}", "", f"_PNCP, consultado em {date.today():%d/%m/%Y} · {len(itens)} contratação(ões)_", "",
              "| Encerra propostas | Órgão (UF) | Modalidade | Objeto | Valor estimado | Palavras | Link |",
              "|---|---|---|---|---|---|---|"]
    for i in sorted(itens, key=lambda x: x.get("encerramento_propostas") or ""):
        valor = i["valor_estimado"]
        valor = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(valor, (int, float)) else "sigiloso/n.i."
        objeto = i["objeto"][:180] + ("…" if len(i["objeto"]) > 180 else "")
        linhas.append(f"| {(i['encerramento_propostas'] or '')[:16].replace('T', ' ')} | {i['orgao']} ({i['uf']}) | "
                      f"{i['modalidade']} | {objeto.replace('|', '/')} | {valor} | {', '.join(i['palavras'])} | "
                      f"[PNCP]({i['link_pncp']}) · `{i['controle']}` |")
    return "\n".join(linhas) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome in ("abertas", "publicadas"):
        p = sub.add_parser(nome)
        if nome == "publicadas":
            p.add_argument("--de", required=True)
        p.add_argument("--ate", default=date.today().isoformat() if nome == "publicadas" else None,
                       required=nome == "abertas")
        p.add_argument("--modalidade", choices=MODALIDADES, default=None if nome == "abertas" else "pregao")
        p.add_argument("--uf")
        p.add_argument("--palavra", action="append", default=[], help="filtra o objeto (repita para várias)")
        p.add_argument("--max-paginas", type=int, default=20)
        p.add_argument("-f", "--formato", choices=["md", "json"], default="md")
        p.add_argument("-o", "--saida", type=Path)
    p = sub.add_parser("detalhe")
    p.add_argument("controle")
    p = sub.add_parser("arquivos")
    p.add_argument("controle", help="número de controle PNCP, ex.: 00394460000141-1-000123/2026")
    p.add_argument("-o", "--saida", type=Path, default=Path("."))
    a = ap.parse_args(argv)

    try:
        if a.cmd == "detalhe":
            print(json.dumps(detalhe(a.controle), ensure_ascii=False, indent=2))
            return 0
        if a.cmd == "arquivos":
            for c in baixar_arquivos(a.controle, a.saida):
                print(c)
            return 0
        mod = MODALIDADES.get(a.modalidade) if a.modalidade else None
        regs = (abertas(a.ate, mod, a.uf, a.max_paginas) if a.cmd == "abertas"
                else publicadas(a.de, a.ate, mod, a.uf, a.max_paginas))
        itens = [resumir(r) for r in filtrar(regs, a.palavra)]
    except ErroPNCP as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2

    titulo = "Contratações com proposta aberta" if a.cmd == "abertas" else "Contratações publicadas"
    texto = json.dumps(itens, ensure_ascii=False, indent=2) if a.formato == "json" else para_markdown(itens, titulo)
    if a.saida:
        a.saida.write_text(texto, encoding="utf-8")
        print(f"{len(itens)} de {len(regs)} contratação(ões) → {a.saida}", file=sys.stderr)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
