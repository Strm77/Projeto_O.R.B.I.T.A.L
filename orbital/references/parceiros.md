# Base de parceiros (fabricantes) — como usar

A empresa do usuário revende ou implanta produtos de fabricantes parceiros. A base de
parceiros descreve esses produtos e diz o que está no escopo da empresa. Ela serve para
responder **"conseguimos atender este edital? com qual parceiro e produto?"**.

## Onde fica

`<dir-da-skill>/perfil/parceiros/`. A pasta fica **fora do git** (`.gitignore`) porque traz
estratégia comercial. Se ela não existir, diga ao usuário que a análise de aderência
precisa da base e siga sem ela.

- **Arquivos:**
  - `00_INDICE_*.md` — regra de escopo, matriz capacidade × parceiro, conflitos de
    portfólio, glossário "termo do edital → documento" e cuidados comuns;
  - `NN_<PARCEIRO>.md` — um documento por fabricante: produtos, licenciamento, mapa
    "requisito → produto" e pontos de atenção.
- **Frontmatter:** cada arquivo tem `data_referencia`. Se ela tiver **mais de 90 dias**,
  avise no topo da matriz que a base pode estar desatualizada (lançamentos, preços,
  regiões, aquisições).

## Leitura

1. Leia o **índice** inteiro.
2. Abra o documento do parceiro só quando um requisito do edital casar com ele. Use o
   glossário do índice para casar os termos ("créditos", "PVU", "Host Units", "F64",
   "por host").

## Regras

1. **A base não é o edital.** O que vem da base nunca vira fato do certame. Na resposta,
   fica separado e rotulado:

   > **Aderência ao portfólio (base de parceiros, ref. dd/mm/aaaa — não consta do edital):** ...

2. **Cite a base pelo documento e pela seção:** `[base: 01_SNOWFLAKE, "Pontos de atenção", 1]`.
   - Sem número de página: o verificador não confere essas citações. Releia a seção
     antes de afirmar.
   - Toda linha da matriz tem duas fontes: o **requisito**, citado do edital no formato
     da Regra 1, e o **produto**, citado da base.
3. **Status de atendimento:**
   - ✅ atende diretamente;
   - 🔸 atende em parte (explique o que falta);
   - ❌ não atende;
   - ❓ a base não diz.
   Nunca suba 🔸 para ✅ por "costuma atender".
4. **Escopo da empresa** (regra do índice):
   - **hardware fora de escopo**: lote que mistura hardware e software → avaliar
     consórcio, subcontratação permitida pelo edital ou não participar;
   - software fora do núcleo → "confirmar unidade responsável do grupo";
   - serviços sobre os produtos → escopo.
5. **Preview não é contratual.** Recurso marcado *Preview* na base não conta como
   atendido. Marque 🔸 e diga "em preview".
6. **Campos `[A PREENCHER]`** (nível de parceria, certificações, atestados) **não
   comprovam nada**. Se o edital exigir declaração do fabricante, nível de parceria ou
   profissional certificado e o campo estiver vazio, o Go/No-Go fica **ATENÇÃO —
   depende do perfil**.
7. **Nível de parceria exigido:** se o edital pedir nível mínimo, declaração do fabricante
   ou "parceiro autorizado", compare com a tabela de níveis do índice.
   - Nível abaixo do exigido → NO-GO naquele item.
   - Ordem dos níveis marcada [VERIFICAR] → ATENÇÃO até confirmar no programa do fabricante.
   - Fabricante sem documento na base (só o nível): atenda apenas o que o edital permite
     comprovar com o nível; para o mapa de produtos, diga que a base não cobre.
8. **Preço de lista não é cotação.** Valores em USD da base são referência pública.
   - Use-os só como ordem de grandeza e rotule "estimativa (preço de lista)".
   - Aponte o **risco cambial** quando o contrato for em BRL.
   - Aponte o **teto do catálogo de preços do governo**, quando a base disser que
     existe um.

## Checagens que a base permite (rode em todo edital com software)

| Checagem | O que comparar | Exemplo de alerta |
|----------|----------------|-------------------|
| **Residência de dados** | Cláusula de hospedagem no Brasil ou na nuvem do órgão × regiões do produto | Produto só SaaS sem região no Brasil → ❌ ou 🔸 com mitigação |
| **On-premises / nuvem do contratante** | Exigência de instalação local, nuvem de governo ou infraestrutura indicada pelo órgão × modelos de entrega | Produto só SaaS → ❌. Versão autogerenciada pode não ter todos os recursos da SaaS → conferir requisito a requisito |
| **Nomenclatura legada** | SKU ou métrica do TR × nomes atuais da base | Métrica "clássica", SKU descontinuado ou produto renomeado → pedido de esclarecimento sobre o equivalente |
| **Métrica × ambiente** | Unidade pedida (núcleo, vCPU, usuário, host, GB, créditos) × ambiente descrito | Métrica por núcleo sem ferramenta de medição exigida pelo fabricante → risco de auditoria |
| **Natureza do item** | "Licença perpétua" × produto vendido por consumo ou subscrição | Incompatível → esclarecimento |
| **Licença por usuário × capacidade** | Quantidade de usuários do TR × limite da capacidade em que o usuário gratuito passa a consumir conteúdo | TR sem licenças de usuário suficientes |
| **Edição mínima** | Requisito (chave do cliente, conexão privada, DR entre regiões) × edição que o tem | Edição superior → preço maior |
| **Marca** | Edital exige marca × justificativa (padronização, compatibilidade, única marca, referência "ou similar") | Marca sem justificativa → avaliar impugnação (art. 41, I, Lei 14.133 [VERIFICAR alínea]) |
| **Carta do fabricante** | Exigência de carta de solidariedade ou declaração de parceria | Prazo para obter com o fabricante (art. 41, IV [VERIFICAR]) |
| **Conflito de portfólio** | Requisito atendido por dois ou mais parceiros | Recomende pelo critério do índice e mostre a alternativa |
| **Concorrente no canal** | Consultoria do próprio fabricante ou empresa adquirida por concorrente | Registre como risco competitivo |

## Entrega 6 — Matriz de Aderência ao Portfólio

Gere quando houver base de parceiros e o objeto envolver software ou serviços sobre
software. Fica **depois** do Go/No-Go e antes do Roteiro de Leitura.

```markdown
## Aderência ao portfólio (base de parceiros, ref. dd/mm/aaaa — não consta do edital)

Resumo: N requisitos mapeados · ✅ x · 🔸 y · ❌ z · ❓ w. Parceiro recomendado: ... (motivo).

| # | Requisito (edital) | Parceiro / produto | Status | Ressalva | Fonte na base |
|---|--------------------|--------------------|--------|----------|---------------|
| 1 | Dados hospedados no Brasil [tr.pdf, item 5.3, p. 12] | Snowflake — conta AWS São Paulo | ✅ | Só AWS; Azure/GCP no Brasil não atende | [base: 01_SNOWFLAKE, "Pontos de atenção", 1] |

### Fora do portfólio
Requisitos sem parceiro na base → precisam de outro fornecedor ou parceiro novo.

### Alertas de escopo e de licitação
Hardware, unidade do grupo, preview, nomenclatura legada, câmbio, carta do fabricante,
campos `[A PREENCHER]` que o edital exige.
```

- Contagens do resumo: refaça a partir da tabela e rotule "calculado".
- Requisito sem citação do edital não entra na matriz.
