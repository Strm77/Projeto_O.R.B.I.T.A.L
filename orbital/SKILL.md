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
0. Se os documentos forem PDF, extraia o texto com o script da skill antes de ler:

   ```bash
   python <dir-da-skill>/scripts/extrair_pdf.py edital.pdf tr.pdf errata*.pdf -f md -o extracao.md
   ```

   - Cada trecho sai com a citação pronta, ex.: `[edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 9]`.
     Use essas citações nas respostas (Regra 1); não recalcule páginas de memória.
   - Use `-f json` quando precisar filtrar por item/seção; o campo `indice` lista as
     páginas de cada item (itens que atravessam páginas: cite `p. 3–4`).
   - Páginas sem camada de texto passam por OCR (`por`). Trechos de OCR trazem
     `confianca_ocr`; números, datas e percentuais vindos de OCR devem ser marcados
     "(OCR — conferir no original)".
   - TR em **modelo AGU/CGU preenchido** (campos de percentual, prazo, alínea): no texto
     extraído esses valores saem fora de lugar ("de % ( por cento) 0,2 dois décimos…").
     Antes de citar número de item de modelo, confira na página (Read do PDF).
   - Se o script avisar que o OCR não rodou, informe ao usuário quais páginas ficaram
     sem conteúdo — nunca trate essas páginas como "não encontrado".
   - Dependências: `bash <dir-da-skill>/scripts/instalar_dependencias.sh` (Tesseract com
     português + pacotes Python).
1. Liste todos os documentos recebidos com: nome, tipo (edital, TR, ETP, anexo nº X,
   minuta de contrato, errata, adendo, resposta a esclarecimento, resposta a impugnação),
   data de publicação e nº de páginas.
2. Ordene por data. Documentos posteriores **alteram** os anteriores (ver Regra 3).
   Confira as datas: documento datado **depois de hoje**, errata anterior ao edital ou
   errata sem data são anomalias — sinalize no inventário e peça conferência no original
   (em documento escaneado, a data pode ser erro de OCR).
3. Registre documentos **citados mas não fornecidos** (ex.: "Anexo VII — Modelo de
   Proposta" referido no edital mas ausente). Peça ao usuário ou marque como lacuna.
   Se faltar um documento-base (**Edital**, **ETP**, **TR** ou a minuta), avise **no topo
   da resposta**, antes de qualquer análise, e diga quais perguntas ficam sem resposta
   por isso (ex.: sem Edital não há data, modo de disputa nem prazo de impugnação; sem ETP
   pode faltar a volumetria para precificar).
4. Se houver número de páginas ilegível/escaneado sem OCR, avise que citações de página
   podem ficar imprecisas.
5. **Fase do certame** — compare a data da sessão com hoje e diga no topo da resposta:
   - *pré-sessão*: fluxo completo, começando pelo Go/No-Go;
   - *pós-sessão* (sessão já passou): avise em destaque que a sessão e a impugnação
     já venceram (com as datas). O Go/No-Go vira histórico; priorize resultado,
     proposta ajustada, documentos, assinatura, riscos de execução e o que levar à
     reunião inicial;
   - *execução* (contrato assinado): foque em prazos de entrega, recebimento,
     pagamento, indicadores e sanções.
6. **Tipo de contratação** — classifique o objeto e, se houver guia em
   `references/tipos/`, leia-o antes do Passo 1 e use o banco de perguntas dele:

   | Tipo | Guia |
   |------|------|
   | Renovação/aquisição de licenças e subscrições de software | `references/tipos/licenciamento-software.md` |
   | Serviços de TI com equipe por demanda (projetos por OS), sustentação e/ou software como insumo | `references/tipos/servicos-ti-sob-demanda.md` |
   | Outros (service desk puro, nuvem, hardware, outsourcing de impressão) | ainda sem guia — use só as referências gerais |

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

Além de texto contra texto, procure inconsistências que só aparecem combinando itens:
- **Prazos encadeados:** obrigações da Contratante (entregar base, acessos, OS) que
  consomem o prazo da Contratada. Monte a linha do tempo da assinatura até a entrega.
- **Marco inicial:** o mesmo prazo contado de eventos diferentes (assinatura × OS × aceite).
- **Atestado × objeto:** quantitativo mínimo exigido em atestado dividido pelo
  quantitativo do objeto; acima de 50% é candidato a impugnação (art. 67, §2º [VERIFICAR]).
- **Horário cotado × horário exigido:** suporte ou sustentação cotados em 8x5 com
  atendimento 24x7, telefone 8x5, emergências fora do horário "sem acréscimo" —
  custo sem item para precificar. (Apareceu nos dois casos reais.)
- **Sanção × prazo contraditório:** multa calculada sobre um prazo que tem duas versões.
- **Mesma falha, várias penalidades:** o mesmo fato (ex.: atraso) no IMR, na tabela de
  sanções e na multa moratória; compare também a **base de cálculo** (OS, parcela,
  valor anual, valor total do contrato).
- **Aritmética dos valores:** mensal × 12 = anual? soma dos itens = total? percentuais
  derivados (PL de 10%, garantia de 5%) — refaça e rotule "calculado".
- **Teto × receita garantida:** item pago por demanda/alocação tem valor máximo, não
  receita certa.
- **Referência cruzada quebrada:** item ou anexo citado que não existe ou é o errado
  (ex.: "subitem 4.94 do TR"; POC que manda verificar o anexo de sustentação em vez do
  de software).
- **Resíduos de outro edital:** nome de outro órgão (ex.: "Correios"), lei revogada
  (8.666), ano antigo, exigência que não se aplica (garantia de proposta não exigida).
  Achou um, procure outros: indicam trechos copiados sem revisão. (Apareceu nos dois
  casos reais.)

### Passo 4 — Entregas iniciais
Leia `references/entregas.md` e produza, nesta ordem:
1. Go/No-Go
2. Ficha-Resumo
3. Roteiro de Leitura (ordenado por risco)
4. Calendário de Prazos

Acrescente ao final a tabela de **Contradições e Pedidos de Esclarecimento sugeridos**
(se houver) e a lista de **Lacunas** (documentos ou informações não encontrados).

Salve as entregas em um arquivo Markdown (ex.: `analise.md`) e gere a planilha de
trabalho a partir de um JSON com as listas de habilitação, requisitos, prazos e
Go/No-Go (formato: `python <dir-da-skill>/scripts/gerar_planilhas.py --exemplo`):

```bash
python <dir-da-skill>/scripts/gerar_planilhas.py analise.json -o planilhas.xlsx
```

Monte as fontes do JSON a partir das citações da extração (campo `citacao`), nunca
digitando páginas à mão.

### Passo 4b — Autoverificação (obrigatória antes de entregar)
1. Rode o verificador nas entregas e nas fontes da planilha:

   ```bash
   python <dir-da-skill>/scripts/verificar_citacoes.py analise.md edital.pdf errata*.pdf
   ```

   Ele confere arquivo, item, página e se cada transcrição entre aspas está no item e
   na página citados. **Zero ERRO** antes de entregar; AVISO de OCR vira "(OCR —
   conferir no original)".
2. O verificador não confere o que não é citação. Revise à mão:
   - **Contagens e somas** ("8 requisitos com POC", "R$ 218.400,00"): refaça a conta a
     partir da lista e rotule "calculado".
   - **Errata:** procure no texto cada valor superado (data/valor antigo) e confirme que
     só aparece como "superado"/"era ...", nunca como vigente.
   - **Contradições:** cada ❗ da Ficha e do Calendário tem linha na tabela de
     contradições, com as duas fontes.
3. Informe no início da resposta o resultado ("91 citações verificadas, 0 erros").

### Passo 5 — Perguntas de acompanhamento
Depois das entregas, responda perguntas pontuais seguindo as Regras de Resposta.
Quando chegar errata/adendo/esclarecimento novo, refaça os passos 0–4 apenas no que
mudou e destaque as alterações.

## Regras de resposta (obrigatórias)

### Regra 1 — Toda afirmação tem citação
Cada informação extraída cita documento, item e página **exatamente no formato gerado
pelo `extrair_pdf.py`** (nome do arquivo, anexo, cláusula, item, alínea, página):

> `[edital.pdf, item 8.3, alínea b, p. 3]`
> `[edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 7]`
> `[edital.pdf, Anexo IV — Minuta de Termo de Contrato, cláusula 7, item 7.1, p. 13]`
> `[errata_01.pdf, item 2, p. 1]`

- **Forma curta, com legenda:** `[TR, 4.8.1–4.8.3, p. 7–8]`, `[Edital, 6.5, 6.8, 6.11, p. 9–10]`,
  `[ETP, seções 8–10, p. 8–13]`, `[Minuta, cl. 4.1, p. 24]` são aceitas **desde que** a
  resposta comece com a legenda (`Abreviações: TR = tr.pdf · Minuta = edital.pdf, Anexo II`)
  e o verificador rode com os mesmos apelidos:
  `verificar_citacoes.py analise.md edital.pdf tr.pdf --alias TR=tr.pdf --alias "Minuta=edital.pdf:Anexo II"`.
  Sem legenda, abreviação é erro.
- Item que atravessa páginas: cite o intervalo (`p. 3–4`); citar só a primeira página
  falha quando o trecho transcrito está na segunda.
- Se o documento não tiver numeração de item, use a seção/cláusula/título mais próximo.
- Se não houver página (texto colado), use `p. n/d` e diga isso.
- Transcrição literal entre aspas quando o texto exato importar (prazos, percentuais,
  quantitativos, fórmulas de IMR, multas), **imediatamente antes** da citação:
  `"até 15 (quinze) dias corridos" [edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 7]`.
  Assim o verificador confere que o trecho está naquele item e página.
- Página lida por OCR: transcreva só o essencial (datas, números) e marque
  "(OCR — conferir no original)"; não corrija acentos do OCR dentro das aspas.

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

> ⚠️ **ALTERADO** — Texto vigente: "..." `[errata_01.pdf, item 1, p. 1]`
> Texto original (superado): "..." `[edital.pdf, preâmbulo, p. 1]`

- O valor vigente é o único usado em cálculos (prazos derivados, calendário, planilha).
  O superado aparece só ao lado do marcador ⚠️ ALTERADO ou como "era ...".

- Se a errata alterar conteúdo que afete a formulação de propostas, verifique se o
  prazo de publicidade foi reaberto e, se não, aponte como ponto de atenção.
  **Interpretação:** art. 55, §1º da Lei 14.133/2021 [VERIFICAR parágrafo].
- Se duas alterações conflitarem entre si, não escolha: aponte como contradição.

### Regra 4 — Contradições viram pedido de esclarecimento
Quando edital, TR, anexos ou minuta divergirem:

| # | Tema | Fonte A | Fonte B | Impacto | Sugestão de esclarecimento |
|---|------|---------|---------|---------|----------------------------|
| 1 | Prazo de implantação | "30 (trinta) dias corridos" `[edital.pdf, item 7.3, p. 3]` | "15 (quinze) dias corridos" `[edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 7]` | 🔴 multa por atraso | "Solicitamos esclarecer qual prazo prevalece..." |

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
| `references/tipos/*.md` | Passo 0.6: guia do tipo de contratação (estrutura, campos, perguntas, armadilhas) |

| Script (`scripts/`) | Quando usar |
|---------------------|-------------|
| `extrair_pdf.py` | Passo 0: PDF → trechos com citação pronta (OCR automático) |
| `gerar_planilhas.py` | Passo 4: planilha de habilitação, requisitos, prazos e Go/No-Go |
| `verificar_citacoes.py` | Passo 4b: confere citações e transcrições contra as páginas reais |
| `instalar_dependencias.sh` | Uma vez por máquina: Tesseract com português + pacotes Python |
