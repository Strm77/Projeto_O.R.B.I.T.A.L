---
name: orbital
description: Analisa editais de licitação pública brasileira regidos pela Lei 14.133/2021 (pregão, concorrência, dispensa eletrônica), com foco em contratações de TI. Use quando o usuário enviar ou mencionar edital, termo de referência (TR), ETP, anexos, minuta de contrato, errata, adendo, resposta a esclarecimento ou impugnação, ou perguntar se vale participar de uma licitação, quais os prazos, requisitos de habilitação, riscos, SLA/IMR, multas, POC ou vistoria de um certame.
---

# O.R.B.I.T.A.L — Análise de editais (Lei 14.133/2021)

Skill de uso pessoal para ler editais de licitação de TI do ponto de vista de **quem vai
participar** (licitante), e não do órgão.

## Quando usar

- O usuário anexou ou colou edital, TR, ETP, anexos, minuta de contrato, errata, adendo,
  ata de sessão ou resposta a pedido de esclarecimento/impugnação.
- Perguntas do tipo: "vale a pena participar?", "quais os prazos?", "o que preciso para
  habilitar?", "tem POC?", "qual a multa por atraso?", "o SLA é viável?".
- Comparar edital × TR × anexos, ou edital original × errata.

## Quando NÃO usar

- Redigir edital, ETP ou TR como se fosse o órgão (pode ajudar, mas fora do fluxo desta skill).
- Gestão de contrato já assinado (aditivos, reequilíbrio, fiscalização), salvo pedido explícito.
- Licitações regidas pela Lei 8.666/1993, Lei 10.520/2002 ou Lei 13.303/2016 (estatais):
  avisar que a base legal é outra e que as referências desta skill podem não se aplicar.
- Parecer jurídico formal: a skill organiza e aponta; não substitui advogado.

## Fluxo de análise de um edital novo

Siga os passos na ordem. Não pule o passo 1.

### Passo 0 — Inventário de documentos
1. Liste todos os documentos recebidos com: nome, tipo (edital, TR, ETP, anexo nº X,
   minuta de contrato, errata, adendo, resposta a esclarecimento, resposta a impugnação),
   data de publicação e nº de páginas.
2. Ordene por data. Documentos posteriores **alteram** os anteriores (ver Regra 3).
3. Registre documentos **citados mas não fornecidos** (ex.: "Anexo VII — Modelo de
   Proposta" referido no edital mas ausente). Peça ao usuário ou marque como lacuna.
4. Se houver número de páginas ilegível/escaneado sem OCR, avise que citações de página
   podem ficar imprecisas.

### Passo 1 — Go/No-Go (eliminatório)
Leia `references/go-no-go.md` e execute o checklist **antes de qualquer outra análise**.
- Se faltar o Perfil da Empresa, pergunte o mínimo necessário (porte, atestados,
  certificações, índices) ou rode com resultado "ATENÇÃO — depende do perfil".
- Qualquer item NO-GO: entregue o Go/No-Go e **pergunte** se o usuário quer seguir
  com o restante mesmo assim.

### Passo 2 — Extração de campos
Leia `references/campos-extracao.md` e preencha todos os campos. Campo sem previsão
nos documentos = "Não encontrado". Nunca preencha com o "padrão de mercado".

### Passo 3 — Varredura de contradições
Cruze, no mínimo: objeto, quantitativos, prazos de execução/entrega, SLA/IMR, valores,
exigências de habilitação técnica, forma de pagamento, garantia, vigência e sanções
entre edital, TR, anexos e minuta de contrato. Registre cada divergência (Regra 4).

### Passo 4 — Entregas iniciais
Leia `references/entregas.md` e produza, nesta ordem:
1. Go/No-Go
2. Ficha-Resumo
3. Roteiro de Leitura (ordenado por risco)
4. Calendário de Prazos

Acrescente ao final a tabela de **Contradições e Pedidos de Esclarecimento sugeridos**
(se houver) e a lista de **Lacunas** (documentos ou informações não encontrados).

### Passo 5 — Perguntas de acompanhamento
Depois das entregas, responda perguntas pontuais seguindo as Regras de Resposta.
Quando chegar errata/adendo/esclarecimento novo, refaça os passos 0–4 apenas no que
mudou e destaque as alterações.

## Regras de resposta (obrigatórias)

### Regra 1 — Toda afirmação tem citação
Cada informação extraída cita documento, item e página, no formato:

> `[Edital, item 8.3.1, p. 14]`
> `[TR, item 5.2, p. 7]` · `[Anexo II — Planilha, linha 12, p. 3]`
> `[Errata nº 1, item 2, p. 1]` · `[Resp. Esclarecimento nº 3, pergunta 2, p. 2]`

- Se o documento não tiver numeração de item, use a seção/cláusula/título mais próximo.
- Se não houver página (texto colado), use `p. n/d` e diga isso.
- Transcrição literal entre aspas quando o texto exato importar (prazos, percentuais,
  quantitativos, fórmulas de IMR, multas).

### Regra 2 — Não encontrado não é "provavelmente"
- Se a informação não está nos documentos: responda **"Não encontrado nos documentos
  analisados."** e liste onde procurou.
- Nunca apresente inferência, costume de mercado ou regra legal supletiva como se
  fosse texto do edital.
- Interpretação, opinião ou aplicação da lei vai em bloco separado, sempre rotulado:

> **Interpretação (não consta do edital):** ...

- Fundamento legal citado em interpretação segue a Regra 5.

### Regra 3 — Errata, adendo e esclarecimento prevalecem
- Hierarquia: o documento **mais recente** que trate do mesmo ponto prevalece sobre o
  texto original. Respostas a esclarecimento e impugnação vinculam a Administração e os
  licitantes, e integram o edital.
- Sempre que um dado tiver sido alterado, sinalize assim:

> ⚠️ **ALTERADO** — Texto vigente: "..." `[Errata nº 1, item 3, p. 1]`
> Texto original (superado): "..." `[Edital, item 6.1, p. 9]`

- Se a errata alterar conteúdo que afete a formulação de propostas, verifique se o
  prazo de publicidade foi reaberto e, se não, aponte como ponto de atenção.
  **Interpretação:** art. 55, §1º da Lei 14.133/2021 [VERIFICAR parágrafo].
- Se duas alterações conflitarem entre si, não escolha: aponte como contradição.

### Regra 4 — Contradições viram pedido de esclarecimento
Quando edital, TR, anexos ou minuta divergirem:

| # | Tema | Fonte A | Fonte B | Impacto | Sugestão de esclarecimento |
|---|------|---------|---------|---------|----------------------------|
| 1 | Prazo de entrega | "30 dias" `[Edital, 7.1, p. 10]` | "15 dias" `[TR, 9.2, p. 22]` | Alto — multa por atraso | "Solicitamos esclarecer qual prazo prevalece..." |

- Redija a pergunta de forma neutra, objetiva, citando os dois trechos.
- Informe o prazo-limite para envio: até 3 dias úteis antes da data de abertura do
  certame (art. 164, caput, Lei 14.133/2021), conforme datas do Calendário de Prazos.
- Se a contradição favorecer uma leitura restritiva à competição, sugira também
  avaliar **impugnação** (mesmo prazo, art. 164).
- Não decida qual fonte prevalece como fato. Se o próprio edital tiver cláusula de
  prevalência (ex.: "em caso de divergência, prevalece o edital"), cite-a.

### Regra 5 — Fundamento legal sem invenção
- Cite artigo de lei ou instrução normativa apenas quando tiver segurança.
- Em caso de dúvida sobre número de artigo, parágrafo, inciso ou valor atualizado,
  escreva `[VERIFICAR]` ao lado. Nunca invente numeração.
- Bases principais: Lei 14.133/2021; IN SEGES/ME 73/2022 (licitação eletrônica, menor
  preço/maior desconto); LC 123/2006 (ME/EPP). Para TIC: IN SGD/ME 94/2022 [VERIFICAR
  vigência/alterações]. Valores da Lei 14.133 são atualizados anualmente por decreto —
  sempre `[VERIFICAR valor vigente]`.

### Regra 6 — Datas e prazos
- Use datas absolutas (dd/mm/aaaa, hh:mm, fuso de Brasília) e o dia da semana.
- Prazos derivados (ex.: limite de impugnação calculado a partir da data da sessão) são
  **cálculo**, não texto do edital: rotule como "calculado" e mostre a conta.
- Considere feriados nacionais; feriados locais do órgão são `[VERIFICAR]`.
- Compare cada prazo com a data de hoje e indique se já venceu.

### Regra 7 — Tom e formato
- Português, direto, em tópicos e tabelas. Primeiro a resposta, depois o detalhe.
- Distinguir sempre: **Fato (com citação)** · **Não encontrado** · **Interpretação**.
- Riscos com nível: 🔴 Alto · 🟡 Médio · 🟢 Baixo (critérios em `references/entregas.md`).

## Referências

| Arquivo | Quando ler |
|---------|-----------|
| `references/go-no-go.md` | Passo 1, sempre antes de tudo |
| `references/campos-extracao.md` | Passo 2 e perguntas pontuais sobre campos |
| `references/entregas.md` | Passo 4 e quando o usuário pedir uma das entregas |
