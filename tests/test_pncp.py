"""PNCP com respostas simuladas (sem rede)."""

import json

import pytest

import pncp

REG = {
    "numeroControlePNCP": "00394460000141-1-000123/2026", "anoCompra": 2026, "sequencialCompra": 123,
    "numeroCompra": "90012/2026", "modalidadeNome": "Pregão - Eletrônico",
    "objetoCompra": "Contratação de solução de Business Intelligence e  plataforma de DADOS",
    "valorTotalEstimado": 1234567.8, "dataEncerramentoProposta": "2026-10-20T10:00:00",
    "orgaoEntidade": {"cnpj": "00394460000141", "razaoSocial": "MINISTÉRIO X"},
    "unidadeOrgao": {"ufSigla": "DF", "municipioNome": "Brasília"},
}
OUTRO = {**REG, "numeroControlePNCP": "11111111000111-1-000001/2026", "objetoCompra": "Aquisição de cadeiras"}


@pytest.fixture
def api(monkeypatch):
    chamadas = []

    def falso(url, params=None, tentativas=3):
        chamadas.append((url, params))
        if url.endswith("/arquivos"):
            return json.dumps([{"sequencialDocumento": 1, "titulo": "Edital PE 90012", "url": url + "/1"},
                               {"sequencialDocumento": 2, "titulo": "velho", "statusAtivo": False}]).encode()
        if "/arquivos/" in url:
            return b"%PDF-1.7 conteudo"
        pagina = params["pagina"]
        return json.dumps({"data": [REG] if pagina == 1 else [OUTRO], "paginasRestantes": 1 if pagina == 1 else 0}).encode()

    monkeypatch.setattr(pncp, "_get", falso)
    return chamadas


def test_abertas_pagina_e_filtra_sem_acento(api):
    regs = pncp.abertas("2026-10-31", pncp.MODALIDADES["pregao"], None, 5)
    assert len(regs) == 2 and api[0][1]["dataFinal"] == "20261031" and api[0][1]["codigoModalidadeContratacao"] == 6
    itens = [pncp.resumir(r) for r in pncp.filtrar(regs, ["dados", "inteligência"])]
    assert [i["controle"] for i in itens] == ["00394460000141-1-000123/2026"]
    assert itens[0]["palavras"] == ["dados"]
    assert itens[0]["link_pncp"] == "https://pncp.gov.br/app/editais/00394460000141/2026/123"


def test_publicadas_respeita_max_paginas(api):
    assert len(pncp.publicadas("01/10/2026", "05/10/2026", 6, "DF", 1)) == 1
    assert api[0][1]["dataInicial"] == "20261001" and api[0][1]["uf"] == "DF"


def test_markdown(api):
    itens = [pncp.resumir(REG)]
    md = pncp.para_markdown(itens, "Teste")
    assert "R$ 1.234.567,80" in md and "2026-10-20 10:00" in md and "plataforma de DADOS" in md


def test_baixar_arquivos(api, tmp_path):
    salvos = pncp.baixar_arquivos("00394460000141-1-000123/2026", tmp_path)
    assert [p.name for p in salvos] == ["01_Edital_PE_90012.pdf"]
    assert "/orgaos/00394460000141/compras/2026/123/arquivos" in api[0][0]


def test_controle_e_data_invalidos():
    with pytest.raises(pncp.ErroPNCP):
        pncp._partes_controle("123/2026")
    with pytest.raises(pncp.ErroPNCP):
        pncp._data("31-31-2026")


def test_detalhe(monkeypatch):
    urls = []
    monkeypatch.setattr(pncp, "_get", lambda url, params=None, tentativas=3: urls.append(url) or b'{"anoCompra": 2026}')
    assert pncp.detalhe("00394460000141-1-000123/2026") == {"anoCompra": 2026}
    assert urls == ["https://pncp.gov.br/api/consulta/v1/orgaos/00394460000141/compras/2026/123"]
