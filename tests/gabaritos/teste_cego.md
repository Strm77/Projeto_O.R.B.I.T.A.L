# Teste cego — 05/10/2026

## Método

- Dois subagentes isolados, um por caso, receberam só os PDFs e a skill (`orbital/`).
  Não viram `perguntas.md`, `notas_revisao.md` nem este repositório.
- Pedido: análise completa pela skill (inventário, Go/No-Go, prazos, as 30 perguntas
  do guia do tipo, contradições, lacunas) e verificação das próprias citações.
- Depois, comparação pergunta por pergunta com o gabarito do usuário. Os guias de tipo
  tinham detalhes tirados dos próprios gabaritos (**vazamento**). Esses pontos foram
  descontados e, depois do teste, os guias foram generalizados.

Resultados: `bcb_pe_327_2026_ibm/teste_cego_resultado.md` e
`midr_tr_7_2026_dados/teste_cego_resultado.md` (as citações são conferidas por
`tests/test_gabaritos.py`).

## Placar

| Caso | Perguntas | Contradições do gabarito | Citações verificadas |
|------|-----------|--------------------------|----------------------|
| BCB, PE 327/2026 (licenças IBM) | 30/30 corretas | 6/6 | 355/355 OK |
| MIDR, TR 7/2026 (serviços de dados) | 28 corretas + 2 parciais | 6/6 | 392/392 OK |

As duas parciais do MIDR:
- **Q18 (processo):** faltaram a ISO/IEC 12207 e a Portaria 750.
- **Q19 (banco de dados):** faltaram a 3FN, o limite de 30 caracteres e a regra de BLOB.

O conteúdo está nos anexos, mas a resposta resumiu demais.

## Achados que o gabarito não tinha

Cada afirmação nova foi conferida no PDF. Todas estavam corretas.

**BCB**

- **Orçamento:** estimado em ≈ R$ 9,84 mi a partir do capital mínimo exigido (o valor é
  sigiloso). A conta é rotulada como interpretação.
- **Preços máximos:** sigilosos (até quando e como são divulgados).
- **Nota fiscal:** conflito entre 6.1 e 6.1.3.
- **ICP:** medido em dias num ponto e em horas noutro.
- **IDS:** inconsistência no indicador.
- **Simples Nacional:** regra pouco clara.
- **TR 4.5:** ambíguo.
- **Referência quebrada:** remissão ao item 6.4.1.2.
- **Declaração falsa:** multa de 15% a 30%.

**MIDR**

- **Anexo I incompleto:** o PDF tem 22 páginas, e a numeração impressa diz 25.
- **Itens conflitantes:**
  - 10.23 × 10.24;
  - compartilhamento de profissionais: TR 3.7 × Anexo B.
- **Itens sem regra:**
  - base de cálculo do desconto do Item 1 não definida;
  - IDP, IQD e IDS citados sem item que os defina.
- **Resíduos de outro edital:** Ministério da Cidadania, "XX/XX/2019", FDA/GxP, ARP,
  VMware × Nutanix, IST copiado.
- **Valores:**
  - garantia de R$ 350.299,64;
  - reajuste a partir de 01/03/2027.

## Descontado por vazamento dos guias

| Caso | Ponto que o guia já entregava |
|------|-------------------------------|
| BCB | Penalidade tripla do atraso (TR 8.1, 9.1, 9.4.4.1) · minuta no Edital, Anexo II · renomeação de produto · fim da cotação em 30/09/2029 × 36 meses da assinatura |
| MIDR | Volumetria remetida a três lugares · centavos acima do teto · média de média nas HST · conversão de unidades no atestado · legado SQL Server 2000 · POC verificando anexos diferentes (10.46 × 10.48) **em parte** |

Mesmo sem esses pontos, as 30 perguntas e as 6 contradições de cada caso foram
respondidas a partir do texto citado.

## Atritos relatados e o que mudou

| Atrito | Correção |
|--------|----------|
| Linhas de sumário ("CLÁUSULA NONA ...... 22") viravam cláusula em centenas de trechos | `extrair_pdf.py`: `RE_SUMARIO` |
| "1. CLÁUSULA PRIMEIRA" não era reconhecida | `_marcador` aceita a cláusula numerada |
| Páginas faltando passavam sem aviso | `_total_impresso`: aviso quando a numeração impressa passa do total do PDF |
| Hífen de quebra de linha reprovava transcrição | `verificar_citacoes._contem` tolera hífen |
| "Anexo C" no nome da seção não casava | `_anexo` aceita letra |
| Texto embaralhado (campos de modelo AGU/CGU) | SKILL.md: renderizar a página e transcrever da imagem, não do `extracao.md` |
| Anexo com dois nomes (letra no TR e número no arquivo) | SKILL.md: tabela de correspondência no inventário |
| Certame já em curso (sessão passada, contrato não assinado) | SKILL.md: fase *indeterminada*; entregas por situação; prazo vencido vira pauta (chat, ofício ou reunião inicial) |
| Prazo em dias corridos vencendo no fim de semana | SKILL.md, regra 6: segue o edital; se omisso, mostrar as duas datas com [VERIFICAR] |
| Planilha gerada sem pedido | Só quando o usuário pede ou na análise pré-sessão; nos outros casos, oferecer |
| Guias com detalhes dos gabaritos | "Base:" e exemplos generalizados |
