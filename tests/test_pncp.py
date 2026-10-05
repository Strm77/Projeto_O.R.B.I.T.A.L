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


def test_resumo_usa_campos_do_schema():
    # Campos de RecuperarCompraPublicacaoDTO (Swagger do PNCP, 05/10/2026)
    r = {**REG, "modoDisputaNome": "Aberto", "amparoLegal": {"nome": "Lei 14.133/2021, Art. 28, I"},
         "linkProcessoEletronico": "https://sei", "dataPublicacaoPncp": "2026-10-04T11:46:12"}
    i = pncp.resumir(r)
    assert i["modo_disputa"] == "Aberto" and i["amparo_legal"].startswith("Lei 14.133")
    assert i["publicado_em"] == "2026-10-04T11:46:12" and i["orgao"] == "MINISTÉRIO X"


def _api_unica(monkeypatch, pagina_unica):
    chamadas = []

    def falso(url, params=None, tentativas=3):
        chamadas.append((url, params))
        return json.dumps({"data": pagina_unica, "paginasRestantes": 0}).encode()

    monkeypatch.setattr(pncp, "_get", falso)
    return chamadas


def test_contratos(monkeypatch):
    c = _api_unica(monkeypatch, [{"numeroControlePNCP": "x", "objetoContrato": "Subscrição Power BI Pro",
                                  "orgaoEntidade": {"razaoSocial": "ÓRGÃO"}, "valorGlobal": 10.5,
                                  "dataVigenciaFim": "2027-01-31", "nomeRazaoSocialFornecedor": "EMPRESA"},
                                 {"objetoContrato": "Limpeza predial"}])
    regs = pncp.contratos("01/01/2026", "05/10/2026", "123", 3)
    assert c[0][0].endswith("/v1/contratos") and c[0][1]["cnpjOrgao"] == "123" and c[0][1]["dataInicial"] == "20260101"
    itens = [pncp.resumir_contrato(r) for r in pncp.filtrar(regs, ["power bi"], ("objetoContrato",))]
    assert len(itens) == 1 and itens[0]["fornecedor"] == "EMPRESA" and itens[0]["vigencia_fim"] == "2027-01-31"
    md = pncp.tabela_markdown(itens, "T", [("Fim", "vigencia_fim"), ("Valor", "valor_global")], "vigencia_fim")
    assert "| 2027-01-31 | R$ 10,50 |" in md


def test_atas(monkeypatch):
    c = _api_unica(monkeypatch, [{"numeroControlePNCPAta": "a1", "objetoContratacao": "Observabilidade de aplicações",
                                  "possibilidadeAdesao": True}])
    itens = [pncp.resumir_ata(r) for r in pncp.filtrar(pncp.atas("2026-10-01", "2027-10-01", None, 1),
                                                         ["observabilidade"], ("objetoContratacao",))]
    assert c[0][0].endswith("/v1/atas") and itens[0]["adesao"] is True


def test_pca_por_atualizacao_achata_itens(monkeypatch):
    c = _api_unica(monkeypatch, [{"idPcaPncp": "p1", "anoPca": 2027, "orgaoEntidadeRazaoSocial": "ÓRGÃO",
                                  "itens": [{"descricaoItem": "Plataforma de dados em nuvem", "valorTotal": 5},
                                            {"descricaoItem": "Cadeiras"}]}])
    regs = pncp.pca(None, None, "2026-09-01", "2026-10-05", None, 2)
    assert c[0][0].endswith("/v1/pca/atualizacao") and c[0][1]["dataInicio"] == "20260901" and "dataInicial" not in c[0][1]
    itens = [pncp.resumir_pca(r) for r in pncp.filtrar(regs, ["dados"], ("descricaoItem",))]
    assert [(i["plano"], i["item"]) for i in itens] == [("p1", "Plataforma de dados em nuvem")]


def test_pca_por_ano_e_classe(monkeypatch):
    c = _api_unica(monkeypatch, [])
    pncp.pca(2027, "70", None, None, None, 1)
    assert c[0][0].endswith("/v1/pca/") and c[0][1]["anoPca"] == 2027 and c[0][1]["codigoClassificacaoSuperior"] == "70"
    with pytest.raises(pncp.ErroPNCP):
        pncp.pca(2027, None, None, None, None, 1)
