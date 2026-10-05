# Entregas iniciais

Quatro entregas, nesta ordem, ao final do fluxo de análise de um edital novo.
Todas em Markdown, com citações no formato `[Documento, item, p.]`.

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
| C2 | Quantitativo mínimo de atestado | Exige 60% do total (5.000 UST); empresa tem 2.800 | [Edital, 9.11.2, p. 21] | Sim — impugnação até 14/10/2026 (art. 67, §2º [VERIFICAR]) |

### Pontos de atenção (⚠️ / ❓)
| # | Critério | Situação | Citação |
|---|----------|----------|---------|

### Critérios atendidos (✅)
| # | Critério | Citação |
|---|----------|---------|

### Depende do perfil da empresa
- <dados que faltam para fechar o veredito>
```

Regras: impeditivos primeiro; se não houver nenhum, escrever "Nenhum impeditivo
identificado". Não esconder ✅ — a lista mostra o que foi verificado.

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
| 1 | 🔴 | TR, item 12 (IMR), p. 30–34 | Fórmula de glosa e teto | Glosa cumulativa com multa; teto ausente |
| 2 | 🔴 | Edital, 9.11 · TR, 15.3 | Quantitativos de atestado | ❗ Edital pede 50%, TR pede 60% |
| 3 | 🟡 | Minuta, cláusula 8 | Prazo de pagamento | 30 dias após aceite definitivo (aceite em até 90) |
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
| 09/10/2026 17:00 | sex | Fim do agendamento de vistoria | [TR, 6.2, p. 8] | Edital | 4 | Aberto | Agendar com fulano@órgão |
| 14/10/2026 23:59 | qua | Limite impugnação/esclarecimento | [Edital, 18.1, p. 30] | Edital | 6 | Aberto | Enviar pedidos #1 e #2 |
| 14/10/2026 | qua | Conferência: 3 dias úteis antes da abertura | art. 164, Lei 14.133 | Calculado | — | — | Conferir se bate com o edital |
| 19/10/2026 10:00 | seg | Abertura da sessão / limite de proposta | [Edital, preâmbulo, p. 1] ⚠️ ALTERADO por [Errata 1, item 1, p. 1] | Edital | 9 | Aberto | Proposta cadastrada até 18/10 |
| (convocação) + 2h | — | Envio de proposta ajustada e documentos | [Edital, 7.5, p. 12] | Relativo | — | — | Deixar documentos prontos |
| (resultado) + 3 d.u. | — | Razões de recurso | [Edital, 14.2, p. 26] · art. 165 | Relativo | — | — | — |
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
