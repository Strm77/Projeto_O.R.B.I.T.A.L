# Revisão do gabarito — MIDR, TR 7/2026 (serviços de dados)

Revisão **sem os PDFs**: confere coerência interna, contas e sintaxe das citações, não as
páginas. As 82 citações são reconhecidas pelo verificador (apelidos `TR` e `An. A` a
`An. K`). Para conferir as páginas, os 12 PDFs precisam vir para esta pasta.

## Contas

| Conta | Resultado |
|-------|-----------|
| Item 1: R$ 326.916,36 × 12 | R$ 3.922.996,32 — o gabarito (e provavelmente o TR) diz **R$ 3.922.996,30** (−R$ 0,02) |
| Item 2: R$ 142.965,15 × 12 | R$ 1.715.581,80 — o gabarito diz **R$ 1.715.581,75** (−R$ 0,05) |
| Item 3: R$ 113.951,23 × 12 | R$ 1.367.414,76 ✅ |
| Soma dos anuais | R$ 7.005.992,81 ✅ (mensal × 12 daria R$ 7.005.992,88) |
| PL de 10% do estimado | R$ 700.599,28 ✅ |
| HST: 17.092 ÷ 12 ÷ 141 | ≈ 10,1 profissionais ✅ (bate com os 10 do Item 1) |
| Atestado de 10.000 h/ano ÷ 17.092 HST/ano | 58,5% do estimado para o Item 1 |

## Pontos de revisão

| # | Ponto | Situação | Sugestão |
|---|-------|----------|----------|
| R1 | Valores anuais dos Itens 1 e 2 menores que mensal × 12 | 🟢 Diferença de centavos, mas o valor é **teto** (pergunta 2) | Acrescentar: quem cotar exatamente o teto mensal pode estourar o teto anual por centavos; cotar a partir do anual |
| R2 | Atestado de 10.000 horas/ano (pergunta 29) | ⚠️ Equivale a 58,5% das 17.092 HST/ano estimadas para o Item 1; com a sustentação (5 × 141 × 12 ≈ 8.460 h) cai para ~39% | **Interpretação:** se a base comparável for só projetos, passa do limite de 50% para quantitativo de atestado (art. 67, §2º [VERIFICAR]) — candidato a impugnação, se ainda houver prazo |
| R3 | Pergunta 24: cadeia de recebimento e pagamento | Fato correto | Acrescentar **Interpretação** de fluxo de caixa: relatório mensal → 5 + 10 dias → 10 + 10 dias úteis ≈ 6 semanas após o fim do mês, sem contar a possível dobra dos prazos |
| R4 | Pergunta 27 | ✅ Coerente: 0,07% × 25 dias = 1,75%, abaixo do teto de 2% antes do limite de extinção | — |
| R5 | Sem Go/No-Go e sem calendário | Esperado: sem Edital não há datas | Quando o Edital chegar: calendário e Go/No-Go |

## Padrões que este gabarito confirmou em relação ao caso BCB
- Horário cotado × exigido (BCB: 24x7 × telefone 8x5; MIDR: 8x5 × emergências sem acréscimo).
- Resíduos de outro edital (BCB: Lei 8.666, "4.94", 2025; MIDR: "Correios").
- Referência cruzada errada (BCB: item 4.94 inexistente; MIDR: POC no Anexo C × D).
- Cadeia longa até o pagamento (BCB e MIDR: provisório → definitivo → liquidação → pagamento).

Viraram regras gerais no SKILL.md (Passo 3). O que é específico deste tipo está em
`orbital/references/tipos/servicos-ti-sob-demanda.md`.
