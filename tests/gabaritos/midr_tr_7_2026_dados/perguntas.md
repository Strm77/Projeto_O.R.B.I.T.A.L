<!--
Gabarito fornecido pelo usuário em 05/10/2026. Conteúdo original, sem edição.
Tipo: serviços de TI com equipe por demanda (projetos), sustentação e software como insumo.
PDFs-fonte NÃO estão no repositório: TR (48 p.) e Anexos A a K (12 arquivos). Edital e ETP não foram fornecidos.
Revisão do gabarito: ver notas_revisao.md nesta pasta.
-->

Seguem as 30 perguntas cobrindo os 12 arquivos. Abreviações: **TR** = Termo de Referência (48 p.) e **An. A** a **An. K** = Anexos A a K. Nos 12 arquivos, o número de página do PDF é o mesmo número impresso na página.

> ⚠️ **O Edital e o ETP não estão entre os 12 arquivos.** Por isso não há como responder sobre data da sessão, prazo de impugnação, modo de disputa, intervalo de lances ou minuta do contrato. E a **volumetria de referência**, necessária para precificar o software do Item 3, está no ETP. Detalho isso nas lacunas, no fim.

## Visão geral

**1. Quem contrata e o quê?**
O Ministério da Integração e do Desenvolvimento Regional (MIDR), pela Diretoria de Tecnologia da Informação (UASG 530032). TR 7/2026, Processo 59000.009749/2025-21.
O objeto são serviços de administração e inteligência de dados, em três frentes: sustentação, disponibilização de software e projetos sob demanda. Todos sem dedicação exclusiva de mão de obra.
📍 `[TR, 1.1, p. 1]`

**2. Quais são os itens e valores?**

| Item | Descrição | Valor mensal | Valor em 12 meses |
|---|---|---|---|
| 1 | Projetos sob demanda | R$ 326.916,36 | R$ 3.922.996,30 |
| 2 | Sustentação | R$ 142.965,15 | R$ 1.715.581,75 |
| 3 | Soluções de software | R$ 113.951,23 | R$ 1.367.414,76 |
| | **Total** | | **R$ 7.005.992,81** |

O valor total é o **máximo aceitável** e é **público**, sem sigilo.
📍 `[TR, 1.1, p. 1]` · `[TR, 11.1, p. 45]` · `[TR, 13.1, p. 46]` · `[An. J, p. 1]`

**3. Dá para disputar só um dos itens?**
Não. É **grupo único**, adjudicado a uma só empresa. A justificativa é técnica: quem desenvolve sustenta, e o software é insumo dos dois serviços.
📍 `[TR, 1.1.1–1.1.2, p. 2]`

**4. Qual é a modalidade, o critério e o regime de execução?**
Pregão eletrônico, menor preço, empreitada por preço unitário.
📍 `[TR, 10.1–10.2, p. 40]`
Data, horário e modo de disputa: **não encontrados nos documentos analisados** (estariam no Edital).

**5. Qual é a vigência?**
12 meses contados da assinatura, prorrogável até 10 anos.
📍 `[TR, 1.4, p. 2]`

**6. ME/EPP, consórcio, cooperativa e subcontratação são permitidos?**
- ME/EPP: sem tratamento favorecido `[TR, 4.79, p. 18]`
- Consórcio: vedado `[TR, 4.81, p. 19]`
- Cooperativa: vedada `[TR, 10.38, p. 44]`
- Subcontratação: vedada `[TR, 4.58, p. 16]`

**7. A vistoria é obrigatória?**
Não, é **facultativa**, com agendamento pelo (61) 2034-5890 ou cosol@mdr.gov.br. Mas o modelo de proposta exige declarar **ou** que a vistoria foi feita **ou** que houve recusa formal. É um detalhe fácil de esquecer.
📍 `[TR, 4.49–4.53, p. 15]` · `[An. J, p. 2]`

## Modelo de execução

**8. Como funciona o Item 1, de projetos?**
1. O MIDR emite uma Ordem de Serviço (OS) com escopo, entregáveis, perfis e percentual de alocação.
2. A contratada entrega um **Plano Preliminar em 5 dias úteis**. Se for recusado, tem 2 dias úteis para corrigir.
3. Os projetos podem ser divididos em OS de Concepção, de Construção e de Homologação/Implantação.
4. O pagamento é o valor mensal da equipe, conforme a alocação prevista nas OS e os produtos aceitos.

📍 `[An. B, p. 1–3]` · `[TR, 3.3, p. 9]`

**9. Como funciona o Item 2, de sustentação?**
- Regime **8x5**, com preço fixo mensal correspondente a 5 profissionais.
- Atendimentos emergenciais em fim de semana, feriado ou fora do horário **não geram acréscimo de preço**.
- Evoluções pequenas são permitidas se levarem até 8 horas. Acima disso, viram projeto do Item 1.

📍 `[An. C, p. 1]` · `[An. C, p. 5]`

**10. Qual é o SLA da sustentação?**

| Severidade | Início do atendimento | Solução operacional | Solução definitiva |
|---|---|---|---|
| 0 | 2 h | 8 h | 48 h |
| 1 | 4 h | 24 h | 72 h |
| 2 | 8 h | 48 h | conforme cronograma |
| 3 | 24 h | 72 h | conforme cronograma |

A severidade sai de uma matriz que cruza criticidade e disponibilidade. Se um prazo vencer fora do horário de execução, conta até o fim da primeira hora do turno seguinte.
📍 `[An. C, p. 5–6]`

**11. Como funciona o Item 3, de software?**
- Há três grupos funcionais: integração em tempo real; qualidade e governança; análise e visualização.
- A regra é instalação **on-premises**. Nuvem só por exceção, sem cópia integral das bases.
- Pode haver **vários fabricantes**, desde que as soluções funcionem integradas.
- A métrica de licenciamento é livre.
- O valor mensal **pode variar conforme o uso efetivo**.
- O software deve ser disponibilizado em **10 dias úteis** contados da OS.

📍 `[An. D, p. 1–2]` · `[TR, 3.5, p. 9]` · `[TR, 4.14, p. 11]`

**12. Qual é o tamanho do ambiente?**
- Até 281 TB de dados (100 TB priorizados), com ingestão de até 3 TB por dia.
- 25 TB estruturados distribuídos em 23 servidores; 70 TB em arquivos e FTP.
- 68 sistemas, dos quais 15 críticos.
- 19.210 usuários, até 1.100 simultâneos.
- Bancos legados: **Oracle 11gR2 e SQL Server 2000**.

📍 `[An. D, p. 2–5]`
> **Interpretação:** esses números aparecem só como "fundamentação" dos requisitos. A volumetria oficial está no ETP, que não foi fornecido. Bancos tão antigos também são um risco para os conectores da sua solução.

**13. O software fica com o MIDR no fim do contrato?**
Não. É insumo da contratada e **não gera licença em nome da Administração**. No fim do contrato, a contratada precisa exportar os dados em formato aberto e comprovar que os eliminou do ambiente dela.
📍 `[An. K, p. 2]` · `[An. D, p. 1]`

**14. Qual é a equipe estimada?**
- **Item 1 (10 pessoas):** analista de BI, analista de negócios, arquiteto de dados, arquiteto de software, analista de testes, 2 desenvolvedores, cientista de dados, gerente de projetos e engenheiro de IA.
- **Item 2 (5 pessoas):** 2 administradores de dados, arquiteto de dados, DBA e líder técnico.

📍 `[TR, 2.3, p. 3–5]` · `[An. B, p. 3–4]` · `[An. C, p. 7]`

**15. Que qualificação cada profissional precisa ter?**
- Todos os perfis: **5 anos de experiência** mais certificação, pós-graduação ou 2 anos adicionais de experiência.
- Diploma reconhecido pelo MEC.
- O MIDR pode **entrevistar** os profissionais.

📍 `[An. E, p. 1–7]`

**16. Posso compartilhar profissionais?**
- Com outros contratos: sim, desde que os níveis de serviço sejam mantidos `[TR, 3.7, p. 9]` `[An. C, p. 1]`.
- Entre equipes deste contrato: com limites, de 1 a 4 equipes por perfil (desenvolvedor só em 1). Acúmulo de funções é proibido.
- Os 5 perfis da sustentação ficam exclusivos dessa equipe.

📍 `[TR, 4.38–4.40, p. 13–14]`

**17. O que é a HST?**
É a Hora de Serviço Técnico, uma **métrica auxiliar** de dimensionamento. **Não é unidade de faturamento.** O catálogo estima 17.092 HST por ano, com média de 141 HST por mês por profissional.
📍 `[An. B, p. 3]` · `[An. F, p. 9–10]`

**18. Qual processo de desenvolvimento é exigido?**
Ágil (Scrum), com sprints de 1 a 4 semanas e Definição de Pronto por projeto. Segue a ISO 12207 e a Portaria SGD 750/2023. Também é exigido TDD sempre que possível, o Design System do gov.br e acessibilidade.
📍 `[An. A, 1.1 e 2.4, p. 1]` · `[An. A, 14.1, p. 12]` · `[TR, 4.28, p. 12]`

**19. Que regras de banco de dados valem?**
- Modelos na 3ª forma normal, nomes com até 30 caracteres, sem BLOB.
- **Scripts em produção só são executados pela equipe do MIDR**, na janela de segunda-feira das 12h às 14h ou após as 18h.

📍 `[An. I, 2.1, p. 3]` · `[An. I, 7.1, p. 14]`

**20. O trabalho é remoto ou presencial? Quem paga a infraestrutura?**
É remoto de preferência. Presencial só com aviso de 5 dias. A contratada fornece por conta própria estação de trabalho, VPN, firewall com IPS e proteção de endpoint.
📍 `[TR, 6.2, p. 21]` · `[TR, 6.6–6.9, p. 21]`

## Início e encerramento

**21. Como é o início do contrato?**
1. Reunião inicial em até 5 dias úteis da assinatura.
2. Plano de Ambientação em até 3 dias úteis depois da reunião.
3. Ambientação de até 30 dias.
4. Declaração de capacidade técnica em até 3 dias úteis após a ambientação.

Durante a ambientação podem ser emitidas OS, **sem penalidades do IMR** (o instrumento de indicadores e descontos).
📍 `[TR, 7.9, p. 24]` · `[TR, 6.1.2–6.1.5, p. 20]` · `[TR, cronograma, p. 46]`

**22. Como é o encerramento?**
- Plano de Transição em até 60 dias antes do fim do contrato, com execução de até 90 dias, **sem pagamento**.
- O Termo de Sigilo continua valendo depois do contrato. O Termo de Ciência é assinado por cada funcionário.

📍 `[TR, 6.19–6.23, p. 22–23]` · `[An. G, cl. 6ª, p. 3]` · `[An. H, p. 1]`

## Dinheiro

**23. Quais indicadores podem reduzir o pagamento?**

| Indicador | O que mede | Meta |
|---|---|---|
| IEP | Entregas de projeto no prazo | ≥ 90% |
| IEQ | Entregas de projeto com qualidade | ≥ 90% |
| IST | Satisfação nos treinamentos | ≥ 80% |
| IDP | Demandas de sustentação no prazo | ≥ 90% |
| IQD | Qualidade nas demandas de sustentação | ≥ 90% |
| IDS | Disponibilidade do software | ≥ 80% |

Os descontos vão de 3% a 20% por indicador, com **teto de 50%** da fatura.
📍 `[TR, 8.4, p. 26–32]` · `[TR, 8.5, p. 32]`

**24. Como funcionam o recebimento e o pagamento?**
1. Relatório Gerencial mensal aprovado.
2. Recebimento provisório em 5 dias.
3. Recebimento definitivo em 10 dias.
4. Liquidação em 10 dias úteis.
5. Pagamento em 10 dias úteis.

Os prazos de recebimento **podem dobrar** com justificativa.
📍 `[TR, 8.8–8.10, p. 33]` · `[TR, 8.23, p. 34]` · `[TR, 8.27 e 8.29, p. 35]` · `[TR, 8.39, p. 36]`

**25. Há reajuste?**
Sim, pelo ICTI, **automático e sem precisar pedir**. A data-base é o orçamento de 01/03/2026.
📍 `[TR, 8.45–8.46, p. 37]`

**26. Quais garantias são exigidas?**
- **Garantia contratual de 5% do valor anual**, válida até 90 dias após o fim do contrato. Seguro-garantia precisa ser entregue até a assinatura; as outras modalidades, em até 10 dias úteis depois.
- **Garantia técnica** de 90 dias após o recebimento definitivo.

📍 `[TR, 4.60–4.61, p. 16]` · `[TR, 4.33, p. 13]`

**27. Quais são as multas?**
- Atraso: 0,2% por dia, até 20 dias.
- Atraso na garantia: 0,07% por dia, até 2%. Acima de 25 dias, o contrato pode ser extinto.
- Multas compensatórias: de 2% a 10% do valor anual.

📍 `[TR, 9.2.4, p. 38–39]`

**28. O que a proposta precisa conter?**
- **Anexo J:** dados obrigatórios de cada software — nome, versão, métrica, fabricante e part number.
- **Anexo K:** planilha de custos com fator K e a fórmula custo mensal por perfil = custo total × quantidade × alocação, mais o custo do software por grupo funcional.
- Validade de 60 dias.
- Proposta abaixo de **70% do valor de referência** de qualquer item passa por diligência detalhada.

📍 `[TR, 4.80, p. 18–19]` · `[An. J, p. 1]` · `[An. K, p. 1–2]`

## Habilitação e Prova de Conceito

**29. O que é exigido na habilitação?** 🔴
- **Atestados técnicos:**
  - de solução de pelo menos um dos três grupos, com instalação e suporte;
  - de **10.000 horas por ano** de serviços de dados.
- **Gestão de equipe:** comprovar **6 perfis mantidos ao mesmo tempo por 6 meses nos últimos 12 meses**. É preciso apresentar contrato, OS, documentos de vínculo dos profissionais e uma planilha consolidada.
- Atestados emitidos por empresa do mesmo grupo empresarial não valem.
- **Econômico-financeira:** índices maiores que 1 em **cada um dos dois últimos exercícios**. Se não atingir, exige-se patrimônio líquido de 10% do valor estimado, que pelo meu cálculo dá **R$ 700.599,28**.

📍 `[TR, 10.30–10.36, p. 42–43]` · `[TR, 10.22–10.24, p. 41–42]`

**30. Como funciona a Prova de Conceito?** 🔴
1. Documentação técnica entregue **imediatamente** após os lances.
2. O pregoeiro valida em 5 dias úteis.
3. A empresa recebe o roteiro e tem 5 dias úteis para preparar o ambiente.
4. Demonstração **ao vivo** por videoconferência, com as **mesmas versões e marcas** que serão fornecidas. Vídeo gravado não é aceito.
5. Resultado em 2 dias úteis.

Os custos são do licitante. Não atender a **todos** os requisitos desclassifica a empresa.
📍 `[TR, 4.59, p. 16]` · `[TR, 10.45–10.58, p. 44–45]`
> **Interpretação:** o Anexo D traz requisitos muito específicos, como AWS Greengrass, microgateways, EDI/SWIFT/HL7, MQTT/CoAP e mais de 30 conectores de BI. Antes de decidir participar, vale cruzar requisito por requisito com a sua solução.

## Contradições

| # | Tema | Fonte A | Fonte B | Impacto |
|---|---|---|---|---|
| 1 | Qual anexo a Prova de Conceito verifica | Tabela de requisitos do **Anexo C** `[TR, 10.47, p. 44]` | Requisitos do **Anexo D** `[TR, 10.45 e 10.49, p. 44]` `[An. D, p. 2]` | 🔴 Não fica claro qual matriz montar |
| 2 | Onde está a volumetria | "No ETP" `[An. D, p. 1]` | "No Edital" `[An. D, p. 2]` `[An. K, p. 2]` | 🔴 Nenhum dos dois foi fornecido, e sem ela não dá para precificar o Item 3 |
| 3 | Receita do Item 1 | Valor mensal fixo por equipe `[TR, 1.1, p. 1]` | Sem OS, não há profissionais; paga-se só a alocação prevista `[An. B, p. 2–3]` `[An. K, p. 1]` | 🔴 Os R$ 3,9 milhões são teto, não receita garantida |
| 4 | Horário da sustentação | 8x5 `[An. C, p. 1]` `[TR, 4.44, p. 14]` | Emergências fora do horário sem custo, e severidade 0 com início em 2 h `[An. C, p. 1 e 6]` | 🟡 Plantão não remunerado |
| 5 | Erro de cópia | O indicador IDS fala em soluções "à disposição dos **Correios**" `[TR, p. 31]` | — | 🟢 Indica texto copiado de outro edital; vale procurar outros resíduos |
| 6 | Nome do Grupo 3 | "Análise, visualização e inteligência de dados" `[TR, 3.5, p. 9]` | "Análise de dados, visualização e business intelligence" `[An. D, p. 21]` | 🟢 |

## Lacunas

Documentos citados que não estão entre os 12 arquivos:
- **Edital**: datas, prazo de impugnação, modo de disputa, minuta do contrato.
- **ETP**: volumetria e salários de referência `[TR, 6.11, p. 22]`.
- **Modelo de formulário** para comprovar os perfis `[TR, 10.34, p. 43]`.
- **Política de Segurança da Informação do MIDR** `[TR, 4.47, p. 14]`.

Se você conseguir o Edital e o ETP, eu completo as respostas que ficaram em aberto.
