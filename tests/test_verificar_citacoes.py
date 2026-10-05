"""Testes do verificar_citacoes.py com citações certas e erradas de propósito."""

from pathlib import Path

import pytest

import extrair_pdf
import verificar_citacoes as vc

FIXTURES = Path(__file__).parent / "fixtures"
PDFS = [FIXTURES / "edital_pe_90042_2026.pdf", FIXTURES / "errata_01_digitalizada.pdf"]
ED = "edital_pe_90042_2026.pdf"
TR = "Anexo I — Termo de Referência"


@pytest.fixture(scope="module")
def docs():
    if extrair_pdf._ocr_indisponivel():
        pytest.skip("tesseract/por indisponível (errata é escaneada)")
    return vc.carregar(PDFS)


def nivel(docs, texto):
    (r,) = vc.verificar(texto, docs)
    return r["nivel"], " ".join(r["msg"])


@pytest.mark.parametrize("texto", [
    f'"30 (trinta) dias corridos" `[{ED}, item 7.3, p. 3]`',
    f'"15 (quinze) dias corridos" `[{ED}, {TR}, item 6.2, p. 7]`',
    f'"500.000 (quinhentos mil) registros" `[{ED}, item 8.5.2, p. 3–4]`',
    f'"consórcio" `[{ED}, item 2.3, alínea d, p. 2]`',
    f'"0,33%" `[{ED}, Anexo IV — Minuta de Termo de Contrato, cláusula 7, item 7.1, p. 13]`',
    '"28/10/2026" `[errata_01_digitalizada.pdf, item 2, p. 1]`',
])
def test_citacoes_corretas(docs, texto):
    assert nivel(docs, texto)[0] == "OK"


@pytest.mark.parametrize("texto, trecho_msg", [
    (f'"30 (trinta) dias corridos" `[{ED}, item 7.3, p. 4]`', "está na(s) p. [3]"),
    (f'"500.000 (quinhentos mil) registros" `[{ED}, item 8.5.2, p. 3]`', "aparece na p. [4]"),
    (f"`[{ED}, Anexo II — Requisitos, item 6.2, p. 7]`", "não encontrado em Anexo II"),
    (f"`[{ED}, item 18.1, p. 5]`", "item 18.1 não encontrado"),
    (f'"até 45 (quarenta e cinco) dias corridos" `[{ED}, item 7.3, p. 3]`', "não encontrada no documento"),
    ('"30 (trinta) dias" `[Edital, item 7.3, p. 9]`', "nem apelido declarado"),
    ('"20/10/2026, às 10h00" `[errata_01_digitalizada.pdf, item 2, p. 1]`', "fora do(s) item(ns) 2"),
    (f"`[{ED}, item 7.3, p. 99]`", "página fora do documento"),
    ("`[outro.pdf, item 1, p. 1]`", "não está entre os PDFs"),
])
def test_citacoes_erradas_viram_erro(docs, texto, trecho_msg):
    n, msg = nivel(docs, texto)
    assert n == "ERRO" and trecho_msg in msg


def test_ocr_aproximado_vira_aviso(docs):
    # O OCR leu "LÉ"; a transcrição com o acento certo só confere por aproximação.
    n, msg = nivel(docs, '"ONDE SE LÊ, no preâmbulo do Edital" `[errata_01_digitalizada.pdf, item 1, p. 1]`')
    assert n == "AVISO" and "OCR" in msg


def test_ocr_nao_aproxima_numeros(docs):
    # Datas diferentes nunca podem passar como "aproximadas".
    n, _ = nivel(docs, '"até as 23h59 do dia 16/10/2026" `[errata_01_digitalizada.pdf, item 2, p. 1]`')
    assert n == "ERRO"


def test_cli_codigo_de_saida(tmp_path, capsys):
    if extrair_pdf._ocr_indisponivel():
        pytest.skip("tesseract/por indisponível")
    ok = tmp_path / "ok.md"
    ok.write_text(f'"30 (trinta) dias corridos" `[{ED}, item 7.3, p. 3]`', encoding="utf-8")
    ruim = tmp_path / "ruim.md"
    ruim.write_text(f"`[{ED}, item 7.3, p. 4]`", encoding="utf-8")
    assert vc.main([str(ok), *map(str, PDFS)]) == 0
    assert vc.main([str(ruim), *map(str, PDFS)]) == 1
    assert "1 erro(s)" in capsys.readouterr().out


def test_analise_de_referencia_sem_erros(docs):
    """A análise de referência do edital fictício não pode regredir."""
    ref = FIXTURES / "referencia"
    texto = (ref / "analise_pe_90042_2026.md").read_text(encoding="utf-8")
    resultados = vc.verificar(texto, docs)
    assert len(resultados) >= 90
    assert [r for r in resultados if r["nivel"] != "OK"] == []
    # errata prevalece: data superada só aparece marcada como superada
    for linha in texto.splitlines():
        if "20/10/2026" in linha or "15/10/2026" in linha:
            assert "superado" in linha
    # contradição proposital apontada com as duas fontes
    assert any("item 7.3, p. 3" in l and "Termo de Referência, item 6.2, p. 7" in l
               for l in texto.splitlines() if l.startswith("| 1 | Prazo de implantação"))


# --- Forma curta com apelidos (formato do gabarito em perguntas e respostas) --------

APELIDOS = vc.ler_apelidos([f"Edital={ED}", f"TR={ED}:Anexo I", f"Req={ED}:Anexo II",
                            f"Minuta={ED}:Anexo IV"])


def nivel_curto(docs, texto):
    (r,) = vc.verificar(texto, docs, APELIDOS)
    return r["nivel"], " ".join(r["msg"])


@pytest.mark.parametrize("texto", [
    "📍 [TR, 6.1–6.3, p. 7]",                      # intervalo de itens
    "📍 [Edital, 7.2, 7.3, p. 3]",                  # vários itens
    "📍 [TR, 4.1 e 4.3, p. 6]",                     # "e"
    "📍 [Minuta, cl. 7.1, p. 13]",                  # cláusula abreviada
    "📍 [Edital, preâmbulo, p. 1]",                 # só página
    "📍 [TR, 7.1, item 2, p. 7]",                   # linha de tabela do item 7.1
    "📍 [Req, seções 2–3, p. 10]",                  # seções
    "📍 [Edital, 7.3 e 8.5.2, p. 3–4]",             # intervalo de páginas
    "📍 [TR, 6.2 e 9.3, p. 7 e 8]",                 # páginas soltas
    '"15 (quinze) dias corridos" [TR, 6.2, p. 7]',   # transcrição + forma curta
])
def test_forma_curta_correta(docs, texto):
    assert nivel_curto(docs, texto) == ("OK", "")


@pytest.mark.parametrize("texto, trecho_msg", [
    ("[TR, 6.2, p. 3]", "item 6.2 está na(s) p. [7]"),
    ("[TR, 99.1, p. 7]", "item 99.1 não encontrado em Anexo I"),
    ("[Minuta, cl. 7.1, p. 7]", "não na(s) p. [7]"),
    ("[ETP, seção 5, p. 2]", "nem apelido declarado"),
    ('"30 (trinta) dias corridos" [TR, 6.2, p. 7]', "não está na(s) página(s) citada(s); aparece na p. [3]"),
])
def test_forma_curta_errada(docs, texto, trecho_msg):
    n, msg = nivel_curto(docs, texto)
    assert n == "ERRO" and trecho_msg in msg


def test_legenda_no_proprio_texto(docs):
    texto = f"<!-- orbital:alias TR={ED}:Anexo I; Edital={ED} -->\n📍 [TR, 6.2, p. 7] · [Edital, 7.3, p. 3]"
    resultados = vc.verificar(texto, docs)
    assert [r["nivel"] for r in resultados] == ["OK", "OK"]
