# O.R.B.I.T.A.L

Agent Skill pessoal (`orbital`) para analisar editais de licitação pública brasileira
regidos pela **Lei 14.133/2021** e pela **IN SEGES/ME 73/2022**, com foco em
contratações de TI. Uso pessoal — não é produto nem parecer jurídico.

## Estrutura

```
orbital/
├── SKILL.md                    # quando usar, fluxo de análise e regras de resposta
├── references/
│   ├── go-no-go.md             # critérios eliminatórios (rodam primeiro)
│   ├── campos-extracao.md      # campos a extrair do edital, TR e anexos
│   ├── entregas.md             # formato das entregas (inclui perguntas e respostas)
│   └── tipos/
│       ├── licenciamento-software.md  # guia: renovação/aquisição de licenças
│       └── servicos-ti-sob-demanda.md # guia: projetos por OS, sustentação, software como insumo
└── scripts/
    ├── extrair_pdf.py          # PDF → trechos com {arquivo, página, seção, item} + OCR
    ├── gerar_planilhas.py      # JSON da análise → .xlsx (habilitação, requisitos, prazos, Go/No-Go)
    ├── verificar_citacoes.py   # confere citações e transcrições contra as páginas reais
    ├── instalar_dependencias.sh # Tesseract + português + pip
    └── requirements.txt
tests/
├── test_extrair_pdf.py
├── fixtures/                   # edital fictício (15 p.) + errata escaneada + gerador
│   └── referencia/             # análise de referência (teste de regressão)
└── gabaritos/                  # análises reais revisadas, usadas para ensinar e avaliar a skill
```

## Instalação (Claude Code)

```bash
# skill pessoal, disponível em qualquer projeto
ln -s "$(pwd)/orbital" ~/.claude/skills/orbital
```

Depois, basta enviar o edital (e TR, anexos, erratas) e pedir a análise.

## Extração de PDF

```bash
# instala Tesseract + português e os pacotes Python (Linux apt/dnf/pacman ou macOS brew)
bash orbital/scripts/instalar_dependencias.sh

python orbital/scripts/extrair_pdf.py edital.pdf errata.pdf -f md -o extracao.md
python orbital/scripts/extrair_pdf.py edital.pdf -f json -o extracao.json
```

Cada trecho sai com a citação pronta: `[edital.pdf, Anexo I — Termo de Referência, item 6.2, p. 7]`.
Detecta páginas sem camada de texto e aplica OCR em português só nelas
(`--ocr sempre|nunca` para forçar). Remove cabeçalho/rodapé repetidos, mantém
tabelas como linhas `| a | b |` e marca itens que continuam na página seguinte.

## Planilha e verificação

```bash
python orbital/scripts/gerar_planilhas.py --exemplo > analise.json   # formato de entrada
python orbital/scripts/gerar_planilhas.py analise.json -o planilhas.xlsx
python orbital/scripts/verificar_citacoes.py analise.md edital.pdf errata.pdf
```

A planilha tem cabeçalho fixo, filtros, listas de validação e cores: status
(verde/amarelo/vermelho) e prazos com ≤ 3 dias em vermelho (≤ 7 em amarelo);
"dias restantes" é fórmula e se atualiza ao abrir. O verificador sai com código 1
se alguma citação não bater com o PDF (item, página ou trecho transcrito).

## Busca no PNCP

API pública de consulta do PNCP (sem chave; só biblioteca padrão do Python):

```bash
# pregões com proposta aberta até 31/10, filtrando o objeto
python orbital/scripts/pncp.py abertas --ate 31/10/2026 --modalidade pregao \
    --palavra dados --palavra "business intelligence" --palavra observabilidade -o oportunidades.md
# publicados no período (a API exige a modalidade; padrão: pregão)
python orbital/scripts/pncp.py publicadas --de 01/10/2026 --ate 05/10/2026 --uf DF
# inteligência de mercado: contratos vencendo, atas com adesão, planos anuais
python orbital/scripts/pncp.py contratos --de 01/01/2025 --ate 05/10/2026 --palavra "business intelligence"
python orbital/scripts/pncp.py atas --de 05/10/2026 --ate 05/10/2027 --palavra observabilidade
python orbital/scripts/pncp.py pca --de 01/09/2026 --ate 05/10/2026 --palavra "plataforma de dados"
# baixar edital, TR e anexos de uma contratação
python orbital/scripts/pncp.py arquivos 00394460000141-1-000123/2026 -o editais/caso/
```

Caminhos, parâmetros e campos conferidos no Swagger
(https://pncp.gov.br/api/consulta/swagger-ui/index.html) em 05/10/2026. Os testes usam
respostas simuladas. Falta a primeira execução contra a API real.

## Testes

```bash
pip install -r requirements-dev.txt
pytest
python tests/fixtures/gerar_fixtures.py   # regenera os PDFs fictícios
```

O edital fictício (AETI-VS, Pregão Eletrônico nº 90042/2026) tem, de propósito:
contradição de prazo de implantação entre edital (item 7.3, 30 dias da assinatura)
e TR (item 6.2, 15 dias da OS), e uma errata escaneada que adia a sessão de
20/10 para 03/11/2026 e o limite de impugnação de 15/10 para 28/10/2026.

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
