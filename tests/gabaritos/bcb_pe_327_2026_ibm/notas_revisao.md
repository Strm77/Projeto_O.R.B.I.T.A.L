# Revisão do gabarito — BCB PE 327/2026 (licenças IBM)

## Conferência contra os PDFs (05/10/2026)

- **Páginas e itens:** as 89 citações conferem (`tests/test_gabaritos.py`), com
  `Minuta = edital.pdf, Anexo II`. Página do PDF = página impressa nos três arquivos.
- **Conteúdo:** as 30 respostas foram lidas contra o texto citado e conferem. Pontos
  em que a fonte citada é o item-pai e o detalhe está num subitem:

| Pergunta | Citado | Onde está o detalhe |
|----------|--------|---------------------|
| 4 (15 min + até 10 aleatórios; lance final até 10%) | Edital 6.11, p. 9–10 | Edital 6.11.1 e 6.11.2, p. 9–10 |
| 5 (divulgação após lances se acima do estimado) | TR 11.1, p. 34 | TR 11.1.1, p. 34 |
| 28 (Portaria) | "Portaria SGD 5.950/2023" | O TR diz "item 6.6. do Anexo I da Portaria nº 5.950/2023", sem "SGD" |

## Pontos de revisão

| # | Ponto | Situação | Sugestão |
|---|-------|----------|----------|
| R1 | Pergunta 22 diz "o pagamento é 100% **adiantado**" | ❗ Contradiz a pergunta 21: pagamento único **após** entrega, TRD e liquidação | A conclusão continua certa por outro motivo: o reajuste só vale após 21/05/2027 e "exclusivamente para as obrigações iniciadas e concluídas após a ocorrência da anualidade" (TR 8.40, p. 26) |
| R2 | Pergunta 8: "o edital não fixa prazo próprio" para esclarecimento | ✅ Confere: o Edital 12.1 só fixa prazo para impugnação; o 12.3 trata do canal dos dois | Acrescentar **Interpretação:** o art. 164 da Lei 14.133 dá o mesmo prazo aos dois |
| R3 | Onde fica a "Minuta de Contrato" | ✅ Resolvido: **Edital, Anexo II, p. 22–31** | Declarar na legenda e usar um só nome ("Minuta") |
| R4 | Atraso na entrega: glosa IAE + multa moratória | ⚠️ Confirmado, e é pior: o atraso aparece em **três** lugares — TR 8.1 (IAE, p. 20), TR 9.1 item 2 (IAE, p. 27–28) e TR 9.4.4.1 (moratória 0,5%/dia, p. 30) | Incluir como risco 🔴 de penalidade cumulada |
| R5 | Contradição nº 4 (início da cobertura) | ✅ Texto confere (TR 3.11, 4.34, 1.4) | Acrescentar a consequência: período sem cobertura e cotação até 30/09/2029 × vigência de 36 meses da assinatura |
| R6 | Pergunta 6: sem benefício ME/EPP | ✅ Capa: "TRATAMENTO FAVORECIDO ME/EPP/EQUIPARADAS NÃO"; Edital 5.7: o valor "ultrapassa os limites de enquadramento" do Simples | — |
| R7 | Formato das citações `[TR, 4.8.1–4.8.3, p. 7–8]` | ✅ Aceito pelo verificador com apelidos (`--alias`) | — |

## O que o gabarito não traz

| # | Achado | Fonte | Impacto |
|---|--------|-------|---------|
| N1 | A contradição nº 1 (IAE) também é de **severidade**: no TR 8.1, atraso acima de 60 dias gera glosa de 10% + multa de 2% sobre a OS; no TR 9.1, IAE acima de 1,00 gera "Multa de 10 (dez) % sobre o valor do Contrato e Glosa de 30 (trinta) % sobre o valor da OS" | [TR, 8.1, p. 20] · [TR, 9.1, item 2, p. 27–28] | 🔴 Penalidades de ordem de grandeza diferente para o mesmo atraso |
| N2 | Não prestar esclarecimentos sobre a execução: multa de 0,5% **do valor total do contrato** por dia útil, até 10 dias úteis; depois, multa de 10% do contrato | [TR, 9.1, item 1, p. 27] | 🔴 Penalidade alta por obrigação acessória; falta na pergunta 30 |
| N3 | Momento da divulgação do valor sigiloso difere: Edital e TR dizem "após o julgamento das propostas"; o ETP diz "após o encerramento do envio de lances" | [Edital, 3.2, p. 6] · [TR, 11.1, p. 34] · [ETP, seções 11 e 13, p. 13] | 🟢 Prevalece o Edital (13.9) |
| N4 | Anexo III (modelo de proposta) datado "de 2025" | [Edital, p. 32] | 🟢 Mais um resto de modelo antigo (soma-se à contradição nº 6) |

## O que este gabarito ensinou (incorporado à skill)
- Estrutura típica do edital de licenciamento: `orbital/references/tipos/licenciamento-software.md`.
- Formato de entrega em perguntas e respostas: `orbital/references/entregas.md`, Entrega 5.
- Modo acompanhamento quando a sessão já passou: SKILL.md, Passo 0.
- Extração de PDFs reais: número de item sozinho na linha, paginação "P á g i n a 4 | 35"
  e "2 de 17", cabeçalho repetido a 11% do topo, linhas de tabela fora da grade.
