#!/usr/bin/env python3
"""Consulta ao PNCP (Portal Nacional de Contratações Públicas) — API pública, sem chave.

Busca contratações com proposta aberta ou publicadas num período, filtra por palavras do
objeto e baixa os arquivos (edital, TR, anexos) de uma contratação para o extrair_pdf.py.

    python pncp.py abertas --ate 2026-10-31 --modalidade pregao --palavra dados --palavra "business intelligence"
    python pncp.py publicadas --de 2026-10-01 --ate 2026-10-05 --uf DF
    python pncp.py contratos --de 2026-01-01 --ate 2026-10-05 --palavra "business intelligence"
    python pncp.py atas --de 2026-10-01 --ate 2027-10-01 --palavra observabilidade
    python pncp.py pca --de 2026-09-01 --ate 2026-10-05 --palavra "plataforma de dados"
    python pncp.py detalhe 00394460000141-1-000123/2026
    python pncp.py arquivos 00394460000141-1-000123/2026 -o editais/

Documentação oficial: https://pncp.gov.br/api/consulta/swagger-ui/index.html
Caminhos, parâmetros e campos conferidos no Swagger em 05/10/2026: contratacoes/proposta,
contratacoes/publicacao, orgaos/{cnpj}/compras/{ano}/{sequencial}, contratos, atas, pca/ e
pca/atualizacao (este usa dataInicio/dataFim, não dataInicial/dataFinal). Datas: yyyyMMdd.
A lista de arquivos vem da API de integração (/api/pncp/v1/.../arquivos), fora do Swagger de
consulta. Se algo mudar, confira em /pncp-consulta/v3/api-docs (BASE_*, MODALIDADES).
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
import zipfile
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

# Termos de dados, IA e observabilidade (portfólio dos parceiros). Palavra inteira, sem acento.
TERMOS_DADOS_IA = [
    "business intelligence", "power bi", "data warehouse", "data lake", "lakehouse", "big data",
    "ciencia de dados", "analise de dados", "analytics", "engenharia de dados", "governanca de dados",
    "qualidade de dados", "catalogo de dados", "integracao de dados", "plataforma de dados",
    "inteligencia artificial", "ia generativa", "machine learning", "aprendizado de maquina", "llm",
    "chatbot", "assistente virtual", "observabilidade", "monitoramento de aplicacoes", "apm", "aiops",
    "snowflake", "microsoft fabric", "azure", "dynatrace", "datadog", "ibm", "watsonx", "cognos", "spss",
    "db2", "guardium", "instana", "sql server", "databricks", "qlik", "tableau", "etl",
]

RE_CONTROLE = re.compile(r"^(?P<cnpj>\d{14})-\d-(?P<seq>\d+)/(?P<ano>\d{4})$")


class ErroPNCP(Exception):
    pass


PAUSA_ENTRE_PAGINAS = 1.0  # segundos; a API devolve 429 com ~30 requisições seguidas


def _get(url: str, params: dict | None = None, tentativas: int = 6) -> bytes | None:
    """GET com nova tentativa em erro 5xx/429 (respeita Retry-After). Devolve None em 204."""
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
                espera = e.headers.get("Retry-After") if e.headers else None
                time.sleep(int(espera) if espera and espera.isdigit() else min(60, 5 * 2 ** n))
                continue
            raise ErroPNCP(f"HTTP {e.code} em {url}") from e
        except urllib.error.URLError as e:
            if n < tentativas - 1:
                time.sleep(2 ** (n + 1))
                continue
            raise ErroPNCP(f"sem acesso a {url}: {e.reason}") from e
    return None


def _paginar(caminho: str, params: dict, max_paginas: int) -> list[dict]:
    registros, pagina, total = [], 1, None
    while pagina <= max_paginas:
        if pagina > 1:
            time.sleep(PAUSA_ENTRE_PAGINAS)
        try:
            corpo = _get(f"{BASE_CONSULTA}/{caminho}", {**params, "pagina": pagina, "tamanhoPagina": TAMANHO_PAGINA})
        except ErroPNCP as e:
            if not registros:
                raise
            print(f"\naviso: parou na página {pagina} de {total} ({e}); resultado PARCIAL", file=sys.stderr)
            return registros
        if not corpo:
            break
        dados = json.loads(corpo)
        registros += dados.get("data") or []
        total = dados.get("totalPaginas")
        if sys.stderr.isatty():
            print(f"\r  página {pagina}/{total or '?'}", end="", file=sys.stderr)
        if not dados.get("paginasRestantes"):
            break
        pagina += 1
    else:
        print(f"\naviso: leu {max_paginas} de {total} páginas; resultado INCOMPLETO "
              f"(aumente --max-paginas ou filtre por --uf/--modalidade)", file=sys.stderr)
    if sys.stderr.isatty():
        print(file=sys.stderr)
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


def filtrar(registros: list[dict], palavras: list[str],
            campos: tuple[str, ...] = ("objetoCompra", "informacaoComplementar")) -> list[dict]:
    """Mantém registros em que algum dos campos contém alguma palavra inteira (sem acento nem caixa)."""
    if not palavras:
        return registros
    alvos = [re.compile(rf"\b{re.escape(_sem_acento(p))}\b") for p in palavras]
    saida = []
    for r in registros:
        texto = _sem_acento(" ".join(str(r.get(c) or "") for c in campos))
        achadas = [p for p, a in zip(palavras, alvos) if a.search(texto)]
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
        "modo_disputa": r.get("modoDisputaNome"),
        "amparo_legal": (r.get("amparoLegal") or {}).get("nome"),
        "esfera": orgao.get("esferaId"),
        "numero": r.get("numeroCompra"),
        "objeto": " ".join((r.get("objetoCompra") or "").split()),
        "valor_estimado": r.get("valorTotalEstimado"),
        "abertura_propostas": r.get("dataAberturaProposta"),
        "encerramento_propostas": r.get("dataEncerramentoProposta"),
        "situacao": r.get("situacaoCompraNome"),
        "srp": r.get("srp"),
        "link_sistema_origem": r.get("linkSistemaOrigem"),
        "link_processo": r.get("linkProcessoEletronico"),
        "publicado_em": r.get("dataPublicacaoPncp"),
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


def contratos(de: str, ate: str, cnpj_orgao: str | None, max_paginas: int) -> list[dict]:
    """Contratos/empenhos publicados no período (GET /v1/contratos)."""
    return _paginar("contratos", {"dataInicial": _data(de), "dataFinal": _data(ate), "cnpjOrgao": cnpj_orgao},
                    max_paginas)


def atas(de: str, ate: str, cnpj: str | None, max_paginas: int) -> list[dict]:
    """Atas de registro de preços com vigência no período (GET /v1/atas)."""
    return _paginar("atas", {"dataInicial": _data(de), "dataFinal": _data(ate), "cnpj": cnpj}, max_paginas)


def pca(ano: int | None, classe: str | None, de: str | None, ate: str | None, cnpj: str | None,
        max_paginas: int) -> list[dict]:
    """Itens dos Planos de Contratações Anuais, um registro por item (com dados do plano).

    Com ano + classe: GET /v1/pca/ (anoPca, codigoClassificacaoSuperior).
    Senão: GET /v1/pca/atualizacao (dataInicio, dataFim, cnpj) — planos atualizados no período.
    """
    if ano and classe:
        planos = _paginar("pca/", {"anoPca": ano, "codigoClassificacaoSuperior": classe}, max_paginas)
    elif de and ate:
        planos = _paginar("pca/atualizacao", {"dataInicio": _data(de), "dataFim": _data(ate), "cnpj": cnpj},
                          max_paginas)
    else:
        raise ErroPNCP("pca: informe --ano e --classe, ou --de e --ate")
    itens = []
    for plano in planos:
        cabecalho = {k: v for k, v in plano.items() if k != "itens"}
        if ano and plano.get("anoPca") not in (None, ano):
            continue
        itens += [{**cabecalho, **item} for item in plano.get("itens") or []]
    return itens


def resumir_contrato(r: dict) -> dict:
    orgao, unidade = r.get("orgaoEntidade") or {}, r.get("unidadeOrgao") or {}
    return {
        "controle": r.get("numeroControlePNCP"), "controle_compra": r.get("numeroControlePncpCompra"),
        "orgao": orgao.get("razaoSocial"), "uf": unidade.get("ufSigla"),
        "fornecedor": r.get("nomeRazaoSocialFornecedor"), "ni_fornecedor": r.get("niFornecedor"),
        "objeto": " ".join((r.get("objetoContrato") or "").split()),
        "valor_global": r.get("valorGlobal"), "vigencia_inicio": r.get("dataVigenciaInicio"),
        "vigencia_fim": r.get("dataVigenciaFim"), "tipo": (r.get("tipoContrato") or {}).get("nome"),
        "palavras": r.get("_palavras", []),
    }


def resumir_ata(r: dict) -> dict:
    return {
        "controle": r.get("numeroControlePNCPAta"), "controle_compra": r.get("numeroControlePNCPCompra"),
        "orgao": r.get("nomeOrgao"), "objeto": " ".join((r.get("objetoContratacao") or "").split()),
        "vigencia_inicio": r.get("vigenciaInicio"), "vigencia_fim": r.get("vigenciaFim"),
        "adesao": r.get("possibilidadeAdesao"), "cancelada": r.get("cancelado"),
        "palavras": r.get("_palavras", []),
    }


def resumir_pca(r: dict) -> dict:
    return {
        "plano": r.get("idPcaPncp"), "orgao": r.get("orgaoEntidadeRazaoSocial"), "unidade": r.get("nomeUnidade"),
        "ano": r.get("anoPca"), "item": " ".join((r.get("descricaoItem") or "").split()),
        "classe": r.get("classificacaoSuperiorNome"), "categoria": r.get("categoriaItemPcaNome"),
        "grupo_contratacao": r.get("grupoContratacaoNome"), "quantidade": r.get("quantidadeEstimada"),
        "valor_total": r.get("valorTotal"), "data_desejada": r.get("dataDesejada"),
        "palavras": r.get("_palavras", []),
    }


def _partes_controle(controle: str) -> tuple[str, str, str]:
    m = RE_CONTROLE.match(controle.strip())
    if not m:
        raise ErroPNCP(f"número de controle inválido: {controle} (ex.: 00394460000141-1-000123/2026)")
    return m["cnpj"], m["ano"], str(int(m["seq"]))


def detalhe(controle: str) -> dict:
    """Dados de uma contratação (GET /v1/orgaos/{cnpj}/compras/{ano}/{sequencial})."""
    cnpj, ano, seq = _partes_controle(controle)
    return json.loads(_get(f"{BASE_CONSULTA}/orgaos/{cnpj}/compras/{ano}/{seq}") or b"{}")


def _extrair_zip(caminho: Path, profundidade: int = 0) -> list[Path]:
    """Extrai o .zip numa pasta ao lado (e zips dentro dele); ignora caminhos fora da pasta."""
    pasta = caminho.with_suffix("")
    pasta.mkdir(exist_ok=True)
    saida = []
    with zipfile.ZipFile(caminho) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            alvo = (pasta / info.filename).resolve()
            if not alvo.is_relative_to(pasta.resolve()):
                continue
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_bytes(z.read(info))
            if alvo.suffix.lower() == ".zip" and profundidade < 3:
                saida += _extrair_zip(alvo, profundidade + 1)
            else:
                saida.append(alvo)
    return saida


def baixar_arquivos(controle: str, destino: Path) -> list[Path]:
    """Baixa os documentos de uma contratação (edital, TR, anexos, erratas) e extrai os .zip."""
    cnpj, ano, seq = _partes_controle(controle)
    base = f"{BASE_PNCP}/orgaos/{cnpj}/compras/{ano}/{seq}/arquivos"
    lista = json.loads(_get(base) or b"[]")
    destino.mkdir(parents=True, exist_ok=True)
    salvos = []
    for arq in lista:
        if arq.get("statusAtivo") is False:
            continue
        n = arq.get("sequencialDocumento")
        rotulo = " ".join(x for x in (arq.get("tipoDocumentoNome"), arq.get("titulo")) if x) or f"documento_{n}"
        nome = re.sub(r"[^\w.\-]+", "_", rotulo).strip("_")
        url = arq.get("url") or f"{base}/{n}"
        conteudo = _get(url) or b""
        sufixo = ".pdf" if conteudo[:4] == b"%PDF" else (".zip" if conteudo[:2] == b"PK" else "")
        caminho = destino / f"{n:02d}_{nome}" if isinstance(n, int) else destino / nome
        if sufixo and not caminho.name.lower().endswith(sufixo):
            caminho = caminho.with_name(caminho.name + sufixo)
        caminho.write_bytes(conteudo)
        salvos += _extrair_zip(caminho) if sufixo == ".zip" else [caminho]
    (destino / "pncp_arquivos.json").write_text(json.dumps(lista, ensure_ascii=False, indent=2), encoding="utf-8")
    return salvos


def _reais(v) -> str:
    if not isinstance(v, (int, float)):
        return "n.i."
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _curto(t: str, n: int = 180) -> str:
    t = (t or "").replace("|", "/")
    return t[:n] + ("…" if len(t) > n else "")


def tabela_markdown(itens: list[dict], titulo: str, colunas: list[tuple[str, str]], ordem: str) -> str:
    """Tabela genérica: colunas = [(cabeçalho, chave)]; chaves 'valor_*' saem em R$."""
    linhas = [f"# {titulo}", "", f"_PNCP, consultado em {date.today():%d/%m/%Y} · {len(itens)} registro(s)_", "",
              "| " + " | ".join(c for c, _ in colunas) + " |", "|" + "---|" * len(colunas)]
    for i in sorted(itens, key=lambda x: str(x.get(ordem) or "")):
        celulas = []
        for _, k in colunas:
            v = i.get(k)
            v = _reais(v) if k.startswith("valor") else ", ".join(v) if isinstance(v, list) else \
                ("sim" if v is True else "não" if v is False else _curto(str(v or "")[:200]))
            celulas.append(v)
        linhas.append("| " + " | ".join(celulas) + " |")
    return "\n".join(linhas) + "\n"


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
        p.add_argument("--dados-ia", action="store_true", help="usa a lista TERMOS_DADOS_IA como palavras")
        p.add_argument("--max-paginas", type=int, default=400)
        p.add_argument("-f", "--formato", choices=["md", "json"], default="md")
        p.add_argument("-o", "--saida", type=Path)
    for nome in ("contratos", "atas"):
        p = sub.add_parser(nome)
        p.add_argument("--de", required=True)
        p.add_argument("--ate", default=date.today().isoformat())
        p.add_argument("--cnpj", help="CNPJ do órgão")
        p.add_argument("--palavra", action="append", default=[])
        p.add_argument("--max-paginas", type=int, default=400)
        p.add_argument("-f", "--formato", choices=["md", "json"], default="md")
        p.add_argument("-o", "--saida", type=Path)
    p = sub.add_parser("pca", help="itens dos Planos de Contratações Anuais")
    p.add_argument("--ano", type=int)
    p.add_argument("--classe", help="código de classificação superior (com --ano)")
    p.add_argument("--de")
    p.add_argument("--ate")
    p.add_argument("--cnpj")
    p.add_argument("--palavra", action="append", default=[])
    p.add_argument("--max-paginas", type=int, default=400)
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
        if a.cmd == "contratos":
            regs = contratos(a.de, a.ate, a.cnpj, a.max_paginas)
            itens = [resumir_contrato(r) for r in filtrar(regs, a.palavra, ("objetoContrato", "informacaoComplementar"))]
            md = lambda: tabela_markdown(itens, "Contratos publicados", [
                ("Fim da vigência", "vigencia_fim"), ("Órgão (UF)", "orgao"), ("Fornecedor", "fornecedor"),
                ("Objeto", "objeto"), ("Valor global", "valor_global"), ("Palavras", "palavras"),
                ("Controle", "controle")], "vigencia_fim")
        elif a.cmd == "atas":
            regs = atas(a.de, a.ate, a.cnpj, a.max_paginas)
            itens = [resumir_ata(r) for r in filtrar(regs, a.palavra, ("objetoContratacao",))]
            md = lambda: tabela_markdown(itens, "Atas de registro de preços", [
                ("Fim da vigência", "vigencia_fim"), ("Órgão", "orgao"), ("Objeto", "objeto"),
                ("Aceita adesão", "adesao"), ("Cancelada", "cancelada"), ("Palavras", "palavras"),
                ("Ata", "controle")], "vigencia_fim")
        elif a.cmd == "pca":
            regs = pca(a.ano, a.classe, a.de, a.ate, a.cnpj, a.max_paginas)
            itens = [resumir_pca(r) for r in filtrar(regs, a.palavra, ("descricaoItem", "classificacaoSuperiorNome",
                                                                      "grupoContratacaoNome"))]
            md = lambda: tabela_markdown(itens, "Itens de Planos de Contratações Anuais", [
                ("Data desejada", "data_desejada"), ("Órgão", "orgao"), ("Item", "item"), ("Classe", "classe"),
                ("Quantidade", "quantidade"), ("Valor total", "valor_total"), ("Palavras", "palavras")],
                "data_desejada")
        else:
            mod = MODALIDADES.get(a.modalidade) if a.modalidade else None
            regs = (abertas(a.ate, mod, a.uf, a.max_paginas) if a.cmd == "abertas"
                    else publicadas(a.de, a.ate, mod, a.uf, a.max_paginas))
            itens = [resumir(r) for r in filtrar(regs, a.palavra + (TERMOS_DADOS_IA if a.dados_ia else []))]
            titulo = "Contratações com proposta aberta" if a.cmd == "abertas" else "Contratações publicadas"
            md = lambda: para_markdown(itens, titulo)
    except ErroPNCP as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2

    texto = json.dumps(itens, ensure_ascii=False, indent=2) if a.formato == "json" else md()
    if a.saida:
        a.saida.write_text(texto, encoding="utf-8")
        print(f"{len(itens)} de {len(regs)} registro(s) → {a.saida}", file=sys.stderr)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
