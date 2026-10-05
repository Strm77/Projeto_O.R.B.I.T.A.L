#!/usr/bin/env python3
"""Gera os PDFs fictícios usados nos testes do orbital.

    python tests/fixtures/gerar_fixtures.py

Saídas (nesta pasta):
- edital_pe_90042_2026.pdf     edital + Anexo I (TR) + Anexo II (requisitos técnicos)
                               + Anexo III (modelo de proposta) + Anexo IV (minuta)
                               + Anexo V (termo de confidencialidade)
- errata_01_digitalizada.pdf   errata nº 1, só imagem (simula documento escaneado)

Tudo é fictício: órgão, processo, valores e pessoas não existem.

Pontos propositais (são verificados nos testes):
- CONTRADIÇÃO: prazo de implantação — Edital item 7.3 diz 30 dias corridos da
  assinatura do contrato; TR item 6.2 diz 15 dias corridos do recebimento da OS.
- ERRATA nº 1: adia a sessão de 20/10/2026 para 03/11/2026 e, em consequência,
  o limite de impugnação/esclarecimento de 15/10/2026 para 28/10/2026.
- A lista de anexos do edital (item 15.1) cita "ANEXO I – ..." no meio da página:
  não pode ser confundida com o início do anexo.
- Item 8.5.2 do edital começa na p. 3 e termina na p. 4 (testa continuação).
  Se mudar o conteúdo antes dele, confira que a quebra continua ocorrendo.
"""

from __future__ import annotations

import io
from pathlib import Path

import pymupdf as fitz
from PIL import Image
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (
    PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

AQUI = Path(__file__).parent
rl_config.invariant = 1  # PDF idêntico a cada geração (sem data/ID aleatório)
ORGAO = "Agência Estadual de Tecnologia da Informação de Vale Serrano (AETI-VS)"
CERTAME = "Pregão Eletrônico nº 90042/2026"
PROCESSO = "Processo nº 4512.000318/2026-11"

base = getSampleStyleSheet()
S = {
    "titulo": ParagraphStyle("titulo", parent=base["Title"], fontSize=14, spaceAfter=6),
    "anexo": ParagraphStyle("anexo", parent=base["Heading1"], fontSize=13, alignment=TA_CENTER, spaceAfter=2),
    "h": ParagraphStyle("h", parent=base["Heading2"], fontSize=11, spaceBefore=10, spaceAfter=4),
    "p": ParagraphStyle("p", parent=base["BodyText"], fontSize=10.5, leading=15,
                        alignment=TA_JUSTIFY, spaceAfter=6),
    "a": ParagraphStyle("a", parent=base["BodyText"], fontSize=10.5, leading=15,
                        alignment=TA_JUSTIFY, leftIndent=18, spaceAfter=4),
    "c": ParagraphStyle("c", parent=base["BodyText"], fontSize=10, alignment=TA_CENTER),
    "cel": ParagraphStyle("cel", parent=base["BodyText"], fontSize=8.5, leading=10.5),
}


class CanvasNumerado(rl_canvas.Canvas):
    """Canvas que escreve cabeçalho e 'Página X de Y' (precisa do total)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._paginas = []

    def showPage(self):
        self._paginas.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._paginas)
        for estado in self._paginas:
            self.__dict__.update(estado)
            self._margens(total)
            super().showPage()
        super().save()

    def _margens(self, total):
        w, h = A4
        self.setFont("Helvetica", 8)
        self.drawString(2.2 * cm, h - 1.3 * cm, f"AETI-VS — {CERTAME} — {PROCESSO}")
        self.drawRightString(w - 2.2 * cm, h - 1.3 * cm, "DOCUMENTO FICTÍCIO — USO EXCLUSIVO EM TESTES")
        self.line(2.2 * cm, h - 1.45 * cm, w - 2.2 * cm, h - 1.45 * cm)
        self.drawCentredString(w / 2, 1.2 * cm, f"Página {self._pageNumber} de {total}")


def tabela(linhas, larguras):
    dados = [[Paragraph(c, S["cel"]) for c in linha] for linha in linhas]
    t = Table(dados, colWidths=[w * cm for w in larguras], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def montar(conteudo):
    """conteudo: lista de (tipo, valor). tipos: titulo, c, h, p, a, anexo, tab, quebra, esp."""
    fluxo = []
    for tipo, *val in conteudo:
        if tipo == "quebra":
            fluxo.append(PageBreak())
        elif tipo == "esp":
            fluxo.append(Spacer(1, val[0] * cm))
        elif tipo == "anexo":
            fluxo += [PageBreak(), Paragraph(val[0], S["anexo"]), Paragraph(val[1], S["anexo"]), Spacer(1, 0.3 * cm)]
        elif tipo == "tab":
            fluxo += [tabela(*val), Spacer(1, 0.3 * cm)]
        else:
            fluxo.append(Paragraph(val[0], S[tipo]))
    return fluxo


def gerar_pdf(destino: Path, conteudo, titulo: str):
    doc = SimpleDocTemplate(
        str(destino), pagesize=A4, title=titulo, author="orbital — fixture de teste",
        leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2.2 * cm, bottomMargin=2.0 * cm,
    )
    doc.build(montar(conteudo), canvasmaker=CanvasNumerado)


def digitalizar(origem: Path, destino: Path, dpi: int = 150):
    """Converte cada página em imagem levemente inclinada (simula scanner)."""
    src = fitz.open(origem)
    out = fitz.open()
    for pagina in src:
        pix = pagina.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
        img = Image.frombytes("L", (pix.width, pix.height), pix.samples)
        img = img.rotate(0.4, expand=False, fillcolor=255)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        nova = out.new_page(width=pagina.rect.width, height=pagina.rect.height)
        nova.insert_image(nova.rect, stream=buf.getvalue())
    out.save(destino, garbage=4, deflate=True)


# ----------------------------------------------------------------------------
# Conteúdo
# ----------------------------------------------------------------------------

EDITAL = [
    ("titulo", "EDITAL DE LICITAÇÃO"),
    ("c", f"<b>{CERTAME}</b> — {PROCESSO}"),
    ("c", f"{ORGAO} — UASG 999042"),
    ("esp", 0.4),
    ("p", "A Agência Estadual de Tecnologia da Informação de Vale Serrano, por intermédio do(a) "
          "Pregoeiro(a) designado(a) pela Portaria AETI-VS nº 77/2026, torna público que realizará "
          "licitação na modalidade PREGÃO, na forma ELETRÔNICA, com critério de julgamento MENOR PREÇO "
          "GLOBAL, nos termos da Lei nº 14.133, de 1º de abril de 2021, da Instrução Normativa SEGES/ME "
          "nº 73, de 30 de setembro de 2022, da Lei Complementar nº 123, de 14 de dezembro de 2006, e "
          "das demais normas aplicáveis, observadas as condições estabelecidas neste Edital e seus anexos."),
    ("p", "<b>Data da sessão pública:</b> 20/10/2026, às 10h00 (horário de Brasília).<br/>"
          "<b>Local:</b> Portal de Compras do Governo Federal — www.gov.br/compras.<br/>"
          "<b>Valor estimado da contratação:</b> R$ 2.184.000,00 (dois milhões, cento e oitenta e quatro mil reais)."),

    ("h", "1. DO OBJETO"),
    ("p", "1.1. O objeto da presente licitação é a contratação de solução de Service Desk em nuvem, "
          "na modalidade de software como serviço (SaaS), compreendendo subscrição de licenças para 300 "
          "(trezentos) agentes, implantação, migração de dados do sistema legado, treinamento e suporte "
          "técnico, pelo período de 30 (trinta) meses, conforme condições, quantidades e exigências "
          "estabelecidas neste Edital e no Termo de Referência (Anexo I)."),
    ("p", "1.2. A licitação será realizada em grupo único, formado por 4 (quatro) itens, conforme tabela "
          "constante do Termo de Referência, devendo o licitante oferecer proposta para todos os itens "
          "que o compõem."),
    ("p", "1.3. O critério de julgamento adotado será o menor preço global do grupo, observadas as "
          "exigências contidas neste Edital e seus anexos quanto às especificações do objeto."),

    ("h", "2. DA PARTICIPAÇÃO NA LICITAÇÃO"),
    ("p", "2.1. Poderão participar deste Pregão os interessados que estiverem previamente credenciados no "
          "Sistema de Cadastramento Unificado de Fornecedores — SICAF e no Sistema de Compras do Governo "
          "Federal."),
    ("p", "2.2. Será concedido tratamento favorecido para as microempresas e empresas de pequeno porte, "
          "nos limites previstos na Lei Complementar nº 123, de 2006. Considerando o valor estimado do "
          "grupo, não se aplica a exclusividade de participação de que trata o art. 48, inciso I, da "
          "referida Lei Complementar."),
    ("p", "2.3. Não poderão disputar esta licitação:"),
    ("a", "a) aquele que não atenda às condições deste Edital e seu(s) anexo(s);"),
    ("a", "b) pessoa física ou jurídica que se encontre, ao tempo da licitação, impossibilitada de "
          "participar da licitação em decorrência de sanção que lhe foi imposta;"),
    ("a", "c) sociedades cooperativas, em razão da natureza do objeto;"),
    ("a", "d) empresas reunidas em consórcio, considerando que o objeto não apresenta complexidade ou "
          "vulto que justifique a participação de consórcios, conforme justificativa no Estudo Técnico "
          "Preliminar."),
    ("p", "2.4. É vedada a subcontratação do núcleo do objeto (subscrição SaaS, implantação e suporte). "
          "Admite-se a subcontratação exclusivamente dos serviços de treinamento, limitada a 20% (vinte "
          "por cento) do valor do item correspondente, mediante prévia autorização da Contratante."),

    ("h", "3. DA APRESENTAÇÃO DA PROPOSTA E DOS DOCUMENTOS DE HABILITAÇÃO"),
    ("p", "3.1. Os licitantes encaminharão, exclusivamente por meio do sistema, proposta com a descrição "
          "do objeto ofertado e o preço, até a data e o horário estabelecidos para abertura da sessão "
          "pública."),
    ("p", "3.2. Os documentos de habilitação serão exigidos apenas do licitante vencedor, observado o "
          "disposto na Seção 8 deste Edital."),
    ("p", "3.3. O prazo de validade da proposta não será inferior a 90 (noventa) dias, a contar da data de "
          "sua apresentação."),
    ("p", "3.4. Na proposta deverão constar o preço mensal da subscrição por agente, o preço global da "
          "implantação e migração, o preço do treinamento e o preço total para 30 meses, conforme modelo "
          "do Anexo III."),

    ("h", "4. DA ABERTURA DA SESSÃO E DA FASE DE LANCES"),
    ("p", "4.1. A abertura da sessão pública ocorrerá na data, na hora e no local indicados no preâmbulo "
          "deste Edital."),
    ("p", "4.2. Será adotado para o envio de lances o modo de disputa ABERTO, em que os licitantes "
          "apresentarão lances públicos e sucessivos, com prorrogações."),
    ("p", "4.3. O intervalo mínimo de diferença de valores entre os lances, que incidirá tanto em relação "
          "aos lances intermediários quanto em relação ao lance que cobrir a melhor oferta, será de "
          "R$ 5.000,00 (cinco mil reais)."),
    ("p", "4.4. A etapa de envio de lances terá duração de 10 (dez) minutos e, após isso, será prorrogada "
          "automaticamente pelo sistema quando houver lance ofertado nos últimos 2 (dois) minutos do "
          "período de duração da sessão pública."),

    ("h", "5. DO JULGAMENTO DAS PROPOSTAS"),
    ("p", "5.1. Encerrada a etapa de lances, o pregoeiro verificará a aceitabilidade da proposta de menor "
          "preço quanto à adequação ao objeto e à compatibilidade do preço em relação ao valor estimado."),
    ("p", "5.2. Será desclassificada a proposta que permanecer acima do valor estimado após a negociação, "
          "ou que apresentar preço manifestamente inexequível."),
    ("p", "5.3. O licitante classificado em primeiro lugar deverá encaminhar a proposta ajustada ao último "
          "lance, no prazo de 2 (duas) horas, contado da convocação pelo pregoeiro no sistema."),
    ("p", "5.4. O licitante provisoriamente vencedor será submetido à Prova de Conceito (POC), nos termos "
          "do item 9 do Termo de Referência, cuja reprovação implicará a desclassificação da proposta."),

    ("h", "6. DO CRITÉRIO DE DESEMPATE"),
    ("p", "6.1. Será assegurado como critério de desempate preferência de contratação para as "
          "microempresas e empresas de pequeno porte, nos termos dos arts. 44 e 45 da Lei Complementar "
          "nº 123, de 2006, e, persistindo o empate, os critérios do art. 60 da Lei nº 14.133, de 2021."),

    ("h", "7. DOS PRAZOS DE EXECUÇÃO"),
    ("p", "7.1. A vigência do contrato será de 30 (trinta) meses, contados da data de sua assinatura, "
          "prorrogável na forma dos arts. 106 e 107 da Lei nº 14.133, de 2021."),
    ("p", "7.2. A Contratada deverá apresentar o Plano de Implantação em até 5 (cinco) dias úteis após a "
          "reunião inicial."),
    ("p", "7.3. O prazo para conclusão da implantação da solução, incluída a migração de dados, será de "
          "até 30 (trinta) dias corridos, contados da assinatura do contrato."),

    ("h", "8. DA HABILITAÇÃO"),
    ("p", "8.1. Para fins de habilitação, deverá o licitante comprovar os requisitos de habilitação "
          "jurídica, fiscal, social e trabalhista, econômico-financeira e técnica, na forma dos arts. 62 "
          "a 70 da Lei nº 14.133, de 2021."),
    ("p", "8.2. Habilitação jurídica: ato constitutivo, estatuto ou contrato social em vigor, devidamente "
          "registrado, cujo objeto social seja compatível com o objeto desta licitação."),
    ("p", "8.3. Regularidade fiscal, social e trabalhista:"),
    ("a", "a) inscrição no Cadastro Nacional de Pessoas Jurídicas (CNPJ);"),
    ("a", "b) prova de regularidade fiscal perante a Fazenda Nacional, mediante certidão conjunta "
          "RFB/PGFN;"),
    ("a", "c) prova de regularidade com o Fundo de Garantia do Tempo de Serviço (FGTS);"),
    ("a", "d) prova de inexistência de débitos inadimplidos perante a Justiça do Trabalho (CNDT);"),
    ("a", "e) prova de regularidade com a Fazenda Estadual e Municipal do domicílio ou sede do licitante."),
    ("p", "8.4. Qualificação econômico-financeira:"),
    ("p", "8.4.1. Certidão negativa de falência expedida pelo distribuidor da sede do licitante."),
    ("p", "8.4.2. Balanço patrimonial e demonstração do resultado do exercício dos 2 (dois) últimos "
          "exercícios sociais, comprovando índices de Liquidez Geral (LG), Solvência Geral (SG) e "
          "Liquidez Corrente (LC) superiores a 1 (um)."),
    ("p", "8.4.3. O licitante que apresentar resultado igual ou inferior a 1 (um) em qualquer dos índices "
          "deverá comprovar patrimônio líquido mínimo de 10% (dez por cento) do valor estimado da "
          "contratação."),
    ("p", "8.5. Qualificação técnica:"),
    ("p", "8.5.1. Comprovação de aptidão para o fornecimento de bens e serviços similares de complexidade "
          "tecnológica e operacional equivalente ou superior, mediante apresentação de atestado(s) "
          "fornecido(s) por pessoa jurídica de direito público ou privado."),
    ("p", "8.5.2. Para fins da comprovação de que trata o subitem anterior, consideram-se parcelas de maior "
          "relevância: (i) a prestação de serviço de solução de Service Desk em nuvem (SaaS) aderente às "
          "práticas ITIL, para no mínimo 150 (cento e cinquenta) agentes simultâneos, por período não "
          "inferior a 12 (doze) meses; e (ii) a migração de base histórica de chamados de, no mínimo, "
          "500.000 (quinhentos mil) registros a partir de sistema legado. Será admitido o somatório de "
          "atestados para atingir o quantitativo mínimo de agentes, desde que referentes a períodos "
          "concomitantes. Os atestados deverão conter a identificação do emitente, a descrição do objeto, "
          "o quantitativo de agentes, o período de execução e os dados de contato do responsável pela "
          "informação, podendo o pregoeiro realizar diligência para confirmação das informações, "
          "inclusive solicitando cópia do contrato que deu suporte ao atestado, notas fiscais ou outros "
          "documentos idôneos."),
    ("p", "8.5.3. Declaração do fabricante da solução SaaS ofertada, ou documento equivalente, comprovando "
          "que o licitante está autorizado a comercializar e prestar suporte à solução no Brasil."),
    ("p", "8.5.4. Declaração de que a solução ofertada armazena os dados da Contratante em data centers "
          "localizados em território nacional."),
    ("p", "8.6. Vistoria: é facultada aos licitantes a realização de vistoria técnica nas instalações da "
          "AETI-VS, nos termos do item 8 do Termo de Referência. A não realização da vistoria será suprida "
          "por declaração formal de pleno conhecimento das condições e peculiaridades da contratação."),

    ("h", "9. DOS RECURSOS"),
    ("p", "9.1. Qualquer licitante poderá, durante o prazo concedido na sessão pública, de forma imediata, "
          "manifestar sua intenção de recorrer, sob pena de preclusão."),
    ("p", "9.2. As razões do recurso deverão ser apresentadas no prazo de 3 (três) dias úteis, contado da "
          "data de intimação ou de lavratura da ata de habilitação ou inabilitação, nos termos do art. 165 "
          "da Lei nº 14.133, de 2021."),

    ("h", "10. DA IMPUGNAÇÃO AO EDITAL E DO PEDIDO DE ESCLARECIMENTO"),
    ("p", "10.1. Qualquer pessoa é parte legítima para impugnar este Edital por irregularidade na aplicação "
          "da Lei nº 14.133, de 2021, ou para solicitar esclarecimento sobre os seus termos, devendo "
          "protocolar o pedido até 3 (três) dias úteis antes da data da abertura do certame."),
    ("p", "10.2. Os pedidos de impugnação e de esclarecimento deverão ser enviados até as 23h59 do dia "
          "15/10/2026, exclusivamente para o endereço eletrônico licitacoes@aeti-vs.exemplo.br."),
    ("p", "10.3. A resposta à impugnação ou ao pedido de esclarecimento será divulgada em sítio eletrônico "
          "oficial no prazo de até 3 (três) dias úteis, limitado ao último dia útil anterior à data da "
          "abertura do certame."),
    ("p", "10.4. As respostas aos pedidos de esclarecimentos serão divulgadas no sistema e vincularão os "
          "participantes e a Administração."),

    ("h", "11. DA GARANTIA DE EXECUÇÃO"),
    ("p", "11.1. Será exigida garantia de execução do contrato, no percentual de 5% (cinco por cento) do "
          "valor contratual, a ser apresentada em até 10 (dez) dias úteis após a assinatura do contrato, "
          "em uma das modalidades previstas no art. 96 da Lei nº 14.133, de 2021."),
    ("p", "11.2. Não será exigida garantia de proposta."),

    ("h", "12. DAS INFRAÇÕES ADMINISTRATIVAS E SANÇÕES"),
    ("p", "12.1. Comete infração administrativa o licitante que, entre outras condutas previstas no art. "
          "155 da Lei nº 14.133, de 2021, deixar de entregar a documentação exigida, não mantiver a "
          "proposta, ou não assinar o contrato quando convocado dentro do prazo de validade da proposta."),
    ("p", "12.2. Pelas infrações cometidas na fase licitatória, poderá ser aplicada multa de 10% (dez por "
          "cento) sobre o valor estimado da contratação, sem prejuízo das demais sanções do art. 156 da "
          "Lei nº 14.133, de 2021."),
    ("p", "12.3. As sanções aplicáveis na fase de execução contratual constam da minuta de contrato "
          "(Anexo IV)."),

    ("h", "13. DO PAGAMENTO E DO REAJUSTE"),
    ("p", "13.1. O pagamento da subscrição será mensal, em até 30 (trinta) dias contados do atesto da nota "
          "fiscal, condicionado à apuração do Instrumento de Medição de Resultado (IMR) do Termo de "
          "Referência."),
    ("p", "13.2. O pagamento da implantação será realizado em parcela única, após o recebimento definitivo."),
    ("p", "13.3. Os preços serão reajustados, após o interregno mínimo de 12 (doze) meses contado da data "
          "do orçamento estimado, pela variação do Índice de Custos de Tecnologia da Informação (ICTI)."),

    ("h", "14. DAS DISPOSIÇÕES GERAIS"),
    ("p", "14.1. Os horários estabelecidos neste Edital observarão o horário de Brasília."),
    ("p", "14.2. O Edital e seus anexos estão disponíveis no Portal Nacional de Contratações Públicas "
          "(PNCP) e no endereço eletrônico www.aeti-vs.exemplo.br/licitacoes."),

    ("h", "15. DOS ANEXOS"),
    ("p", "15.1. Integram este Edital, para todos os fins e efeitos, os seguintes anexos:"),
    ("p", "ANEXO I – Termo de Referência;"),
    ("p", "ANEXO II – Requisitos Técnicos da Solução;"),
    ("p", "ANEXO III – Modelo de Proposta de Preços;"),
    ("p", "ANEXO IV – Minuta de Termo de Contrato;"),
    ("p", "ANEXO V – Termo de Confidencialidade da Informação."),
    ("esp", 0.6),
    ("c", "Vale Serrano, 01 de outubro de 2026."),
    ("c", "Helena Marques Duarte — Pregoeira (personagem fictícia)"),
]

TR = [
    ("anexo", "ANEXO I", "TERMO DE REFERÊNCIA"),
    ("h", "1. DO OBJETO"),
    ("p", "1.1. Contratação de solução de Service Desk em nuvem (SaaS), com subscrição para 300 agentes, "
          "implantação, migração de dados, treinamento e suporte técnico por 30 meses, conforme tabela abaixo."),
    ("tab", [["Item", "Descrição", "Unidade", "Qtd."],
             ["1", "Subscrição SaaS de Service Desk — agente nomeado", "agente/mês", "9.000"],
             ["2", "Implantação e migração de dados do sistema legado", "serviço", "1"],
             ["3", "Treinamento de agentes e administradores (turmas de até 20 pessoas)", "turma", "12"],
             ["4", "Suporte técnico especializado 8x5 durante a vigência", "mês", "30"]],
     [1.3, 9.5, 2.8, 2.0]),
    ("h", "2. DA JUSTIFICATIVA"),
    ("p", "2.1. O atual sistema de chamados da AETI-VS, instalado on-premises em 2014, encontra-se sem "
          "suporte do fabricante, não possui integração com os canais digitais de atendimento e não permite "
          "a extração de indicadores de nível de serviço exigidos pelo Comitê de Governança Digital."),
    ("p", "2.2. A adoção de modelo SaaS transfere ao fornecedor a responsabilidade pela infraestrutura, "
          "atualização e disponibilidade da plataforma, conforme detalhado no Estudo Técnico Preliminar."),
    ("h", "3. DA ESPECIFICAÇÃO DA SOLUÇÃO"),
    ("p", "3.1. A solução deverá atender integralmente aos requisitos técnicos constantes do Anexo II."),
    ("p", "3.2. A solução deverá ser acessível por navegador web e por aplicativo móvel, sem necessidade de "
          "instalação de componentes nas estações dos usuários finais."),
    ("p", "3.3. A Contratada deverá manter, durante toda a vigência, ambiente de homologação segregado do "
          "ambiente de produção, sem custo adicional."),
    ("h", "4. DO MODELO DE EXECUÇÃO"),
    ("p", "4.1. A execução será iniciada por reunião inicial, convocada pela Contratante em até 5 (cinco) "
          "dias úteis após a assinatura do contrato, na qual será entregue a Ordem de Serviço (OS) de "
          "implantação."),
    ("p", "4.2. A implantação compreende: configuração da plataforma, parametrização do catálogo de "
          "serviços, integração com o diretório corporativo (LDAP/Azure AD), integração com o e-mail "
          "institucional e migração da base histórica."),
    ("p", "4.3. A migração deverá contemplar no mínimo 820.000 (oitocentos e vinte mil) registros de "
          "chamados, com anexos, abertos entre 2014 e 2026, preservando datas, solicitantes e histórico de "
          "interações."),
    ("h", "5. DA EQUIPE TÉCNICA"),
    ("p", "5.1. A Contratada deverá indicar gerente de projeto com certificação PMP ou equivalente e "
          "especialista na solução com certificação emitida pelo fabricante, ambos dedicados durante a fase "
          "de implantação."),
    ("p", "5.2. As certificações dos profissionais serão exigidas na reunião inicial, não constituindo "
          "requisito de habilitação."),
    ("h", "6. DOS PRAZOS"),
    ("p", "6.1. A Contratada deverá apresentar o Plano de Implantação em até 5 (cinco) dias úteis após a "
          "reunião inicial."),
    ("p", "6.2. O prazo para conclusão da implantação da solução, incluída a migração de dados, será de até "
          "15 (quinze) dias corridos, contados do recebimento da Ordem de Serviço."),
    ("p", "6.3. O recebimento provisório ocorrerá em até 5 (cinco) dias úteis após a comunicação de "
          "conclusão da implantação, e o recebimento definitivo em até 15 (quinze) dias úteis após o "
          "provisório."),
    ("h", "7. DO INSTRUMENTO DE MEDIÇÃO DE RESULTADO (IMR)"),
    ("p", "7.1. A remuneração mensal da subscrição estará vinculada ao atendimento dos indicadores abaixo, "
          "aferidos mensalmente pela própria plataforma e validados pelo fiscal técnico."),
    ("tab", [["Indicador", "Meta", "Aferição", "Glosa por descumprimento"],
             ["IND-01 Disponibilidade da plataforma", "99,5% ao mês", "Monitoramento externo a cada 5 min",
              "1% da fatura mensal a cada 0,1 p.p. abaixo da meta"],
             ["IND-02 Tempo de resposta a incidente crítico (P1)", "30 minutos", "Registro no sistema de chamados",
              "0,5% da fatura por ocorrência"],
             ["IND-03 Tempo de solução de incidente crítico (P1)", "4 horas", "Registro no sistema de chamados",
              "1% da fatura por ocorrência"],
             ["IND-04 Tempo de solução de incidente não crítico (P2/P3)", "2 dias úteis", "Registro no sistema",
              "0,2% da fatura por ocorrência"]],
     [4.6, 2.4, 4.2, 4.4]),
    ("p", "7.2. As glosas do IMR serão limitadas a 20% (vinte por cento) do valor da fatura mensal. O "
          "descumprimento reiterado sujeitará a Contratada às sanções contratuais, sem prejuízo da glosa."),
    ("p", "7.3. Nos 2 (dois) primeiros meses após o recebimento definitivo, os indicadores serão apenas "
          "monitorados, sem aplicação de glosa (período de estabilização)."),
    ("h", "8. DA VISTORIA"),
    ("p", "8.1. A vistoria é facultativa e poderá ser agendada pelo telefone (00) 0000-0000 ou pelo e-mail "
          "infra@aeti-vs.exemplo.br, de segunda a sexta-feira, das 9h às 17h, até o último dia útil anterior "
          "à data da sessão pública."),
    ("h", "9. DA PROVA DE CONCEITO (POC)"),
    ("p", "9.1. O licitante provisoriamente classificado em primeiro lugar será convocado para realizar Prova "
          "de Conceito, com o objetivo de verificar a aderência da solução aos requisitos marcados como "
          "\"POC\" no Anexo II."),
    ("p", "9.2. A POC será iniciada em até 5 (cinco) dias úteis após a convocação e terá duração máxima de "
          "2 (dois) dias úteis, de forma remota, com acompanhamento de comissão técnica designada."),
    ("p", "9.3. Será reprovada a solução que deixar de atender a qualquer requisito marcado como \"POC\". "
          "Os custos de preparação e execução da POC correrão por conta do licitante."),
    ("h", "10. DO PAGAMENTO"),
    ("p", "10.1. O pagamento da subscrição será mensal e proporcional ao número de agentes efetivamente "
          "habilitados no mês, após a aplicação das glosas do IMR."),
    ("p", "10.2. O pagamento da implantação será realizado após o recebimento definitivo."),
    ("h", "11. DA PROTEÇÃO DE DADOS"),
    ("p", "11.1. A Contratada atuará como operadora de dados pessoais, nos termos da Lei nº 13.709, de 2018 "
          "(LGPD), devendo observar as instruções da Contratante e assinar Termo de Confidencialidade."),
    ("p", "11.2. Ao final do contrato, a Contratada deverá entregar a totalidade dos dados em formato aberto "
          "(CSV ou JSON) e eliminá-los de seus ambientes em até 30 (trinta) dias, mediante comprovação."),

    ("h", "12. DAS OBRIGAÇÕES DA CONTRATADA"),
    ("p", "12.1. Além das obrigações previstas no Edital e na minuta de contrato, a Contratada deverá:"),
    ("a", "a) executar o objeto em estrita conformidade com este Termo de Referência e com a proposta apresentada;"),
    ("a", "b) manter, durante toda a execução, as condições de habilitação e qualificação exigidas na licitação;"),
    ("a", "c) designar preposto com poderes para representá-la, informando nome, telefone e e-mail em até 5 (cinco) dias úteis após a assinatura do contrato;"),
    ("a", "d) comunicar à Contratante, com antecedência mínima de 15 (quinze) dias, qualquer alteração na plataforma que impacte funcionalidades em uso;"),
    ("a", "e) não utilizar os dados da Contratante para finalidade diversa da execução contratual, inclusive para treinamento de modelos de inteligência artificial;"),
    ("a", "f) disponibilizar relatório mensal de indicadores do IMR até o 5º (quinto) dia útil do mês subsequente;"),
    ("a", "g) responder por danos causados à Contratante ou a terceiros decorrentes de sua culpa ou dolo na execução do contrato;"),
    ("a", "h) manter equipe de suporte com conhecimento da configuração específica do ambiente da Contratante."),
    ("h", "13. DAS OBRIGAÇÕES DA CONTRATANTE"),
    ("p", "13.1. Caberá à Contratante: (i) fornecer as informações e acessos necessários à implantação; (ii) "
          "disponibilizar extração da base do sistema legado em até 10 (dez) dias úteis após a reunião inicial; "
          "(iii) designar fiscais técnico, administrativo e requisitante; e (iv) efetuar os pagamentos nas "
          "condições pactuadas."),
    ("h", "14. DA FISCALIZAÇÃO"),
    ("p", "14.1. A execução do contrato será acompanhada e fiscalizada por fiscais designados, nos termos do "
          "art. 117 da Lei nº 14.133, de 2021, que registrarão as ocorrências e determinarão o necessário à "
          "regularização das falhas observadas."),
    ("p", "14.2. O fiscal técnico validará mensalmente o relatório de indicadores do IMR e poderá solicitar "
          "à Contratada os registros brutos de monitoramento que deram origem aos valores apurados."),
    ("h", "15. DA TRANSIÇÃO CONTRATUAL"),
    ("p", "15.1. Nos 90 (noventa) dias que antecedem o término da vigência, a Contratada deverá apoiar a "
          "transição para nova solução ou novo fornecedor, mantendo a plataforma em funcionamento e "
          "fornecendo exportações completas sempre que solicitado."),
    ("p", "15.2. A Contratada deverá entregar documentação atualizada de todas as configurações, fluxos "
          "automatizados, integrações e catálogo de serviços, em formato editável."),
]

REQUISITOS = [
    ("anexo", "ANEXO II", "REQUISITOS TÉCNICOS DA SOLUÇÃO"),
    ("h", "1. DISPOSIÇÕES GERAIS"),
    ("p", "1.1. Os requisitos marcados como \"POC\" serão verificados na Prova de Conceito (item 9 do TR). "
          "Os demais serão verificados durante a implantação e o recebimento."),
    ("h", "2. REQUISITOS FUNCIONAIS"),
]
_RF = [
    ("Registrar chamados por portal web, e-mail, aplicativo móvel e chat, com numeração única.", True),
    ("Permitir catálogo de serviços hierárquico com no mínimo 3 níveis e formulários dinâmicos.", True),
    ("Classificar chamados em incidente, requisição, problema e mudança, aderente às práticas ITIL v4.", True),
    ("Calcular automaticamente prazos de SLA por prioridade, considerando calendário de feriados.", True),
    ("Escalonar automaticamente chamados com SLA em risco, notificando grupo e gestor.", False),
    ("Possuir base de conhecimento com versionamento, aprovação e busca textual.", False),
    ("Oferecer pesquisa de satisfação configurável ao encerramento do chamado.", False),
    ("Permitir automação de fluxos sem programação (low-code), com aprovações paralelas.", True),
    ("Gerar painéis e relatórios exportáveis em CSV e PDF, com agendamento de envio.", False),
    ("Disponibilizar API REST documentada para integração com sistemas da Contratante.", True),
]
_RNF = [
    ("Disponibilidade mínima de 99,5% ao mês, medida conforme IMR do Termo de Referência.", False),
    ("Armazenar os dados exclusivamente em data centers localizados no Brasil.", False),
    ("Possuir certificação ISO/IEC 27001 vigente para o ambiente de nuvem ofertado.", False),
    ("Autenticação única (SSO) via SAML 2.0 ou OpenID Connect, com suporte a MFA.", True),
    ("Criptografia de dados em trânsito (TLS 1.2 ou superior) e em repouso (AES-256).", False),
    ("Registro de trilha de auditoria de todas as ações de agentes e administradores por 5 anos.", False),
    ("Interface integralmente em português do Brasil, inclusive mensagens e ajuda.", True),
    ("Acessibilidade conforme eMAG, versão 3.1, no portal do usuário final.", False),
    ("Backup diário com retenção mínima de 30 dias e RPO de 24 horas.", False),
    ("Suportar no mínimo 400 agentes simultâneos sem degradação de desempenho.", False),
]
n = 1
for desc, poc in _RF:
    REQUISITOS.append(("p", f"2.{n}. [RF-{n:02d}] {desc}" + (" (POC)" if poc else "")))
    n += 1
REQUISITOS.append(("h", "3. REQUISITOS NÃO FUNCIONAIS"))
for i, (desc, poc) in enumerate(_RNF, start=1):
    REQUISITOS.append(("p", f"3.{i}. [RNF-{i:02d}] {desc}" + (" (POC)" if poc else "")))
REQUISITOS += [
    ("h", "4. REQUISITOS DE SUPORTE TÉCNICO"),
    ("p", "4.1. Atendimento em português, das 8h às 18h em dias úteis (8x5), por telefone, e-mail e portal."),
    ("p", "4.2. Incidentes críticos (P1) deverão ser atendidos em regime 24x7, independentemente do horário "
          "contratado para o suporte."),
    ("p", "4.3. Atualizações de versão da plataforma serão comunicadas com antecedência mínima de 15 dias "
          "e aplicadas primeiro no ambiente de homologação."),
]

PROPOSTA = [
    ("anexo", "ANEXO III", "MODELO DE PROPOSTA DE PREÇOS"),
    ("p", f"À {ORGAO}<br/>Ref.: {CERTAME}"),
    ("p", "Razão social: ____________________ CNPJ: ____________________<br/>"
          "Endereço: ____________________ Telefone/e-mail: ____________________"),
    ("tab", [["Item", "Descrição", "Unid.", "Qtd.", "Preço unit. (R$)", "Total (R$)"],
             ["1", "Subscrição SaaS — agente nomeado", "agente/mês", "9.000", "", ""],
             ["2", "Implantação e migração", "serviço", "1", "", ""],
             ["3", "Treinamento", "turma", "12", "", ""],
             ["4", "Suporte técnico 8x5", "mês", "30", "", ""],
             ["", "VALOR GLOBAL", "", "", "", ""]],
     [1.2, 6.0, 2.2, 1.6, 2.6, 2.4]),
    ("p", "Validade da proposta: ___ dias (mínimo de 90 dias). Declaramos que nos preços propostos estão "
          "incluídos todos os custos diretos e indiretos, tributos, encargos e demais despesas necessárias à "
          "execução do objeto."),
    ("p", "Local e data: ____________________  Assinatura do representante legal: ____________________"),
]

MINUTA = [
    ("anexo", "ANEXO IV", "MINUTA DE TERMO DE CONTRATO"),
    ("p", f"Contrato que entre si celebram a {ORGAO} e a empresa ____________________, "
          "para prestação de serviços de Service Desk em nuvem."),
    ("h", "CLÁUSULA PRIMEIRA – DO OBJETO"),
    ("p", "1.1. O objeto do presente contrato é a contratação de solução de Service Desk em nuvem (SaaS), "
          "nas condições estabelecidas no Termo de Referência."),
    ("h", "CLÁUSULA SEGUNDA – DA VIGÊNCIA"),
    ("p", "2.1. O prazo de vigência da contratação é de 30 (trinta) meses contados da assinatura, "
          "prorrogável na forma da Lei nº 14.133, de 2021."),
    ("h", "CLÁUSULA TERCEIRA – DO PREÇO"),
    ("p", "3.1. O valor total da contratação é de R$ ________ (________)."),
    ("h", "CLÁUSULA QUARTA – DO PAGAMENTO"),
    ("p", "4.1. O prazo para pagamento e demais condições estão no Termo de Referência."),
    ("h", "CLÁUSULA QUINTA – DO REAJUSTE"),
    ("p", "5.1. Os preços são fixos e irreajustáveis pelo prazo de 12 meses contado da data do orçamento "
          "estimado; após, serão reajustados pelo ICTI."),
    ("h", "CLÁUSULA SEXTA – DA GARANTIA DE EXECUÇÃO"),
    ("p", "6.1. A Contratada prestará garantia de 5% (cinco por cento) do valor do contrato, com validade "
          "de 90 (noventa) dias após o término da vigência contratual."),
    ("h", "CLÁUSULA SÉTIMA – DAS INFRAÇÕES E SANÇÕES ADMINISTRATIVAS"),
    ("p", "7.1. Pelo atraso injustificado na conclusão da implantação, será aplicada multa moratória de "
          "0,33% (trinta e três centésimos por cento) por dia de atraso, calculada sobre o valor do item 2, "
          "até o limite de 30 (trinta) dias."),
    ("p", "7.2. O atraso superior a 30 (trinta) dias configurará inexecução parcial, sujeitando a Contratada "
          "a multa compensatória de 10% (dez por cento) sobre o valor total do contrato e à possibilidade de "
          "extinção contratual."),
    ("p", "7.3. A aplicação das sanções não exclui a aplicação das glosas previstas no IMR do Termo de "
          "Referência."),
    ("h", "CLÁUSULA OITAVA – DA EXTINÇÃO CONTRATUAL"),
    ("p", "8.1. O contrato poderá ser extinto nas hipóteses do art. 137 da Lei nº 14.133, de 2021."),
    ("h", "CLÁUSULA NONA – DA PROTEÇÃO DE DADOS PESSOAIS"),
    ("p", "9.1. As partes deverão cumprir a Lei nº 13.709, de 2018 (LGPD), observando o disposto no item 11 "
          "do Termo de Referência e no Termo de Confidencialidade (Anexo V)."),
    ("h", "CLÁUSULA DÉCIMA – DO FORO"),
    ("p", "10.1. Fica eleito o foro da comarca de Vale Serrano para dirimir litígios decorrentes deste "
          "contrato."),
]

CONFIDENCIALIDADE = [
    ("anexo", "ANEXO V", "TERMO DE CONFIDENCIALIDADE DA INFORMAÇÃO"),
    ("p", f"A empresa ____________________, inscrita no CNPJ sob o nº ____________________, doravante "
          f"denominada RECEPTORA, e a {ORGAO}, doravante denominada AETI-VS, celebram o presente Termo de "
          "Confidencialidade, mediante as cláusulas a seguir."),
    ("h", "CLÁUSULA PRIMEIRA – DO OBJETO"),
    ("p", "1.1. Este Termo tem por objeto a proteção das informações sigilosas disponibilizadas pela AETI-VS "
          "em razão da execução do contrato de Service Desk em nuvem, incluindo dados pessoais de servidores "
          "e cidadãos registrados nos chamados."),
    ("h", "CLÁUSULA SEGUNDA – DAS INFORMAÇÕES SIGILOSAS"),
    ("p", "2.1. Consideram-se sigilosas todas as informações, em qualquer meio, a que a RECEPTORA tiver "
          "acesso, exceto aquelas que: a) sejam de domínio público; b) já estivessem em posse legítima da "
          "RECEPTORA; ou c) venham a ser reveladas por determinação judicial, hipótese em que a RECEPTORA "
          "deverá comunicar imediatamente a AETI-VS."),
    ("h", "CLÁUSULA TERCEIRA – DAS OBRIGAÇÕES"),
    ("p", "3.1. A RECEPTORA se obriga a: (i) utilizar as informações exclusivamente para a execução do "
          "contrato; (ii) restringir o acesso aos profissionais que delas necessitem; (iii) comunicar à "
          "AETI-VS, em até 24 (vinte e quatro) horas, qualquer incidente de segurança envolvendo as "
          "informações; e (iv) devolver ou eliminar as informações ao término do contrato."),
    ("h", "CLÁUSULA QUARTA – DA VIGÊNCIA"),
    ("p", "4.1. As obrigações deste Termo vigorarão durante a execução do contrato e por 5 (cinco) anos "
          "após o seu término."),
    ("h", "CLÁUSULA QUINTA – DAS PENALIDADES"),
    ("p", "5.1. O descumprimento deste Termo sujeitará a RECEPTORA às sanções previstas no contrato e na "
          "legislação, sem prejuízo da responsabilidade civil e penal."),
    ("esp", 0.8),
    ("p", "Local e data: ____________________"),
    ("p", "Assinatura do representante legal da RECEPTORA: ____________________"),
]

ERRATA = [
    ("titulo", "ERRATA Nº 01"),
    ("c", f"<b>{CERTAME}</b> — {PROCESSO}"),
    ("c", ORGAO),
    ("esp", 0.4),
    ("p", "A Pregoeira da AETI-VS torna pública a presente ERRATA ao Edital do Pregão Eletrônico nº "
          "90042/2026, publicado em 01/10/2026, nos seguintes termos:"),
    ("p", "1. ONDE SE LÊ, no preâmbulo do Edital: \"Data da sessão pública: 20/10/2026, às 10h00 (horário "
          "de Brasília)\"; LEIA-SE: \"Data da sessão pública: 03/11/2026, às 10h00 (horário de Brasília)\"."),
    ("p", "2. Em consequência, ONDE SE LÊ, no item 10.2 do Edital: \"até as 23h59 do dia 15/10/2026\"; "
          "LEIA-SE: \"até as 23h59 do dia 28/10/2026\"."),
    ("p", "3. A alteração decorre da necessidade de ajustes no ambiente da Prova de Conceito e não afeta a "
          "formulação das propostas. Permanecem inalteradas as demais disposições do Edital e de seus anexos."),
    ("esp", 0.8),
    ("c", "Vale Serrano, 07 de outubro de 2026."),
    ("c", "Helena Marques Duarte — Pregoeira (personagem fictícia)"),
]


def main():
    edital = AQUI / "edital_pe_90042_2026.pdf"
    gerar_pdf(edital, EDITAL + TR + REQUISITOS + PROPOSTA + MINUTA + CONFIDENCIALIDADE, f"Edital {CERTAME} (fictício)")

    errata_digital = AQUI / "_errata_01_digital.pdf"
    gerar_pdf(errata_digital, ERRATA, f"Errata 01 {CERTAME} (fictícia)")
    digitalizar(errata_digital, AQUI / "errata_01_digitalizada.pdf")
    errata_digital.unlink()

    for f in sorted(AQUI.glob("*.pdf")):
        print(f"{f.name}: {fitz.open(f).page_count} páginas")


if __name__ == "__main__":
    main()
