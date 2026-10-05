# Revisão do gabarito — MIDR, TR 7/2026 (serviços de dados)

## Conferência contra os PDFs (05/10/2026)

- **12 PDFs:** TR (48 p.) e Anexos A a K. Edital e ETP continuam ausentes.
- **Páginas e itens:** 81 das 82 citações conferem (`tests/test_gabaritos.py`). A que
  não confere é de forma, não de conteúdo (ver R7).
- **Conteúdo:** as 30 respostas foram lidas contra o texto citado e conferem.
- **Numeração:** onde há número impresso, ele bate com a página do PDF. Os Anexos C, D,
  E, F, H e K não têm itens numerados nem número de página impresso: são texto corrido,
  e citar só a página (`[An. C, p. 5]`) é o certo.

## Contas

| Conta | Resultado |
|-------|-----------|
| TR 1.1: 12 × R$ 326.916,36 | R$ 3.922.996,32, mas a tabela do TR diz **R$ 3.922.996,30** (−R$ 0,02) |
| TR 1.1: 12 × R$ 142.965,15 | R$ 1.715.581,80, mas a tabela do TR diz **R$ 1.715.581,75** (−R$ 0,05) |
| Total | R$ 7.005.992,81 = soma dos anuais do TR ✅ (TR 11.1: "máximo aceitável") |
| PL de 10% | R$ 700.599,28 ✅ |
| HST (Anexo F, p. 10) | Total 17.092 ✅. A média "141,12" é a média simples das médias dos 9 perfis; como o desenvolvedor conta 2 pessoas, a média real é 17.092 ÷ 10 ÷ 12 = **142,4** HST/mês (🟢, a HST não fatura) |
| Atestado de 10.000 h/ano | 58,5% das HST do Item 1; ~39% se somada a sustentação |

## Pontos de revisão

| # | Ponto | Situação | Sugestão |
|---|-------|----------|----------|
| R1 | Valores anuais dos Itens 1 e 2 | 🟢 Inconsistência **do próprio TR**: 12 × valor unitário ≠ valor anual | Quem cotar o teto mensal estoura o teto anual por centavos; cotar a partir do anual |
| R2 | Atestado de 10.000 h/ano (pergunta 29) | ⚠️ O TR 10.30.1.2 admite **converter** outras unidades de fornecimento, se o contrato tiver a regra de conversão — o gabarito não diz | Acrescentar; e a **Interpretação** sobre o limite de 50% (art. 67, §2º [VERIFICAR]) depende da base |
| R3 | Pergunta 24 (recebimento e pagamento) | ✅ Confere; a liquidação é "prorrogável por igual período" (TR 8.29) | Acrescentar a prorrogação e a interpretação de fluxo de caixa (≈ 6 semanas após o fim do mês, até ≈ 10 se tudo dobrar) |
| R4 | Pergunta 12: "bancos legados Oracle 11gR2 e SQL Server 2000" | Incompleto: o Anexo D cita SQL Server **2000 a 2016**, MySQL 5.1/5.5 e PostgreSQL 8/9/11 | Listar a faixa toda |
| R5 | Pergunta 27 (multas) | ✅ Faixa de 2% a 10% confere | Ver N2: os campos do modelo saem embaralhados na extração; confirmar na página quais alíneas cada multa cobre |
| R6 | Contradição 4 (8x5) | ✅ TR 4.44 confirma 8 horas e 5 dias | — |
| R7 | Contradição 2: "No ETP" entre aspas `[An. D, p. 1]` | Forma: o texto diz "volumetria de referência estabelecida no Estudo Técnico Preliminar". Aspas só para transcrição literal | Escrever sem aspas ou transcrever o trecho |

## O que o gabarito não traz

| # | Achado | Fonte | Impacto |
|---|--------|-------|---------|
| N1 | A volumetria aparece em **três** lugares: o TR diz "estabelecida **neste instrumento**" (mas o TR não traz nenhum número), o Anexo D diz "no Estudo Técnico Preliminar" e o Anexo D (p. 2) e o Anexo K (p. 2) dizem "no Edital" | [TR, 3.5, p. 9] · [An. D, p. 1] · [An. D, p. 2] · [An. K, p. 2] | 🔴 Reforça a contradição nº 2: cada documento manda para um lugar diferente |
| N2 | O TR usa o modelo da AGU/CGU com campos preenchidos (percentuais, prazos, alíneas). Na extração de texto esses valores saem **fora de lugar** ("de % ( por cento) 0,2 dois décimos…"; "alíneas “ ” a “ ” … a e h") | [TR, 9.2.4, p. 38–39] · [TR, 4.44, p. 14] · [TR, 4.60, p. 16] | Leitura: em itens de modelo preenchido, conferir o número na página |
| N3 | A equipe de sustentação deve estar montada em até 30 dias corridos da abertura da OS | [An. C, p. 7] | 🟡 Prazo de mobilização que corre junto com a ambientação |

## O que este gabarito ensinou (incorporado à skill)
- Extração: caractere invisível antes do número do item, item depois de subtítulo em
  caixa normal, anexo que se intitula "ANEXO C"/"ANEXO I" (seção raiz do arquivo),
  negrito Markdown dentro de aspas na verificação.
- Guia `orbital/references/tipos/servicos-ti-sob-demanda.md`: volumetria com três
  remissões diferentes, tabela de valores com centavos inconsistentes, conversão de
  unidades no atestado, campos de modelo AGU/CGU.
