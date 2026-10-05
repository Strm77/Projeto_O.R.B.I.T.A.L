# O.R.B.I.T.A.L

Agent Skill pessoal (`orbital`) para analisar editais de licitação pública brasileira
regidos pela **Lei 14.133/2021** e pela **IN SEGES/ME 73/2022**, com foco em
contratações de TI. Uso pessoal — não é produto nem parecer jurídico.

## Estrutura

```
orbital/
├── SKILL.md                    # quando usar, fluxo de análise e regras de resposta
└── references/
    ├── go-no-go.md             # critérios eliminatórios (rodam primeiro)
    ├── campos-extracao.md      # campos a extrair do edital, TR e anexos
    └── entregas.md             # formato das 4 entregas iniciais
```

## Instalação (Claude Code)

```bash
# skill pessoal, disponível em qualquer projeto
ln -s "$(pwd)/orbital" ~/.claude/skills/orbital
```

Depois, basta enviar o edital (e TR, anexos, erratas) e pedir a análise.

## Entregas

1. **Go/No-Go** — impeditivos antes de tudo.
2. **Ficha-Resumo** — campos-chave com citação.
3. **Roteiro de Leitura** — o que ler primeiro, ordenado por risco.
4. **Calendário de Prazos** — datas do edital e prazos calculados.

## Pendências

Trechos marcados `[VERIFICAR]` são referências legais (artigo, parágrafo, valor)
que precisam ser conferidas no texto oficial:

```bash
grep -rn "\[VERIFICAR" orbital/
```
