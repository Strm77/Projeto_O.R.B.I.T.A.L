# Gabaritos

Análises de editais reais, feitas ou revisadas pelo usuário, usadas para ensinar e
avaliar a skill. Cada pasta é um caso:

| Pasta | Tipo | PDFs no repositório? |
|-------|------|----------------------|
| `bcb_pe_327_2026_ibm/` | Licenças/subscrições de software (IBM) | Sim — 89 citações conferidas (`tests/test_gabaritos.py`) |
| `midr_tr_7_2026_dados/` | Serviços de dados: projetos por OS, sustentação, software como insumo | Sim (TR + Anexos A–K) — 81 de 82 citações conferidas; Edital e ETP não fornecidos |

Arquivos de cada caso:
- `perguntas.md` — o gabarito (perguntas, respostas e localização);
- `notas_revisao.md` — inconsistências encontradas no gabarito e o que virou regra na skill.

## Quando os PDFs chegarem

1. Salve-os na pasta do caso (ex.: `edital.pdf`, `tr.pdf`, `etp.pdf`).
2. Confira as citações do gabarito contra as páginas reais:

   ```bash
   python orbital/scripts/verificar_citacoes.py tests/gabaritos/bcb_pe_327_2026_ibm/perguntas.md \
       tests/gabaritos/bcb_pe_327_2026_ibm/*.pdf \
       --alias Edital=edital.pdf --alias TR=tr.pdf --alias ETP=etp.pdf \
       --alias "Minuta=edital.pdf:Anexo II" --alias "Minuta de Contrato=edital.pdf:Anexo II"
   ```

3. Rode a skill no mesmo edital, sem mostrar o gabarito, e compare: quais das 30
   perguntas ela respondeu, com que fontes, e o que ela achou ou deixou de achar.
