# Entregas iniciais

Quatro entregas, nesta ordem, ao final do fluxo de análise de um edital novo.
Todas em Markdown, com citações no formato do `extrair_pdf.py`
(`[arquivo.pdf, Anexo …, item X, p. N]` — ver Regra 1 do SKILL.md).

Cabeçalho comum (uma vez, antes da Entrega 1):

```markdown
# O.R.B.I.T.A.L — <Modalidade> nº <número> — <Órgão>
Análise em: dd/mm/aaaa · Documentos considerados: Edital (dd/mm), TR (dd/mm),
Anexos I–VIII, Errata nº 1 (dd/mm), Resp. Esclarecimentos nº 1–3 (dd/mm)
Documentos citados e não fornecidos: Anexo VII (modelo de proposta)
```

Legenda usada em todas as entregas:
`✅ GO` · `⛔ NO-GO` · `⚠️ ATENÇÃO` · `❓ NÃO ENCONTRADO` · `⚠️ ALTERADO` (errata/esclarecimento) ·
`❗ CONTRADIÇÃO` · 🔴 risco alto · 🟡 médio · 🟢 baixo

---

## Entrega 1 — Go/No-Go

```markdown
## 1. Go/No-Go

**Veredito: GO COM RESSALVAS**
<1–3 linhas: motivo principal>

### Impeditivos (⛔)
| # | Critério | Situação | Citação | Reversível? |
|---|----------|----------|---------|-------------|
| C2 | Quantitativo mínimo de atestado | Exige 60% do total (5.000 UST); empresa tem 2.800 | `[edital.pdf, item 9.11.2, p. 21]` | Sim — impugnação até 14/10/2026 (art. 67, §2º [VERIFICAR]) |

### Pontos de atenção (⚠️ / ❓)
| # | Critério | Situação | Citação |
|---|----------|----------|---------|

### Critérios atendidos (✅)
| # | Critério | Citação |
|---|----------|---------|

### Condições do veredito
GO **se** os itens <n> do Checklist de Exigências forem confirmados internamente.
```

Regras: impeditivos primeiro; se não houver nenhum, escrever "Nenhum impeditivo
identificado". Não esconder ✅ — a lista mostra o que foi verificado.

---

## Entrega 1b — Checklist de Exigências (o que a empresa precisa ter)

Sempre na análise pré-sessão, logo depois do Go/No-Go. Responde: **"o que eu preciso
ter e entregar para participar e ganhar este certame?"**. Lista **todas** as exigências
do edital, TR e anexos (já com erratas aplicadas), não só as eliminatórias.

```markdown
## 1b. Checklist de Exigências

Legenda: 🔒 dado interno (confirmar com o time; a skill não recebe) · 📄 documento
público ou de emissão (certidão, SICAF, balanço publicado) · 🤝 depende do fabricante ·
✍️ declaração ou modelo do edital (preencher e assinar) · 💰 garantia ou custo.

### A. Com a proposta (até a abertura da sessão — dd/mm/aaaa hh:mm)
| # | O que precisa ter | Exigência (transcrita) | Fonte | Tipo | Responsável | Status |
|---|-------------------|------------------------|-------|------|-------------|--------|
| 1 | Proposta no modelo do Anexo III com marca, modelo, SKU e prazo de validade de 90 dias | "..." | [edital.pdf, item 4.3, p. 6] | ✍️ | Comercial | |

### B. Habilitação (quando o pregoeiro convocar — prazo: N horas)
Subgrupos na ordem do edital: **jurídica · fiscal, social e trabalhista ·
econômico-financeira · técnica**. Cada atestado, índice, certidão e declaração em linha
própria. Valores derivados calculados ("PL ≥ R$ 984.000,00 — calculado: 10% de
R$ 9.840.000,00").

### C. Depois da sessão (proposta ajustada, amostra/POC, diligências)
### D. Para assinar o contrato (garantia contratual, preposto, termos de sigilo)
### E. Durante a execução (certificações a manter, equipe mínima, seguros)

### Resumo
- N exigências · 🔒 x a confirmar internamente · 🤝 y dependem do fabricante · prazo mais curto: ...
- **Itens que eliminam** (sem eles a proposta é desclassificada ou a empresa inabilitada): #...
```

Regras:
- **Uma linha por exigência.** Nada de "documentos de habilitação conforme edital".
  Atestado com quantitativo, período e objeto exatos; índice com fórmula e valor mínimo;
  certidão com o órgão emissor.
- **Exigência transcrita** entre aspas, com citação verificável (Regra 1).
- **Status** fica vazio para o time preencher. A skill só preenche quando a informação
  for pública ou estiver na base de parceiros (ex.: nível de parceria → "✅ Gold
  (base de parceiros)").
- **Quando entregar** vem do edital; se o prazo for relativo ("2 horas após convocação"),
  diga isso.
- Inclua o que vem **de anexos-modelo** (declarações) e do **TR** (equipe, certificações,
  POC), não só da seção de habilitação do edital.
- Exigência ambígua ou contraditória → linha normal + ❗ e referência à tabela de
  contradições.
- A mesma lista alimenta a aba **Checklist Habilitação** da planilha.

---

## Entrega 2 — Ficha-Resumo

Uma tela. Só os campos-chave; o detalhamento completo fica na extração (Passo 2).

```markdown
## 2. Ficha-Resumo

| Campo | Valor | Citação |
|-------|-------|---------|
| Órgão | | |
| Certame / processo | | |
| Plataforma / UASG | | |
| Objeto (resumo) | | |
| Lotes/itens · adjudicação | | |
| SRP? | | |
| Valor estimado | R$ ... / Sigiloso | |
| Critério de julgamento | | |
| Modo de disputa · intervalo de lances | | |
| ME/EPP (exclusividade/cota) | | |
| Consórcio · Subcontratação | | |
| Sessão pública | dd/mm/aaaa hh:mm (dia) | |
| Impugnação / esclarecimento até | | |
| Vistoria | Obrigatória/Facultativa/Não prevista | |
| POC / amostra | | |
| Garantia de proposta · contratual | | |
| Vigência · prorrogação | | |
| Pagamento (forma · prazo) | | |
| Reajuste (índice · periodicidade) | | |
| IMR/SLA (resumo) | | |
| Multas (moratória · compensatória) | | |
| Habilitação técnica (resumo) | | |
| Habilitação econômica (índices · PL) | | |
```

Regras:
- Campo alterado por errata/esclarecimento: valor vigente + `⚠️ ALTERADO` + as duas
  citações (vigente e original).
- Campo ausente: `❓ Não encontrado` (nunca deixar vazio, nunca preencher com padrão).
- Campo com fontes divergentes: `❗ CONTRADIÇÃO — ver tabela` e as duas citações.

---

## Entrega 3 — Roteiro de Leitura (ordenado por risco)

Diz ao usuário **o que ler primeiro no original**, em vez de ler o edital do início ao fim.

### Critérios de classificação de risco

| Nível | Quando |
|-------|--------|
| 🔴 Alto | Pode desclassificar/inabilitar; gera multa/glosa relevante ou impede execução; contradição entre documentos em tema de preço, prazo, habilitação ou SLA; cláusula fora do padrão legal; item alterado por errata em tema crítico |
| 🟡 Médio | Afeta custo ou esforço de forma relevante mas contornável; ambiguidade sem contradição; exigência incomum porém lícita; prazos apertados |
| 🟢 Baixo | Cláusulas padrão; leitura de conferência |

Desempate dentro do mesmo nível: (1) o que tem prazo mais próximo; (2) o que afeta
habilitação/aceitação da proposta; (3) o que afeta preço.

```markdown
## 3. Roteiro de Leitura

| Ordem | Risco | Documento · item · páginas | O que verificar | Por quê |
|-------|-------|----------------------------|-----------------|---------|
| 1 | 🔴 | `[edital.pdf, Anexo I — Termo de Referência, item 12, p. 30–34]` (IMR) | Fórmula de glosa e teto | Glosa cumulativa com multa; teto ausente |
| 2 | 🔴 | `[edital.pdf, item 9.11, p. 20]` · `[edital.pdf, Anexo I — Termo de Referência, item 15.3, p. 41]` | Quantitativos de atestado | ❗ Edital pede 50%, TR pede 60% |
| 3 | 🟡 | `[edital.pdf, Anexo IV — Minuta de Termo de Contrato, cláusula 8, p. 52]` | Prazo de pagamento | 30 dias após aceite definitivo (aceite em até 90) |
| ... | 🟢 | Edital, 1–5 | Disposições gerais | Conferência |
```

Regras: cobrir todos os documentos (inclusive anexos); itens alterados por errata
sempre entram com a referência da errata; não incluir item sem citação.

---

## Entrega 4 — Calendário de Prazos

```markdown
## 4. Calendário de Prazos
Referência: hoje = dd/mm/aaaa (dia). Horário de Brasília.

| Data/hora | Dia | Evento | Fonte | Tipo | Dias úteis restantes | Status | Ação |
|-----------|-----|--------|-------|------|----------------------|--------|------|
| 09/10/2026 17:00 | sex | Fim do agendamento de vistoria | `[edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 8]` | Edital | 4 | Aberto | Agendar com fulano@órgão |
| 14/10/2026 23:59 | qua | Limite impugnação/esclarecimento | `[edital.pdf, item 18.1, p. 30]` | Edital | 6 | Aberto | Enviar pedidos #1 e #2 |
| 14/10/2026 | qua | Conferência: 3 dias úteis antes da abertura | art. 164, Lei 14.133 | Calculado | — | — | Conferir se bate com o edital |
| 19/10/2026 10:00 | seg | Abertura da sessão / limite de proposta | `[errata_01.pdf, item 1, p. 1]` ⚠️ ALTERADO (era `[edital.pdf, preâmbulo, p. 1]`) | Edital | 9 | Aberto | Proposta cadastrada até 18/10 |
| (convocação) + 2h | — | Envio de proposta ajustada e documentos | `[edital.pdf, item 7.5, p. 12]` | Relativo | — | — | Deixar documentos prontos |
| (resultado) + 3 d.u. | — | Razões de recurso | `[edital.pdf, item 14.2, p. 26]` · art. 165 | Relativo | — | — | — |
```

Regras:
- **Tipo**: `Edital` (data expressa nos documentos), `Calculado` (derivado por conta —
  mostrar a conta numa nota abaixo da tabela) ou `Relativo` (depende de evento
  futuro sem data, ex.: convocação do pregoeiro).
- Ordenar por data; eventos relativos ao final, na ordem em que ocorrem.
- **Status**: `Aberto`, `Vence hoje`, `Vencido`.
- Se a data calculada pela lei divergir da data do edital: `❗` e incluir na tabela
  de contradições (sugerir esclarecimento).
- Dias úteis: excluir sábados, domingos e feriados nacionais; feriados estaduais/
  municipais do local do órgão → `[VERIFICAR]`.
- Incluir prazos pós-sessão conhecidos: proposta ajustada, documentos de habilitação,
  POC, recurso, assinatura de contrato/ARP, garantia contratual, início da execução.

---

## Entrega 5 — Perguntas e Respostas (quando o tipo tiver banco de perguntas)

Formato de leitura rápida, usado quando há um guia do tipo em `references/tipos/`
(ex.: as 30 perguntas de `licenciamento-software.md`). Pode substituir a Ficha-Resumo
se o usuário pedir "as perguntas" ou quando a sessão já passou.

```markdown
Abreviações: Edital = edital.pdf (35 p.) · TR = tr.pdf (36 p.) · ETP = etp.pdf (17 p.) ·
Minuta = Edital, Anexo II (p. 22–30). Página do PDF = página impressa: sim/não.

⚠️ <aviso de fase, se houver: "A sessão foi em dd/mm (dia) e já passou; o prazo de
impugnação venceu em dd/mm (calculado). Este material serve para ...">
⚠️ <aviso de documento ausente, se houver: "O Edital e o ETP não estão entre os arquivos.
Por isso não há como responder sobre ...">

## Identificação e regras da disputa

1. <Pergunta>
<Resposta direta em 1–3 linhas, ou lista curta.>
📍 [Edital, 1.1–1.2, p. 4] · [TR, 1.1, p. 1]

Interpretação (não consta do edital): <se houver>
```

Regras:
- **Seções conforme o tipo** (ver o banco de perguntas do guia). Tabelas e listas
  numeradas dentro da resposta são bem-vindas para valores, SLA, indicadores e etapas.
- **Resposta antes da fonte.** Cada pergunta termina com a linha `📍` com todas as
  fontes; em listas, a fonte pode ir no fim de cada linha.
- **Legenda obrigatória** no topo, ligando cada abreviação a um arquivo (e anexo, se for
  o caso), com nº de páginas e se a página do PDF bate com a impressa. Sem a legenda o
  verificador não consegue conferir as citações curtas.
- Cálculos do analista em primeira pessoa e marcados: "pelo meu cálculo, 25/09/2026:
  contei 29/09, 28/09 e 25/09".
- Seções na ordem do banco de perguntas do tipo; feche com **Contradições** (tabela
  com Impacto 🔴/🟡/🟢), **Lacunas** e o que levar à reunião inicial / próximo marco.
- Uma interpretação nunca pode contradizer um fato de outra resposta (ex.: dizer
  "pagamento adiantado" quando outra resposta diz "após a entrega"). Releia as
  interpretações contra as respostas antes de entregar.

---

## Entrega 6 — Matriz de Aderência ao Portfólio (com base de parceiros)

Formato e regras em `references/parceiros.md`. Vai logo depois do Go/No-Go.

---

## Após as quatro entregas

```markdown
## Contradições e pedidos de esclarecimento sugeridos
| # | Tema | Fonte A | Fonte B | Impacto | Texto sugerido |
|---|------|---------|---------|---------|----------------|

## Lacunas
- Não encontrado: <campo> — procurado em <documentos/seções>
- Documento citado e não fornecido: <anexo>

## Próximos passos sugeridos
1. ...
```
