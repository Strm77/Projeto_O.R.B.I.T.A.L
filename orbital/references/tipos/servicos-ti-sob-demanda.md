# Tipo: serviços de TI com equipe por demanda, sustentação e software como insumo

Guia para editais que contratam **serviços continuados sem dedicação exclusiva de mão de
obra**, combinando duas ou três frentes num grupo único:
- **projetos sob demanda** — equipe alocada por Ordem de Serviço (OS), paga pela alocação;
- **sustentação** — equipe fixa com preço mensal e SLA;
- **software como insumo** — ferramentas fornecidas pela contratada, sem licença em nome
  do órgão.

> Base: 1 caso real (MIDR, TR 7/2026, serviços de administração e inteligência de dados,
> 12 meses — gabarito em `tests/gabaritos/midr_tr_7_2026_dados/`, ainda **sem os PDFs**:
> páginas não conferidas). Confirme cada padrão no edital novo.

## 1. Como reconhecer

Três ou mais destes sinais:
- objeto em "frentes" ou itens de natureza diferente (projetos, sustentação, software)
  num **grupo único**, com justificativa de que "quem desenvolve sustenta";
- "sem dedicação exclusiva de mão de obra";
- OS com **perfis e percentual de alocação**; catálogo de serviços; métrica auxiliar de
  horas (HST, UST) que **não** é unidade de faturamento;
- tabela de **perfis profissionais** com experiência mínima e certificações;
- IMR com vários indicadores e **teto de desconto** sobre a fatura;
- **Prova de Conceito** do software;
- **planilha de custos** com fator K, custo por perfil × quantidade × alocação;
- ambientação inicial e **transição final**.

## 2. Onde as coisas costumam estar

O pacote costuma vir **fatiado em muitos arquivos** (TR + Anexos A a K no caso MIDR).
Mapeie cada anexo no inventário antes de responder:

| Anexo (caso MIDR) | Conteúdo típico |
|-------------------|-----------------|
| TR | Itens e valores, grupo único, vigência, modelo de execução, compartilhamento de profissionais, vistoria, garantias, IMR (seção 8), sanções (9), critérios de seleção e habilitação (10), POC, estimativa (11), cronograma |
| A | Processo de desenvolvimento (ágil, normas, Design System, acessibilidade) |
| B | Projetos sob demanda: ciclo da OS, plano preliminar, fases, pagamento por alocação |
| C | Sustentação: horário, preço fixo, emergências, evoluções pequenas, matriz de severidade e SLA |
| D | Software: grupos funcionais, requisitos (base da POC), volumetria de "fundamentação" |
| E | Perfis profissionais e qualificação |
| F | Catálogo de serviços e métrica auxiliar (HST) |
| G / H | Termo de sigilo / termo de ciência |
| I | Padrões de banco de dados e janela de execução em produção |
| J | Modelo de proposta (dados obrigatórios do software, declaração de vistoria) |
| K | Planilha de custos e fórmula de preço |

**Edital e ETP às vezes não vêm junto.** Sem eles faltam: data e modo de disputa, prazo
de impugnação, minuta do contrato, **volumetria oficial** e salários de referência.
Diga isso no topo da resposta e liste as perguntas que ficam sem resposta.

## 3. Campos específicos deste tipo

| Campo | O que extrair |
|-------|---------------|
| Itens e valores | Por item: valor mensal, anual e se é **teto** ou receita fixa; total; sigiloso ou público |
| Aritmética dos valores | Mensal × 12 = anual? Soma dos itens = total? (calcule e mostre) |
| Grupo único | Justificativa; consequência (uma só empresa para tudo) |
| Projetos (OS) | Conteúdo da OS, prazo do plano preliminar, correção, fases, regra de pagamento |
| Sustentação | Horário (8x5?), preço fixo por quantas pessoas, emergências fora do horário, limite de "evolução pequena" |
| SLA | Por severidade: início, solução de contorno, solução definitiva; matriz de severidade; regra de prazo fora do horário |
| Software | Grupos funcionais, on-premises × nuvem, vários fabricantes, métrica livre, valor variável pelo uso, prazo de disponibilização, propriedade (licença em nome de quem?) e saída de dados no fim |
| Volumetria | Números do ambiente e **onde está a oficial** (ETP? Edital? anexo?) |
| Equipe | Perfis por item, quantidade, qualificação, entrevista, compartilhamento (outros contratos, entre equipes, acúmulo) |
| Métrica auxiliar | HST/UST: definição, estimativa anual, média por profissional — e se fatura ou não |
| Processo e padrões | Metodologia, normas, padrões de banco, quem executa scripts em produção |
| Local e infraestrutura | Remoto/presencial; o que a contratada paga (estação, VPN, firewall, endpoint) |
| Início | Reunião inicial, plano de ambientação, duração, carência do IMR |
| Encerramento | Plano de transição (prazo, duração, se é pago), sigilo pós-contrato |
| IMR | Indicadores, metas, faixas de desconto, **teto** total |
| Recebimento e pagamento | Relatório mensal, provisório, definitivo, liquidação, pagamento; prazos que podem dobrar |
| Reajuste | Índice, data-base, automático ou a pedido |
| Garantias | Contratual (%, base, validade, prazo por modalidade) e técnica |
| Multas | Moratória, por atraso na garantia, compensatórias (base: valor anual?) |
| Proposta | Dados obrigatórios, planilha, validade, limite para diligência de inexequibilidade |
| Habilitação técnica | Atestados de software, de horas/ano, de **gestão de equipe** (perfis simultâneos, período), vedações (mesmo grupo) |
| POC | Etapas e prazos, ao vivo × gravado, mesmas versões/marcas, critério de reprovação, qual anexo é verificado |

## 4. Banco de perguntas (modelo em 30 perguntas)

**Visão geral**
1. Quem contrata (órgão, unidade, UASG, nº do TR/processo) e o quê.
2. Itens e valores (mensal e anual), total, teto e sigilo — confira a aritmética.
3. Grupo único ou itens separados; justificativa.
4. Modalidade, critério e regime de execução (data e modo de disputa, se houver Edital).
5. Vigência e prorrogação.
6. ME/EPP, consórcio, cooperativa, subcontratação.
7. Vistoria: obrigatória ou facultativa; o que o modelo de proposta exige declarar.

**Modelo de execução**
8. Como funciona o item de projetos (OS, plano, fases, pagamento).
9. Como funciona a sustentação (horário, preço, emergências, evoluções).
10. SLA da sustentação por severidade.
11. Como funciona o item de software (grupos, instalação, fabricantes, métrica, preço, prazo).
12. Tamanho do ambiente e de onde vem a volumetria oficial.
13. Propriedade do software e saída de dados no fim.
14. Equipe estimada por item.
15. Qualificação exigida por perfil.
16. Compartilhamento de profissionais.
17. Métrica auxiliar (HST/UST): o que é e se fatura.
18. Processo de desenvolvimento exigido.
19. Regras de banco de dados e de execução em produção.
20. Remoto ou presencial; quem paga a infraestrutura.

**Início e encerramento**
21. Início: reunião, ambientação, carência de indicadores.
22. Encerramento: transição (paga?), sigilo.

**Dinheiro**
23. Indicadores do IMR, metas, descontos e teto.
24. Recebimento e pagamento (prazos em sequência).
25. Reajuste.
26. Garantias (contratual e técnica).
27. Multas.
28. Conteúdo obrigatório da proposta e limite de inexequibilidade.

**Habilitação e Prova de Conceito**
29. Habilitação (técnica, gestão de equipe, econômico-financeira). 🔴
30. Prova de Conceito (etapas, prazos, critério). 🔴

Feche com **Contradições** e **Lacunas** (documentos citados e não fornecidos).

## 5. Armadilhas típicas deste tipo

| Armadilha | Como aparece | Por que importa |
|-----------|--------------|-----------------|
| **Teto, não receita** | Item de projetos com "valor mensal" mas pago só pela alocação prevista nas OS | Sem OS, não há receita; não dimensione a empresa pelo teto 🔴 |
| **Plantão não remunerado** | Sustentação 8x5 com preço fixo, mas emergências fora do horário "sem acréscimo" e severidade máxima com início em 2 h | Custo de sobreaviso fora do preço 🟡 |
| **Volumetria fora do pacote** | Números do ambiente só como "fundamentação"; a oficial "no ETP" ou "no Edital" (às vezes os dois, em lugares diferentes) | Sem ela não dá para precificar o software 🔴 |
| **POC verifica qual anexo?** | TR manda verificar a tabela de um anexo e, adiante, os requisitos de outro | Matriz errada = reprovação 🔴 |
| **Atestado de gestão de equipe** | N perfis mantidos simultaneamente por M meses, com contrato, OS, vínculos e planilha | Exigência documental pesada; checar cedo 🔴 |
| **Atestado em horas × estimativa** | Atestado de X horas/ano contra a estimativa anual do catálogo | Se passar de 50% do objeto comparável, avaliar impugnação (art. 67, §2º [VERIFICAR]); defina a base (só projetos? projetos + sustentação?) |
| **Teto do IMR alto** | Descontos somados até 50% da fatura | Risco de margem; simule o pior mês |
| **Software sem licença para o órgão** | Insumo da contratada; dados exportados e eliminados no fim | Custo de saída e de comprovação de eliminação |
| **Legado antigo** | Bancos fora de suporte (ex.: SQL Server 2000, Oracle 11gR2) | Conectores da solução podem não suportar |
| **Execução em produção pelo órgão** | Scripts só rodam pela equipe do órgão em janelas fixas | Prazos de SLA dependem de terceiro |
| **Infraestrutura por conta da contratada** | Estação, VPN, firewall com IPS, endpoint | Custo fixo a incluir na planilha |
| **Centavos acima do teto** | Valor anual do edital menor que mensal × 12 | Cotar no teto mensal pode estourar o teto anual por centavos |
