# Go/No-Go — critérios eliminatórios

Executar **antes de qualquer outra análise** (Passo 1). Objetivo: descobrir em poucos
minutos se existe algo que impede a participação ou a torna inviável.

## Resultados possíveis

| Resultado | Significado | Efeito |
|-----------|-------------|--------|
| ✅ GO | Critério atendido, com citação | Segue |
| ⛔ NO-GO | Impedimento objetivo, com citação | Interrompe; reportar e perguntar se o usuário quer continuar a análise mesmo assim |
| ⚠️ ATENÇÃO | Risco relevante, ambiguidade, ou depende de informação do perfil da empresa | Segue, com alerta destacado |
| ❓ NÃO ENCONTRADO | Documento silente | Segue; vira candidato a pedido de esclarecimento |

Regras:
- Todo resultado leva citação `[Documento, item, p.]` — inclusive GO.
- NO-GO só com base em texto do edital + perfil da empresa. Nunca por inferência.
- Se o critério puder ser revertido por impugnação/esclarecimento ainda no prazo,
  registrar NO-GO **e** indicar "reversível — prazo de impugnação até dd/mm".
- Verifique erratas e respostas a esclarecimento antes de marcar NO-GO (Regra 3).

## Perfil da Empresa (input do usuário)

A avaliação depende destes dados. Se não estiverem disponíveis na conversa ou em
arquivo fornecido pelo usuário, pergunte apenas o que o edital efetivamente exige.

```
Razão social / CNPJ:
Porte: ME | EPP | Demais (faturamento último exercício: R$ ...)
Optante pelo Simples: sim | não
UF/cidades com presença física:
Atestados disponíveis: [objeto, órgão/cliente, quantitativo, período] ...
Certificações da empresa: ISO ..., CMMI/MPS.BR ...
Parcerias/credenciamentos de fabricante: ...
Profissionais e certificações: ...
Índices contábeis (último balanço): LG ..., SG ..., LC ...
Patrimônio líquido: R$ ...   Capital social: R$ ...
Garantias: capacidade de emitir seguro-garantia/fiança até R$ ...
Sanções vigentes (impedimento, inidoneidade, suspensão): sim | não
Certidões fiscais/trabalhistas regulares: sim | não (quais pendentes)
Recuperação judicial: sim | não
```

Se existir `<dir-da-skill>/perfil/parceiros/`, use-a para os campos de parcerias e
escopo (o que a empresa vende e o que está fora, como hardware). Campos `[A PREENCHER]`
da base contam como **não informados** — ver `references/parceiros.md`.

## Checklist eliminatório

Ordem sugerida: do mais rápido/objetivo ao mais analítico.

### A. Tempo
| # | Pergunta | Onde verificar | NO-GO quando |
|---|----------|----------------|--------------|
| A1 | A sessão/limite de proposta ainda não passou? | Preâmbulo; erratas (adiamento) | Data já passou e não há reabertura |
| A2 | Há tempo hábil para montar proposta, planilha e documentos? | Preâmbulo × hoje | Usuário declara que não consegue — senão ⚠️ se < 5 dias úteis |
| A3 | Vistoria **obrigatória** cujo prazo já venceu, sem declaração substitutiva? | Edital/TR — vistoria | Prazo vencido e vistoria obrigatória sem alternativa (Lei 14.133, art. 63, §§2º-3º) |
| A4 | POC/amostra com prazo de preparação inexequível para a empresa? | Anexo de POC | Usuário confirma que não consegue — senão ⚠️ |

### B. Elegibilidade
| # | Pergunta | Onde verificar | NO-GO quando |
|---|----------|----------------|--------------|
| B1 | Item/lote **exclusivo ME/EPP** e a empresa não é ME/EPP? | Tabela de itens | Exclusivo e empresa "Demais" (LC 123, art. 48, I) |
| B2 | Empresa tem sanção que impede participar neste órgão/esfera? | Seção de participação | Impedimento/inidoneidade abrangendo o órgão (Lei 14.133, arts. 14 e 156, §§4º-5º) |
| B3 | Consórcio é necessário para a empresa e o edital veda? | Seção de participação | Empresa só atende em consórcio e consórcio vedado (art. 15) |
| B4 | Empresa em recuperação judicial e o edital não admite / exige certidão negativa sem ressalva? | Habilitação econômica | ⚠️ por padrão — tema com jurisprudência [VERIFICAR] |
| B5 | Exigência de presença física local/regional que a empresa não tem e não consegue montar? | TR — local de execução | Usuário confirma inviabilidade |

### C. Habilitação técnica
| # | Pergunta | Onde verificar | NO-GO quando |
|---|----------|----------------|--------------|
| C1 | A empresa tem atestados que cobrem as **parcelas de maior relevância**? | Habilitação técnica | Não possui atestado compatível com alguma parcela exigida |
| C2 | Os **quantitativos mínimos** dos atestados são atingíveis (com soma, se permitida)? | Habilitação técnica | Quantitativo inatingível mesmo somando |
| C3 | Certificações da **empresa** exigidas como habilitação (ISO, CMMI, MPS.BR)? | Habilitação técnica | Exigida e empresa não tem (se for só pontuação → ⚠️) |
| C4 | Parceria/credenciamento/carta do fabricante exigida? | TR, habilitação | Exigida e empresa não obtém |
| C5 | Profissionais certificados exigidos na habilitação (não só na execução)? | Habilitação técnica | Não consegue indicar no prazo |
| C6 | Registro em conselho profissional exigido? | Habilitação técnica | Exigido e empresa não possui (avaliar impugnação se impertinente ao objeto) |

> Exigências acima do permitido em lei (ex.: quantitativo > 50% do objeto,
> parcela de maior relevância < 4% do valor) → marcar NO-GO "reversível" e sugerir
> impugnação. Base: Lei 14.133, art. 67, §§1º-2º [VERIFICAR].

### D. Habilitação econômico-financeira
| # | Pergunta | Onde verificar | NO-GO quando |
|---|----------|----------------|--------------|
| D1 | Índices contábeis exigidos são atendidos pelo último balanço? | Habilitação econômica | Índice abaixo e o edital não admite compensação por PL/capital |
| D2 | Capital social ou PL mínimo atendido? | Habilitação econômica | Abaixo do exigido |
| D3 | Balanço dos exercícios exigidos disponível? | Habilitação econômica | Empresa não possui (ex.: recém-constituída sem regra alternativa) |

### E. Habilitação jurídica e fiscal
| # | Pergunta | Onde verificar | NO-GO quando |
|---|----------|----------------|--------------|
| E1 | Objeto social compatível com o objeto da licitação? | Contrato social × objeto | Incompatível e sem tempo de alterar |
| E2 | Certidões fiscais/trabalhistas regularizáveis até a habilitação? | Habilitação fiscal | Débito não regularizável a tempo (ME/EPP: verificar prazo de regularização da LC 123, art. 43, §1º) |

### F. Economia do contrato
| # | Pergunta | Onde verificar | NO-GO quando |
|---|----------|----------------|--------------|
| F1 | Valor estimado (se não sigiloso) é compatível com o custo da empresa? | Planilha de preços | Usuário confirma inviabilidade — senão ⚠️ |
| F2 | Garantia de proposta/contratual cabe na capacidade de emissão? | Seção de garantias | Valor acima da capacidade |
| F3 | IMR/SLA, glosas e multas são compatíveis com a operação? | Anexo de IMR, minuta | ⚠️ por padrão (não é eliminatório objetivo, mas pode ser decisivo) |
| F4 | Prazo de pagamento/medição sustentável para o fluxo de caixa? | Minuta | ⚠️ por padrão |
| F5 | Reajuste ausente em contrato de longa duração? | Edital/minuta | ⚠️ e candidato a esclarecimento (Lei 14.133, art. 25, §7º — reajuste obrigatório no edital) |

## Veredito

- **NO-GO** — há ao menos um ⛔ não reversível.
- **NO-GO REVERSÍVEL** — há ⛔ que pode cair por impugnação/esclarecimento no prazo.
- **GO COM RESSALVAS** — sem ⛔, mas com ⚠️ ou ❓ relevantes.
- **GO** — tudo ✅.

O veredito é uma **recomendação**; a decisão é do usuário. Formato de saída em
`entregas.md` → Entrega 1.
