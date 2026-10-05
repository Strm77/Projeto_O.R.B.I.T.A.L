#!/usr/bin/env python3
"""Extrai texto de PDFs de licitação preservando página e numeração de itens.

Cada trecho extraído carrega {arquivo, pagina, secao, clausula, item, alinea,
inciso} e uma string de citação pronta, no formato usado pela skill orbital:
    [edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 9]

Páginas sem camada de texto (PDF escaneado) passam por OCR em português
(Tesseract, idioma "por"), decidido página a página.

Uso:
    python extrair_pdf.py edital.pdf errata.pdf --formato md -o extracao.md
    python extrair_pdf.py edital.pdf --formato json > extracao.json
    python extrair_pdf.py edital.pdf --ocr sempre

Dependências: pymupdf (obrigatória); pytesseract + tesseract-ocr-por (para OCR).
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover
    try:
        import fitz  # PyMuPDF < 1.24
    except ImportError:
        sys.exit("Requer PyMuPDF: pip install pymupdf")

VERSAO = "0.1.0"

# Página com menos caracteres visíveis que isso é tratada como sem camada de texto.
MIN_CHARS_TEXTO = 25
# Faixa (fração da altura) onde ficam cabeçalho e rodapé. Blocos nessa faixa só
# são removidos se se repetem em várias páginas ou se são só a paginação.
FAIXA_MARGEM = 0.15
OCR_DPI = 300
OCR_IDIOMA = "por"

# --- Marcadores de estrutura -------------------------------------------------

RE_ITEM = re.compile(
    r"^(?P<num>\d{1,2}(?:\.\d{1,2}){0,5})(?P<sep>\.|\)|\s*[-–—]|)\s+(?P<resto>\S.*)$"
)
# Número de item sozinho na linha, com o texto na linha seguinte (comum em editais
# diagramados em duas colunas): "1.1." / "7.10.1" / "12."
RE_ITEM_SOZINHO = re.compile(r"^(?P<num>\d{1,2}(?:\.\d{1,2}){0,5})(?P<ponto>\.?)$")
RE_ALINEA = re.compile(r"^(?P<al>[a-z])\)\s+(?P<resto>\S.*)$")
RE_INCISO = re.compile(r"^(?P<inc>[IVX]{1,6})\s*[-–—]\s+(?P<resto>\S.*)$")
RE_CLAUSULA = re.compile(
    r"^CL[ÁA]USULA\s+(?P<n>\d{1,2}|[A-ZÀ-Ú]+)\s*[ªºa]?\s*(?:[-–—.:]\s*)?(?P<resto>.*)$",
    re.IGNORECASE,
)
RE_ANEXO = re.compile(r"^ANEXO\s+(?P<n>[IVXL]+|\d{1,2})\b\s*(?:[-–—:.]\s*)?(?P<resto>.*)$")
RE_PAGINA_IMPRESSA = re.compile(
    r"\bp[áa]g(?:ina)?\.?\s*(?P<n>\d{1,4})(?:\s*(?:de|/|\|)\s*\d{1,4})?\b", re.IGNORECASE
)
RE_PAGINA_DE = re.compile(r"^(?P<n>\d{1,4})\s*(?:de|/)\s*\d{1,4}$")  # "2 de 17"


def _compactar_espacadas(texto: str) -> str:
    """'P á g i n a 4 | 35' → 'Página 4 | 35' (letras separadas por espaço)."""
    return re.sub(r"\b(?:\w ){2,}\w\b", lambda m: m.group(0).replace(" ", ""), texto)

ORDINAIS = {
    "PRIMEIRA": 1, "SEGUNDA": 2, "TERCEIRA": 3, "QUARTA": 4, "QUINTA": 5,
    "SEXTA": 6, "SETIMA": 7, "OITAVA": 8, "NONA": 9, "DECIMA": 10,
}


def _sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _numero_clausula(token: str) -> str:
    if token.isdigit():
        return token
    return str(ORDINAIS.get(_sem_acento(token).upper(), token.capitalize()))


def _eh_item(num: str, sep: str, resto: str) -> bool:
    partes = num.split(".")
    if any(len(p) > 1 and p.startswith("0") for p in partes):
        return False
    if len(partes) > 1 or sep:
        return True
    # "8 DA HABILITAÇÃO" (sem pontuação) só conta se o título vier em caixa alta.
    primeira = resto.split()[0]
    return len(primeira) >= 2 and primeira.isupper()


def _marcador(linha: str) -> dict | None:
    """Identifica se a linha abre item, alínea, inciso, cláusula ou anexo."""
    if m := RE_ANEXO.match(linha):
        return {"tipo": "anexo", "n": m["n"], "resto": m["resto"].strip()}
    if m := RE_CLAUSULA.match(linha):
        return {"tipo": "clausula", "n": _numero_clausula(m["n"]), "resto": m["resto"].strip()}
    if (m := RE_ITEM.match(linha)) and _eh_item(m["num"], m["sep"].strip(), m["resto"]):
        return {"tipo": "item", "n": m["num"]}
    if (m := RE_ITEM_SOZINHO.match(linha)) and ("." in m["num"] or m["ponto"]):
        if not any(len(p) > 1 and p.startswith("0") for p in m["num"].split(".")):
            return {"tipo": "item", "n": m["num"]}
    if m := RE_ALINEA.match(linha):
        return {"tipo": "alinea", "n": m["al"]}
    if m := RE_INCISO.match(linha):
        return {"tipo": "inciso", "n": m["inc"]}
    return None


# --- Estruturas --------------------------------------------------------------

@dataclass
class Bloco:
    linhas: list[str]
    y0: float  # fração da altura da página (0 = topo)
    y1: float
    confianca: float | None = None  # média do OCR, quando aplicável
    tabela: bool = False  # linhas são linhas de tabela ("| a | b |")


@dataclass
class Trecho:
    arquivo: str
    tipo_documento: str
    pagina: int
    pagina_impressa: int | None
    secao: str | None
    clausula: str | None
    item: str | None
    alinea: str | None
    inciso: str | None
    texto: str
    metodo: str  # "texto" | "ocr"
    confianca_ocr: float | None
    continuacao: bool = False  # item que vem da página anterior
    citacao: str = ""


@dataclass
class Documento:
    arquivo: str
    caminho: str
    sha256: str
    paginas: int
    tipo_documento: str
    paginas_ocr: list[int] = field(default_factory=list)
    paginas_sem_texto: list[int] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)


# --- Leitura das páginas -----------------------------------------------------

def _ocr_indisponivel() -> str | None:
    """Retorna o motivo se o OCR não puder rodar; None se estiver disponível."""
    try:
        import pytesseract
    except ImportError:
        return "pytesseract não instalado (pip install pytesseract)"
    try:
        idiomas = pytesseract.get_languages(config="")
    except Exception as e:  # binário ausente
        return f"tesseract não encontrado ({e.__class__.__name__})"
    if OCR_IDIOMA not in idiomas:
        return f"idioma '{OCR_IDIOMA}' do tesseract não instalado (apt install tesseract-ocr-por)"
    return None


def _tabelas(pagina: fitz.Page) -> list[tuple[fitz.Rect, list[str]]]:
    """Tabelas com grade, como linhas Markdown. Sem find_tables (PyMuPDF antigo): []."""
    if not hasattr(pagina, "find_tables"):
        return []
    tabelas = []
    with contextlib.redirect_stdout(io.StringIO()):  # PyMuPDF imprime dicas no stdout
        encontradas = pagina.find_tables().tables
    for tab in encontradas:
        linhas = []
        for linha in tab.extract():
            celulas = [re.sub(r"\s+", " ", c or "").strip() for c in linha]
            if any(celulas):
                linhas.append("| " + " | ".join(celulas) + " |")
        if linhas:
            tabelas.append((fitz.Rect(tab.bbox), linhas))
    return tabelas


def _blocos_texto(pagina: fitz.Page) -> list[Bloco]:
    altura = pagina.rect.height
    tabelas = _tabelas(pagina)
    blocos = [Bloco(linhas, r.y0 / altura, r.y1 / altura, tabela=True) for r, linhas in tabelas]
    for x0, y0, x1, y1, texto, _n, tipo in pagina.get_text("blocks", sort=True):
        if tipo != 0:
            continue
        centro = fitz.Point((x0 + x1) / 2, (y0 + y1) / 2)
        if any(centro in r for r, _ in tabelas):
            continue  # já capturado como tabela
        linhas = [l.strip() for l in texto.splitlines() if l.strip()]
        if linhas:
            blocos.append(Bloco(linhas, y0 / altura, y1 / altura))
    blocos.sort(key=lambda b: b.y0)
    return blocos


def _blocos_ocr(pagina: fitz.Page) -> list[Bloco]:
    import pytesseract
    from PIL import Image

    pix = pagina.get_pixmap(dpi=OCR_DPI, colorspace=fitz.csGRAY)
    img = Image.frombytes("L", (pix.width, pix.height), pix.samples)
    dados = pytesseract.image_to_data(
        img, lang=OCR_IDIOMA, config="--psm 3", output_type=pytesseract.Output.DICT
    )
    # Agrupa palavras em parágrafos (bloco, parágrafo) e linhas.
    pars: dict[tuple, dict] = {}
    for i, palavra in enumerate(dados["text"]):
        palavra = palavra.strip()
        if not palavra:
            continue
        chave = (dados["block_num"][i], dados["par_num"][i])
        p = pars.setdefault(chave, {"linhas": {}, "y0": 1.0, "y1": 0.0, "conf": []})
        p["linhas"].setdefault(dados["line_num"][i], []).append(palavra)
        topo = dados["top"][i] / pix.height
        p["y0"] = min(p["y0"], topo)
        p["y1"] = max(p["y1"], topo + dados["height"][i] / pix.height)
        conf = float(dados["conf"][i])
        if conf >= 0:
            p["conf"].append(conf)
    blocos = []
    for chave in sorted(pars):
        p = pars[chave]
        linhas = [" ".join(p["linhas"][n]) for n in sorted(p["linhas"])]
        conf = round(sum(p["conf"]) / len(p["conf"]), 1) if p["conf"] else None
        blocos.append(Bloco(linhas, p["y0"], p["y1"], conf))
    return blocos


def _precisa_ocr(pagina: fitz.Page) -> bool:
    visiveis = re.sub(r"\s", "", pagina.get_text("text"))
    return len(visiveis) < MIN_CHARS_TEXTO


# --- Cabeçalho, rodapé e numeração impressa ---------------------------------

def _normaliza_margem(bloco: Bloco) -> str:
    return re.sub(r"\d+", "#", " ".join(bloco.linhas).lower())


def _eh_margem(bloco: Bloco) -> bool:
    return bloco.y1 <= FAIXA_MARGEM or bloco.y0 >= 1 - FAIXA_MARGEM


def _separar_margens(paginas: list[list[Bloco]]) -> tuple[list[list[Bloco]], list[int | None]]:
    """Remove cabeçalhos/rodapés repetidos e devolve o número impresso de cada página."""
    contagem: Counter[str] = Counter()
    for blocos in paginas:
        for chave in {_normaliza_margem(b) for b in blocos if _eh_margem(b)}:
            contagem[chave] += 1
    minimo = max(2, (len(paginas) + 1) // 2)

    limpas, impressas = [], []
    for blocos in paginas:
        numero = None
        corpo = []
        for b in blocos:
            if not _eh_margem(b):
                corpo.append(b)
                continue
            texto = _compactar_espacadas(" ".join(b.linhas))
            if m := RE_PAGINA_IMPRESSA.search(texto) or RE_PAGINA_DE.match(texto.strip()):
                numero = int(m["n"])
            elif texto.strip().isdigit() and len(texto.strip()) <= 4:
                numero = int(texto.strip())
            repetido = contagem[_normaliza_margem(b)] >= minimo
            so_paginacao = (bool(RE_PAGINA_IMPRESSA.fullmatch(texto.strip())) or texto.strip().isdigit()
                            or bool(RE_PAGINA_DE.match(texto.strip())))
            if not (repetido or so_paginacao):
                corpo.append(b)
        limpas.append(corpo)
        impressas.append(numero)
    return limpas, impressas


# --- Montagem de parágrafos e trechos ---------------------------------------

def _termina_frase(linha: str) -> bool:
    return linha.endswith((".", ";", ":", "!", "?")) or linha.isupper()


def _paragrafos(blocos: list[Bloco]):
    """Divide blocos em parágrafos; uma linha com marcador abre parágrafo novo
    somente se a linha anterior encerrou frase (evita "...conforme subitem\\n8.5.2")."""
    for bloco in blocos:
        if bloco.tabela:
            yield bloco.linhas, bloco.confianca, True
            continue
        atual: list[str] = []
        for linha in bloco.linhas:
            if atual and _termina_frase(atual[-1]) and _marcador(linha):
                yield atual, bloco.confianca, False
                atual = []
            atual.append(linha)
        if atual:
            yield atual, bloco.confianca, False


def _juntar(linhas: list[str]) -> str:
    texto = ""
    for linha in linhas:
        if texto.endswith("-") and linha[:1].islower():
            texto = texto[:-1] + linha  # hifenização de quebra de linha
        elif texto:
            texto += " " + linha
        else:
            texto = linha
    return texto


def _titulo_anexo(marc: dict, par: list[str], proximo: list[str] | None) -> str:
    numero = marc["n"]
    titulo = marc["resto"] or " ".join(l for l in par[1:] if l.isupper())
    if not titulo and proximo and proximo[0].isupper():
        titulo = proximo[0]
    titulo = titulo.strip(" -–—:.")
    return f"Anexo {numero} — {_capitalizar(titulo)}" if titulo else f"Anexo {numero}"


def _capitalizar(titulo: str) -> str:
    minusculas = {"de", "da", "do", "das", "dos", "e", "a", "o", "para", "por", "em"}
    palavras = titulo.lower().split()
    return " ".join(
        p if i and p in minusculas else p[:1].upper() + p[1:] for i, p in enumerate(palavras)
    )


def _proximo_numero(num: str) -> str:
    partes = num.split(".")
    return ".".join(partes[:-1] + [str(int(partes[-1]) + 1)])


def _linha_de_tabela(num: str, seguintes: list) -> bool:
    """True se, logo adiante (pulando restos de célula sem marcador), vem uma tabela
    cuja 1ª célula é o número seguinte: "1.12 D27RMLL Cloud Pak" … "| 1.13 | …"."""
    for linhas, _conf, eh_tabela in seguintes:
        if eh_tabela:
            celula = linhas[0].strip("| ").split("|")[0].strip()
            return celula == _proximo_numero(num)
        if _marcador(linhas[0]):
            return False
    return False


def _citacao(t: Trecho) -> str:
    partes = [t.arquivo]
    if t.secao:
        partes.append(t.secao)
    if t.clausula:
        partes.append(f"cláusula {t.clausula}")
    if t.item:
        partes.append(f"item {t.item}")
    if t.inciso:
        partes.append(f"inciso {t.inciso}")
    if t.alinea:
        partes.append(f"alínea {t.alinea}")
    if not (t.secao or t.clausula or t.item):
        partes.append("preâmbulo")
    pagina = f"p. {t.pagina}"
    if t.pagina_impressa and t.pagina_impressa != t.pagina:
        pagina += f" (numerada {t.pagina_impressa})"
    partes.append(pagina)
    return "[" + ", ".join(partes) + "]"


def _tipo_documento(texto_inicial: str) -> str:
    t = _sem_acento(texto_inicial[:1500]).upper()
    if "ERRATA" in t:
        return "errata"
    if "ADENDO" in t:
        return "adendo"
    if "ESCLARECIMENTO" in t and "RESPOSTA" in t:
        return "resposta_esclarecimento"
    if "IMPUGNACAO" in t and ("DECISAO" in t or "RESPOSTA" in t):
        return "resposta_impugnacao"
    if "ESTUDO TECNICO PRELIMINAR" in t[:300]:  # título, não menção ao ETP
        return "etp"
    if "EDITAL" in t[:600]:
        return "edital"
    if "TERMO DE REFERENCIA" in t:
        return "termo_referencia"
    if "MINUTA" in t and "CONTRATO" in t:
        return "minuta_contrato"
    return "desconhecido"


def extrair(caminho: Path, ocr: str = "auto") -> tuple[Documento, list[Trecho]]:
    pdf = fitz.open(caminho)
    doc = Documento(
        arquivo=caminho.name,
        caminho=str(caminho),
        sha256=hashlib.sha256(caminho.read_bytes()).hexdigest(),
        paginas=pdf.page_count,
        tipo_documento="desconhecido",
    )
    motivo_sem_ocr = "desativado (--ocr nunca)" if ocr == "nunca" else _ocr_indisponivel()

    paginas_blocos: list[list[Bloco]] = []
    metodos: list[str] = []
    for i, pagina in enumerate(pdf, start=1):
        escaneada = _precisa_ocr(pagina)
        if (ocr == "sempre" or escaneada) and motivo_sem_ocr is None:
            paginas_blocos.append(_blocos_ocr(pagina))
            metodos.append("ocr")
            doc.paginas_ocr.append(i)
        else:
            paginas_blocos.append(_blocos_texto(pagina))
            metodos.append("texto")
            if escaneada:
                doc.paginas_sem_texto.append(i)
    if doc.paginas_sem_texto:
        doc.avisos.append(
            f"Páginas {doc.paginas_sem_texto} parecem escaneadas, mas o OCR não rodou: "
            f"{motivo_sem_ocr}. Conteúdo dessas páginas ausente."
        )
    if doc.paginas_ocr:
        doc.avisos.append(
            f"Páginas {doc.paginas_ocr} lidas por OCR: confira citações literais "
            "(números, datas, percentuais) no original."
        )

    paginas_blocos, impressas = _separar_margens(paginas_blocos)
    doc.tipo_documento = _tipo_documento(
        " ".join(l for b in (paginas_blocos[0] if paginas_blocos else []) for l in b.linhas)
    )

    estado = {"secao": None, "clausula": None, "item": None, "alinea": None, "inciso": None}
    trechos: list[Trecho] = []
    for n_pag, (blocos, metodo) in enumerate(zip(paginas_blocos, metodos), start=1):
        pars = list(_paragrafos(blocos))
        for idx, (par, conf, eh_tabela) in enumerate(pars):
            marc = None if eh_tabela else _marcador(par[0])
            if marc and marc["tipo"] == "item" and _linha_de_tabela(marc["n"], pars[idx + 1:idx + 4]):
                # Linha numerada que ficou fora da grade da tabela seguinte
                # ("1.6 Cloud Pak ... 8 36 meses" antes de "| 1.7 | ..."): é dado, não item.
                marc, eh_tabela = None, True
            if marc and marc["tipo"] == "anexo" and idx > 0:
                # Anexo só muda a seção quando abre a página; na lista de anexos do
                # edital ("ANEXO I – Termo de Referência") é apenas texto.
                marc = None
            if marc and marc["tipo"] == "anexo":
                proximo = pars[idx + 1][0] if idx + 1 < len(pars) else None
                estado = dict.fromkeys(estado)
                estado["secao"] = _titulo_anexo(marc, par, proximo)
            elif marc and marc["tipo"] == "clausula":
                estado.update(clausula=marc["n"], item=None, alinea=None, inciso=None)
            elif marc and marc["tipo"] == "item":
                estado.update(item=marc["n"], alinea=None, inciso=None)
            elif marc and marc["tipo"] == "inciso":
                estado.update(inciso=marc["n"], alinea=None)
            elif marc and marc["tipo"] == "alinea":
                estado["alinea"] = marc["n"]

            texto = "\n".join(par) if eh_tabela else _juntar(par)
            anterior = trechos[-1] if trechos else None
            mesma_posicao = anterior and all(
                getattr(anterior, k) == v for k, v in estado.items()
            ) and anterior.arquivo == doc.arquivo
            if not marc and mesma_posicao and anterior.pagina == n_pag:
                anterior.texto += "\n" + texto
                continue
            trechos.append(Trecho(
                arquivo=doc.arquivo,
                tipo_documento=doc.tipo_documento,
                pagina=n_pag,
                pagina_impressa=impressas[n_pag - 1],
                texto=texto,
                metodo=metodo,
                confianca_ocr=conf,
                continuacao=bool(not marc and mesma_posicao and anterior.pagina != n_pag),
                **estado,
            ))
    for t in trechos:
        t.citacao = _citacao(t)
    return doc, trechos


# --- Saídas -------------------------------------------------------------------

def indice(trechos: list[Trecho]) -> list[dict]:
    """Itens únicos com as páginas onde aparecem (útil para o Roteiro de Leitura)."""
    vistos: dict[tuple, dict] = {}
    for t in trechos:
        if not t.item and not t.clausula:
            continue
        chave = (t.arquivo, t.secao, t.clausula, t.item)
        e = vistos.setdefault(chave, {
            "arquivo": t.arquivo, "secao": t.secao, "clausula": t.clausula,
            "item": t.item, "paginas": [], "inicio": t.texto[:90],
        })
        if t.pagina not in e["paginas"]:
            e["paginas"].append(t.pagina)
    return list(vistos.values())


def para_json(docs: list[Documento], trechos: list[Trecho]) -> str:
    return json.dumps({
        "ferramenta": f"orbital/extrair_pdf.py {VERSAO}",
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "documentos": [asdict(d) for d in docs],
        "indice": indice(trechos),
        "trechos": [asdict(t) for t in trechos],
    }, ensure_ascii=False, indent=2)


def para_markdown(docs: list[Documento], trechos: list[Trecho]) -> str:
    saida = [f"<!-- orbital/extrair_pdf.py {VERSAO} · {datetime.now():%d/%m/%Y %H:%M} -->"]
    for d in docs:
        saida += [
            f"\n# {d.arquivo}",
            f"- Tipo: {d.tipo_documento} · Páginas: {d.paginas} · "
            f"OCR: {d.paginas_ocr or 'nenhuma'} · SHA-256: `{d.sha256[:16]}…`",
        ]
        saida += [f"- ⚠️ {a}" for a in d.avisos]
        pagina = None
        for t in (t for t in trechos if t.arquivo == d.arquivo):
            if t.pagina != pagina:
                pagina = t.pagina
                saida.append(f"\n## p. {pagina}" + (" (OCR)" if t.metodo == "ocr" else ""))
            conf = f" _(OCR {t.confianca_ocr:.0f}%)_" if t.confianca_ocr is not None else ""
            cont = " _(continuação)_" if t.continuacao else ""
            saida.append(f"\n`{t.citacao}`{cont}{conf}\n{t.texto}")
    return "\n".join(saida) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="+", type=Path, help="arquivos PDF (edital, TR, anexos, erratas...)")
    ap.add_argument("-f", "--formato", choices=["json", "md"], default="md")
    ap.add_argument("-o", "--saida", type=Path, help="arquivo de saída (padrão: stdout)")
    ap.add_argument("--ocr", choices=["auto", "sempre", "nunca"], default="auto",
                    help="auto = só páginas sem camada de texto (padrão)")
    args = ap.parse_args(argv)

    docs, trechos = [], []
    for caminho in args.pdfs:
        if not caminho.is_file():
            print(f"erro: arquivo não encontrado: {caminho}", file=sys.stderr)
            return 2
        d, t = extrair(caminho, args.ocr)
        docs.append(d)
        trechos.extend(t)
        itens = len({x.item for x in t if x.item})
        print(f"{d.arquivo}: {d.paginas} p., tipo={d.tipo_documento}, "
              f"OCR={d.paginas_ocr or '-'}, {len(t)} trechos, {itens} itens", file=sys.stderr)
        for a in d.avisos:
            print(f"  aviso: {a}", file=sys.stderr)

    conteudo = para_json(docs, trechos) if args.formato == "json" else para_markdown(docs, trechos)
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(conteudo, encoding="utf-8")
    else:
        sys.stdout.write(conteudo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
