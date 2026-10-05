"""Regressão com editais reais (tests/gabaritos/). Pula o caso se os PDFs não estiverem lá."""

from pathlib import Path

import pytest

import extrair_pdf as ex
import verificar_citacoes as vc

BCB = Path(__file__).parent / "gabaritos" / "bcb_pe_327_2026_ibm"
PDFS = [BCB / "edital.pdf", BCB / "tr.pdf", BCB / "etp.pdf"]
APELIDOS = ["Edital=edital.pdf", "TR=tr.pdf", "ETP=etp.pdf",
            "Minuta=edital.pdf:Anexo II", "Minuta de Contrato=edital.pdf:Anexo II"]

pytestmark = pytest.mark.skipif(not all(p.is_file() for p in PDFS), reason="PDFs do BCB ausentes")


@pytest.fixture(scope="module")
def extraidos():
    return {p.stem: ex.extrair(p) for p in PDFS}


def test_tipos_e_paginas(extraidos):
    tipos = {nome: doc.tipo_documento for nome, (doc, _) in extraidos.items()}
    assert tipos == {"edital": "edital", "tr": "termo_referencia", "etp": "etp"}
    assert {nome: doc.paginas for nome, (doc, _) in extraidos.items()} == {"edital": 35, "tr": 36, "etp": 17}
    # Nos três arquivos a página do PDF é a página impressa ("P á g i n a 4 | 35", "2 de 17").
    for _, trechos in extraidos.values():
        assert all(t.pagina_impressa in (None, t.pagina) for t in trechos)


def test_item_com_numero_sozinho_na_linha(extraidos):
    _, trechos = extraidos["edital"]
    (t,) = [t for t in trechos if t.item == "5.9" and t.secao is None]
    assert t.pagina == 9 and "60 (sessenta) dias" in t.texto


def test_anexos_do_edital(extraidos):
    _, trechos = extraidos["edital"]
    paginas = {}
    for t in trechos:
        if t.secao:
            paginas.setdefault(t.secao.split(" — ")[0], set()).add(t.pagina)
    assert paginas["Anexo II"] == set(range(22, 32))  # minuta de contrato
    assert min(paginas["Anexo III"]) == 32 and min(paginas["Anexo IV"]) == 34


def test_linha_de_tabela_nao_vira_item(extraidos):
    # "1.6 Cloud Pak..." (TR p. 2) e "1.12 D27RMLL..." (ETP p. 8) são linhas de tabela.
    _, tr = extraidos["tr"]
    assert all(t.item != "1.6" for t in tr if t.pagina == 2)
    assert any(t.item == "1.1" and t.pagina == 2 and "1.11" in t.texto for t in tr)
    _, etp = extraidos["etp"]
    assert all(t.item != "1.12" for t in etp)


def test_citacoes_do_gabarito_conferem():
    docs = vc.carregar(PDFS)
    texto = (BCB / "perguntas.md").read_text(encoding="utf-8")
    resultados = vc.verificar(texto, docs, vc.ler_apelidos(APELIDOS))
    assert len(resultados) == 89
    assert [(r["citacao"], r["msg"]) for r in resultados if r["nivel"] != "OK"] == []


# --- MIDR, TR 7/2026 (serviços de dados): TR + Anexos A a K -------------------------

MIDR = Path(__file__).parent / "gabaritos" / "midr_tr_7_2026_dados"
MIDR_PDFS = sorted(MIDR.glob("*.pdf"))
MIDR_APELIDOS = ["TR=tr.pdf"] + [f"An. {l}=anexo_{l.lower()}.pdf" for l in "ABCDEFGHIJK"]
sem_midr = pytest.mark.skipif(len(MIDR_PDFS) != 12, reason="PDFs do MIDR ausentes")


@sem_midr
def test_midr_padroes_de_pdf_real():
    _, tr = ex.extrair(MIDR / "tr.pdf")
    # "​1.1." (caractere invisível) e itens após subtítulo em caixa normal ("Consórcio")
    assert any(t.item == "1.1" and t.pagina == 1 for t in tr)
    assert any(t.item == "4.81" and t.pagina == 19 and "consórcio" in t.texto for t in tr)
    # anexo que se intitula "ANEXO I" vira seção raiz do próprio arquivo
    _, an_i = ex.extrair(MIDR / "anexo_i.pdf")
    assert all(t.secao and t.secao.startswith("Anexo I ") for t in an_i if t.pagina == 3)


@sem_midr
def test_midr_citacoes_do_gabarito():
    docs = vc.carregar(MIDR_PDFS)
    texto = (MIDR / "perguntas.md").read_text(encoding="utf-8")
    resultados = vc.verificar(texto, docs, vc.ler_apelidos(MIDR_APELIDOS))
    assert len(resultados) == 82
    erros = [r["citacao"] for r in resultados if r["nivel"] != "OK"]
    # Único erro conhecido: "No ETP" entre aspas é paráfrase de "estabelecida no Estudo
    # Técnico Preliminar" (Anexo D, p. 1) — ver notas_revisao.md.
    assert erros == ["[An. D, p. 1]"]


# --- Teste cego: análise feita pela skill sem ver o gabarito ------------------------

@pytest.mark.parametrize("pasta, pdfs, total", [
    pytest.param(BCB, PDFS, 355, id="bcb"),
    pytest.param(MIDR, MIDR_PDFS, 392, id="midr", marks=sem_midr),
])
def test_teste_cego_citacoes(pasta, pdfs, total):
    docs = vc.carregar(pdfs)
    texto = (pasta / "teste_cego_resultado.md").read_text(encoding="utf-8")
    resultados = vc.verificar(texto, docs, vc.ler_apelidos([]))
    assert len(resultados) == total
    assert [(r["citacao"], r["msg"]) for r in resultados if r["nivel"] != "OK"] == []
