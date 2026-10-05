"""Testes do orbital/scripts/extrair_pdf.py sobre o edital fictício de tests/fixtures."""

import json
from pathlib import Path

import pytest

import extrair_pdf as ex

FIXTURES = Path(__file__).parent / "fixtures"
EDITAL = FIXTURES / "edital_pe_90042_2026.pdf"
ERRATA = FIXTURES / "errata_01_digitalizada.pdf"
TR = "Anexo I — Termo de Referência"

sem_ocr = pytest.mark.skipif(ex._ocr_indisponivel() is not None, reason="tesseract/por indisponível")


@pytest.fixture(scope="module")
def edital():
    return ex.extrair(EDITAL)


@pytest.fixture(scope="module")
def errata():
    if ex._ocr_indisponivel():
        pytest.skip("tesseract/por indisponível")
    return ex.extrair(ERRATA)


def achar(trechos, item, secao=None, clausula=None, alinea=None):
    return [t for t in trechos
            if t.item == item and t.secao == secao and t.clausula == clausula and t.alinea == alinea]


# --- Marcadores ---------------------------------------------------------------

@pytest.mark.parametrize("linha, tipo, n", [
    ("8.5.2. Para fins da comprovação", "item", "8.5.2"),
    ("9.4.2 A contratada deverá", "item", "9.4.2"),
    ("1. DO OBJETO", "item", "1"),
    ("8 DA HABILITAÇÃO", "item", "8"),
    ("a) aquele que não atenda", "alinea", "a"),
    ("IV - efetuar os pagamentos", "inciso", "IV"),
    ("CLÁUSULA SÉTIMA – DAS SANÇÕES", "clausula", "7"),
    ("Cláusula 7ª - Das sanções", "clausula", "7"),
    ("ANEXO II – REQUISITOS", "anexo", "II"),
])
def test_marcador_reconhece(linha, tipo, n):
    m = ex._marcador(linha)
    assert m and m["tipo"] == tipo and m["n"] == n


@pytest.mark.parametrize("linha", [
    "15 (quinze) dias corridos",       # número solto não é item
    "1.234,56 reais",                  # valor monetário
    "22/10/2026, às 10h00",            # data
    "2026 foi o ano",                  # ano
    "01.02 texto",                     # componente com zero à esquerda
])
def test_marcador_ignora_falsos_positivos(linha):
    assert ex._marcador(linha) is None


# --- Edital (camada de texto) -------------------------------------------------

def test_documento_e_paginas(edital):
    doc, trechos = edital
    assert doc.paginas == 15
    assert doc.tipo_documento == "edital"
    assert doc.paginas_ocr == []
    assert {t.pagina for t in trechos} == set(range(1, 16))
    assert all(t.pagina_impressa == t.pagina for t in trechos)


def test_cabecalho_e_rodape_removidos(edital):
    _, trechos = edital
    assert not any("USO EXCLUSIVO EM TESTES" in t.texto for t in trechos)
    assert not any(t.texto.startswith("Página ") for t in trechos)


def test_contradicao_prazo_implantacao_edital_x_tr(edital):
    _, trechos = edital
    (no_edital,) = achar(trechos, "7.3")
    (no_tr,) = achar(trechos, "6.2", secao=TR)
    assert "30 (trinta) dias corridos" in no_edital.texto and "assinatura do contrato" in no_edital.texto
    assert "15 (quinze) dias corridos" in no_tr.texto and "Ordem de Serviço" in no_tr.texto
    assert no_edital.citacao == "[edital_pe_90042_2026.pdf, item 7.3, p. 3]"
    assert no_tr.citacao == f"[edital_pe_90042_2026.pdf, {TR}, item 6.2, p. {no_tr.pagina}]"


def test_item_que_atravessa_pagina(edital):
    _, trechos = edital
    partes = achar(trechos, "8.5.2")
    assert [(t.pagina, t.continuacao) for t in partes] == [(3, False), (4, True)]
    assert partes[0].texto.startswith("8.5.2.")
    assert "documentos idôneos" in partes[1].texto


def test_secoes_dos_anexos(edital):
    _, trechos = edital
    secoes = list(dict.fromkeys(t.secao for t in trechos))
    assert secoes == [
        None, TR, "Anexo II — Requisitos Técnicos da Solução",
        "Anexo III — Modelo de Proposta de Preços", "Anexo IV — Minuta de Termo de Contrato",
        "Anexo V — Termo de Confidencialidade da Informação",
    ]


def test_lista_de_anexos_nao_abre_secao(edital):
    _, trechos = edital
    (lista,) = achar(trechos, "15.1")
    assert "ANEXO I – Termo de Referência" in lista.texto
    assert "ANEXO V – Termo de Confidencialidade" in lista.texto


def test_alinea(edital):
    _, trechos = edital
    (t,) = achar(trechos, "2.3", alinea="d")
    assert "consórcio" in t.texto
    assert t.citacao.endswith("item 2.3, alínea d, p. 2]")


def test_clausula_da_minuta(edital):
    _, trechos = edital
    (t,) = achar(trechos, "7.1", secao="Anexo IV — Minuta de Termo de Contrato", clausula="7")
    assert "0,33%" in t.texto
    assert "cláusula 7, item 7.1" in t.citacao


def test_tabela_imr_preserva_linhas(edital):
    _, trechos = edital
    (t,) = achar(trechos, "7.1", secao=TR)
    assert "| IND-01 Disponibilidade da plataforma | 99,5% ao mês |" in t.texto
    assert "| IND-03 Tempo de solução de incidente crítico (P1) | 4 horas |" in t.texto


def test_indice_lista_paginas_do_item(edital):
    _, trechos = edital
    entrada = next(e for e in ex.indice(trechos) if e["item"] == "8.5.2" and e["secao"] is None)
    assert entrada["paginas"] == [3, 4]


# --- Errata (escaneada → OCR) -------------------------------------------------

@sem_ocr
def test_errata_detectada_e_lida_por_ocr(errata):
    doc, trechos = errata
    assert doc.tipo_documento == "errata"
    assert doc.paginas_ocr == [1]
    assert all(t.metodo == "ocr" and t.confianca_ocr for t in trechos)
    (nova_sessao,) = achar(trechos, "1")
    (novo_prazo,) = achar(trechos, "2")
    assert "20/10/2026" in nova_sessao.texto and "03/11/2026" in nova_sessao.texto
    assert "15/10/2026" in novo_prazo.texto and "28/10/2026" in novo_prazo.texto


def test_pdf_escaneado_sem_ocr_gera_aviso():
    doc, trechos = ex.extrair(ERRATA, ocr="nunca")
    assert doc.paginas_sem_texto == [1]
    assert trechos == []
    assert any("OCR não rodou" in a for a in doc.avisos)


# --- CLI ----------------------------------------------------------------------

def test_cli_json(tmp_path):
    saida = tmp_path / "x.json"
    assert ex.main([str(EDITAL), "-f", "json", "-o", str(saida)]) == 0
    dados = json.loads(saida.read_text(encoding="utf-8"))
    assert dados["documentos"][0]["arquivo"] == EDITAL.name
    t = dados["trechos"][0]
    assert {"arquivo", "pagina", "item", "secao", "texto", "citacao"} <= t.keys()


def test_cli_markdown(tmp_path, capsys):
    assert ex.main([str(EDITAL), "-f", "md"]) == 0
    md = capsys.readouterr().out
    assert md.startswith("<!-- orbital/extrair_pdf.py")
    assert "`[edital_pe_90042_2026.pdf, item 7.3, p. 3]`" in md


def test_cli_arquivo_inexistente(tmp_path):
    assert ex.main([str(tmp_path / "nao_existe.pdf")]) == 2


# --- Padrões vistos em editais reais (BCB PE 327/2026) -------------------------

@pytest.mark.parametrize("linha, n", [("1.1.", "1.1"), ("7.10.1", "7.10.1"), ("12.", "12")])
def test_numero_de_item_sozinho_na_linha(linha, n):
    m = ex._marcador(linha)
    assert m and m["tipo"] == "item" and m["n"] == n


@pytest.mark.parametrize("linha", ["12", "35", "2.200", "01.1"])
def test_numero_sozinho_que_nao_e_item(linha):
    assert ex._marcador(linha) is None


@pytest.mark.parametrize("texto, n", [("P á g i n a 4 | 35", 4), ("Página 7 de 15", 7)])
def test_paginacao_impressa(texto, n):
    assert int(ex.RE_PAGINA_IMPRESSA.search(ex._compactar_espacadas(texto))["n"]) == n


def test_paginacao_n_de_total():
    assert int(ex.RE_PAGINA_DE.match("2 de 17")["n"]) == 2


def test_caractere_invisivel_e_subtitulo():
    assert ex.RE_INVISIVEIS.sub("", "​1.1. Contratação") == "1.1. Contratação"
    assert ex._eh_subtitulo("Consórcio") and ex._eh_subtitulo("Requisitos de Garantia e Manutenção")
    assert not ex._eh_subtitulo("o prazo de entrega será de até 30 (trinta) dias, contados a partir da")


def test_anexo_com_letra():
    m = ex._marcador("ANEXO C")
    assert m and m["tipo"] == "anexo" and m["n"] == "C"


def test_sumario_nao_abre_clausula():
    assert ex._marcador("CLÁUSULA NONA – DAS SANÇÕES ........................ 22") is None
    assert ex._marcador("8.1 Da habilitação técnica ______ 14") is None


def test_clausula_numerada_da_minuta():
    m = ex._marcador("1. CLÁUSULA PRIMEIRA – DO OBJETO")
    assert m and m["tipo"] == "clausula" and m["n"] == "1"


def test_total_impresso_detecta_paginas_faltando(tmp_path):
    import pymupdf as fitz
    pdf = fitz.open()
    for n in (1, 2):
        pdf.new_page().insert_text((72, 800), f"Página {n} / 5")
    assert ex._total_impresso(pdf) == 5
