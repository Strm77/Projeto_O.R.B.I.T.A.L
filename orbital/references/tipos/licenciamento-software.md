# Tipo: renovação e aquisição de licenças/subscrições de software

Guia para editais cujo objeto é **renovar suporte/subscrição** e/ou **comprar licenças
novas** de um fabricante (IBM, Microsoft, Oracle, VMware, Red Hat etc.), com suporte
prestado pelo próprio fabricante e revendido por um parceiro.

> Base: 1 caso real analisado (BCB, PE 327/2026, licenças IBM, 36 meses — gabarito em
> `tests/gabaritos/bcb_pe_327_2026_ibm/`). Os padrões abaixo vêm desse caso; confirme
> em cada edital novo e, quando divergir, registre a diferença em vez de supor.

## 1. Como reconhecer

Use este guia quando aparecerem **três ou mais** destes sinais:
- objeto com "licenças", "subscrições", "renovação", "suporte e atualização", "S&S";
- tabela de subitens com **produto + métrica + quantidade** (VPC, PVU, núcleo, usuário,
  FETB, RU, instância);
- part numbers/SKU do fabricante;
- **indicação de marca** justificada no ETP (art. 41, I, Lei 14.133);
- data de **vencimento das subscrições atuais** e regra de início da nova cobertura;
- pagamento em **parcela única** após a entrega (ativação na conta do fabricante);
- **declaração de não ocorrência de registro de oportunidade** (deal registration).

## 2. Onde as coisas costumam estar

| Documento | Seções que importam neste tipo |
|-----------|-------------------------------|
| **Edital** | Capa (sessão, UASG, ME/EPP); preâmbulo; regras de disputa (modo, intervalo de lances); valor estimado (muitas vezes sigiloso); impugnação/esclarecimento; SICAF e prazos de documentos; inexequibilidade; assinatura do contrato; cláusula de prevalência; anexos-modelo (proposta, declarações); minuta de contrato |
| **TR** | 1 — tabela de subitens (renovação × nova), vigência; 3 — especificação: SKU, métricas, regras de cobertura e pró-rata, justificativa do item único; 4 — execução: suporte do fabricante, canais, SLA por severidade, segurança (CVE, MFA, termos), entrega e comprovação, marca, subcontratação, garantia, **declaração de registro de oportunidade**; 6 — etapas e cronograma de pagamento; 7 — gestão, preposto, reunião inicial; 8 — indicadores (IMR), recebimento, liquidação, pagamento, reajuste; 9 — sanções; 10 — habilitação; 11 — estimativa/sigilo |
| **ETP** | Inventário atual com **vencimentos**; cenários avaliados (renovar × trocar × consultoria × sem suporte × nuvem); quantitativos (memória de cálculo às vezes sigilosa); **sinais de redução de escopo** (substituição em outro pregão, redução progressiva) |
| **Minuta de contrato** | Objeto com a tabela de subitens; vedação de subcontratação; garantia; supressões (até 25%, art. 125 da Lei 14.133); preposto; sanções |

Os anexos-modelo citados (declaração de registro de oportunidade, ordem de
fornecimento, termo de sigilo, termo de ciência) **costumam não vir** com o pacote
principal: liste-os como lacuna.

## 3. Campos específicos deste tipo

Extraia **além** de `references/campos-extracao.md`:

| Campo | O que extrair |
|-------|---------------|
| Tabela de subitens | Para cada subitem: nº, produto, métrica, quantidade, **renovação ou nova** |
| Métricas | Definição de cada métrica no TR (ex.: FETB = volume de dados alvo do backup; VPC = núcleos) |
| Vencimento atual | Data em que vencem as subscrições em uso (ETP/TR) |
| Início da cobertura | Regra para renovação (dia seguinte ao vencimento? data da assinatura? até X dias após?) e para licenças novas |
| Fim da cobertura / cotação | Data-fim cotada (ex.: 30/09/2029) × vigência contada da assinatura |
| Pró-rata | Se há cobrança/pagamento proporcional por dia e sobre qual período |
| SKU | Obrigatório ou só referência? O que prevalece (SKU × descrição × data de cobertura) |
| Quem presta o suporte | Fabricante direto ou revenda; idioma; canais; horário; limite de chamados |
| SLA por severidade | Prazo de primeiro atendimento por severidade; regra de recontagem ao mudar severidade |
| Segurança | Aviso de CVE, acesso à conta do fabricante (MFA), termos de sigilo/ciência |
| Comprovação da entrega | Licenças visíveis na conta do órgão no portal do fabricante; declaração do fabricante como alternativa; checklist de aceite |
| Cadeia de pagamento | Etapas (ex.: D2), NF só após TRD, prazos de provisório → definitivo → liquidação → pagamento; correção por atraso |
| Data-base do reajuste | Data do orçamento × data prevista do pagamento único |
| Atestado | Quantidade mínima de licenças/subscrições; **de qualquer produto do fabricante ou só dos listados**; soma de atestados |
| Registro de oportunidade | Declaração exigida? Modelo (anexo)? Base normativa citada (ex.: Portaria SGD/MGI 5.950/2023 [VERIFICAR]) |
| Redução de escopo | Produto em substituição por outro certame; "redução progressiva"; supressões |
| Indicadores e penalidades | Cada indicador (ex.: IAE atraso, ICP chamados, IDS disponibilidade) com faixa e consequência; multa moratória separada |

## 4. Banco de perguntas (modelo em 30 perguntas)

Responda no formato da Entrega 5 (`references/entregas.md`). Pergunta sem resposta
nos documentos = "Não encontrado nos documentos analisados."

**Identificação e disputa**
1. Órgão, unidade, nº do pregão, UASG e processo.
2. Objeto, prazo, item único ou lotes — e a justificativa do agrupamento.
3. Data/hora da sessão (e se já passou).
4. Disputa: critério, modo, lance por total ou unitário, intervalo mínimo, tempos.
5. Valor estimado: público ou sigiloso; quando é divulgado; justificativa.
6. ME/EPP e margem de preferência; restrições ligadas ao Simples Nacional.
7. Consórcio, cooperativa, subcontratação.
8. Prazo e canal de impugnação e de esclarecimento (calcular a data-limite).
9. Indicação de marca: base no ETP e cenários avaliados.

**Escopo técnico**
10. Subitens de renovação (produto, métrica, quantidade).
11. Subitens de licenças novas.
12. Métricas de licenciamento e suas definições.
13. Início e fim da nova cobertura; pró-rata; vencimento das atuais.
14. SKU: obrigatório ou referência?
15. Quem presta o suporte e em que condições (idioma, canais, horário, chamados).
16. SLA de atendimento por severidade.
17. Exigências de segurança para o fornecedor.
18. Sinais de redução futura do escopo.

**Entrega, recebimento e pagamento**
19. Prazo de entrega e marco inicial (contrato vale como OS?).
20. Como a entrega é comprovada.
21. Cadeia de pagamento e prazos somados.
22. Reajuste: índice, data-base, se é automático ou a pedido.
23. Garantia contratual.
24. Validade mínima da proposta.

**Habilitação**
25. Qualificação técnica (atestados, declarações, equipe).
26. Qualificação econômico-financeira (índices, capital/PL, certidões).
27. SICAF: prazo de credenciamento e envio de documentos complementares.
28. Declarações especiais com a proposta (registro de oportunidade). 🔴
29. Prazos depois de vencer (proposta ajustada, assinatura, impedimentos).

**Riscos**
30. Multas, glosas e indicadores; critério de inexequibilidade.

Feche sempre com **Contradições** (com a cláusula de prevalência, se houver, e se ela
resolve ou não cada caso) e **Lacunas**.

## 5. Armadilhas típicas deste tipo (verificar sempre)

| Armadilha | Como aparece | Por que importa |
|-----------|--------------|-----------------|
| **Buraco de cobertura** | Subscrições vencem antes da assinatura possível (sessão no dia do vencimento, assinatura dias depois); TR manda cobrir "a partir do dia seguinte ao vencimento" e também "até 30 dias após a assinatura" | Quem paga o período retroativo? O fabricante pode cobrar reativação (conferir com o fabricante). 🔴 |
| **Cotação × vigência** | Cotação até data fixa (ex.: 30/09/2029) e vigência de 36 meses contados da assinatura | Datas finais diferentes; risco de cobrir menos ou mais do que o pago |
| **Fluxo de caixa** | Pagamento único só após TRD + liquidação (≈ 6–7 semanas após a entrega) | O fornecedor paga o fabricante/distribuidor antes de receber |
| **Registro de oportunidade** | Declaração de não ocorrência exigida com a proposta | Parceiro com deal registration na conta fica impedido ou exposto a declaração falsa 🔴 |
| **Mesmo atraso, duas penalidades** | Glosa de indicador de atraso + multa moratória diária | Custo do atraso maior do que parece; perguntar se cumulam |
| **Indicador definido duas vezes** | Faixas em dias numa tabela e em índice noutra | Glosa calculável de duas formas 🔴 |
| **Canais incoerentes** | Suporte 24x7 num item, telefone 8x5 noutro | Dúvida sobre o que precisa ser garantido |
| **Minuta genérica** | "Preposto no local da obra", Lei 8.666 citada, garantia de proposta mencionada sem exigência, item inexistente referido | Modelos reaproveitados: sinalizar como 🟢, mas checar se alguma cláusula muda obrigação |
| **Renomeação de produto** | Nome antigo e novo do mesmo produto (ex.: Spectrum Protect → Storage Protect); produto citado na métrica mas fora da tabela | Cotação do SKU errado |
| **Redução de escopo** | Produto em substituição por outro pregão; "redução progressiva"; supressão de até 25% | Receita futura menor; não contar com renovações |
| **Reajuste sem efeito** | Data-base no orçamento e pagamento único antes de completar 12 meses | Reajuste não se aplica na prática (interpretação) |
| **Valor sigiloso** | Estimado divulgado só após julgamento | Lances sem âncora; inexequibilidade relativa ao orçado (ex.: < 50%) |

## 6. Fase do certame

Este tipo costuma ser analisado **depois** da sessão (renovação urgente, sessão próxima do
vencimento). Se a sessão já passou, siga o modo acompanhamento do SKILL.md (Passo 0):
Go/No-Go deixa de ser a primeira entrega; priorize prazos pós-sessão (proposta ajustada,
documentos, assinatura), riscos de execução e o que levar à **reunião inicial**.
