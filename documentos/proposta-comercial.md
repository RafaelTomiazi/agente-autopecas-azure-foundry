# Assistente Inteligente de Consulta ao Catálogo

**Proposta de Solução em Inteligência Artificial**

Cliente: Rodavale Distribuidora de Autopeças Ltda.
Área: Comercial — Televendas
Documento: Proposta Comercial nº 2026-014 (revisão 2)
Validade: 30 dias a contar da data de emissão

Documento confidencial. Destinado exclusivamente ao cliente identificado acima.

---

## 1. Sumário Executivo

A Rodavale enfrenta um gargalo estrutural no televendas: o conhecimento sobre quais peças servem em quais veículos está concentrado na memória de poucos vendedores experientes e em catálogos de fabricante dispersos. Esta proposta apresenta um assistente de inteligência artificial que torna esse conhecimento consultável em segundos por qualquer vendedor da equipe.

A solução é composta por **três agentes especializados** que trabalham em conjunto. O vendedor faz uma pergunta em linguagem natural — "que pastilha serve num Onix 2018 1.4?" — e um agente orquestrador identifica o domínio da pergunta e encaminha para o especialista adequado: catálogo e estoque, ou comercial. Quando a pergunta é uma cotação, os dois especialistas atuam em sequência.

Não se trata de substituir o vendedor, mas de eliminar o tempo que ele gasta procurando informação. O atendimento continua humano; a consulta deixa de depender de memória.

| 11 → 7 | 3 | R$ 9.900 | 0 |
|---|---|---|---|
| minutos por atendimento | agentes especializados | de ganho mensal estimado | linhas de código a manter |

---

## 2. Entendimento do Cliente

A Rodavale Distribuidora de Autopeças é uma empresa familiar fundada em 2004, hoje sob gestão da segunda geração. Atua na distribuição de peças de reposição para o mercado independente, com sede e centro de distribuição em Duque de Caxias (RJ) e uma filial em Campos dos Goytacazes.

| Indicador | Situação atual |
|---|---|
| Faturamento anual | R$ 74 milhões |
| Colaboradores | 68 |
| Itens ativos em catálogo | 18.000 SKUs, de 35 fornecedores |
| Carteira de clientes ativos | 900 (oficinas, autocenters, retíficas e frotistas) |
| Equipe de televendas | 9 vendedores internos |
| Equipe de TI | 2 profissionais (sustentação de ERP e infraestrutura) |

### Como o atendimento funciona hoje

O cliente liga ou envia mensagem descrevendo o veículo e a peça de que precisa. O vendedor consulta o ERP, que permite busca por código ou descrição — mas não por aplicação veicular. Para descobrir quais itens servem em determinado carro, o vendedor recorre à própria experiência, a catálogos de fabricante em PDF ou a um colega mais antigo.

A observação central deste diagnóstico: **o ERP da Rodavale registra o que a empresa tem, mas não responde a pergunta que o cliente faz.** A tradução entre "meu carro é um Onix 2018" e "o SKU RV-1002 atende" acontece na cabeça do vendedor.

---

## 3. Diagnóstico do Problema

### 3.1 Sintomas observados

| Métrica | Situação atual |
|---|---|
| Tempo médio de atendimento | 11 minutos |
| Chamadas que exigem retorno posterior | ~30% |
| Pedidos perdidos por demora na resposta (estimado) | ~6% do potencial |
| Tempo de formação de um novo vendedor | 4 a 6 meses |
| Consultas fora do expediente sem resposta | ~40 por semana |

### 3.2 Causas identificadas

**Busca por aplicação não existe no sistema.** O catálogo é organizado por código e descrição. A relação entre peça e veículo — que é como o cliente pensa — não é consultável.

**Assimetria de experiência na equipe.** Dois vendedores resolvem a maioria das consultas de memória. Os recém-contratados levam o triplo do tempo e cometem mais erros de aplicação, o que gera devolução e retrabalho no pós-venda.

**Concentração de risco.** O conhecimento crítico não está documentado. A saída de um vendedor experiente representa perda operacional imediata e difícil de repor.

### 3.3 Impacto

Cada minuto adicional no atendimento se multiplica por aproximadamente 270 contatos diários. Além do custo direto de horas, a demora afeta a percepção de serviço: oficinas trabalham com o veículo parado e priorizam o distribuidor que responde primeiro.

---

## 4. Solução Proposta

Um conjunto de **três agentes especializados** disponível aos vendedores do televendas, capaz de consultar o catálogo da Rodavale em linguagem natural e responder com dados de aplicação, estoque e preço.

### 4.1 Por que três agentes, e não um

Um agente único precisa dominar todos os assuntos ao mesmo tempo: compatibilidade técnica, regras de estoque, tabelas de preço e política comercial. Quanto mais assuntos em um mesmo conjunto de instruções, maior a chance de o agente misturar domínios — por exemplo, aplicar desconto sem confirmar a peça, ou sugerir peça sem checar a aplicação.

A arquitetura multiagente separa responsabilidades:

| Agente | Responsabilidade | Fonte de informação |
|---|---|---|
| **Orquestrador** | Recebe a pergunta, identifica o domínio e define o caminho | Nenhuma. Apenas classifica |
| **Especialista de Catálogo e Estoque** | Compatibilidade, SKU, marca, preço-base e saldo por filial | Base de catálogo e índice de SKUs |
| **Especialista Comercial** | Cliente, tabela de preço, desconto e cotação indicativa | Base de clientes e condições comerciais |

Cada especialista responde apenas dentro do seu domínio e é explicitamente proibido de opinar fora dele. Isso torna o comportamento previsível e o erro fácil de localizar: quando uma resposta sai errada, sabe-se qual agente e qual base revisar.

### 4.2 O que o assistente faz

| Pergunta do vendedor | Caminho | Resposta |
|---|---|---|
| "Que pastilha serve num Onix 2018 1.4?" | Catálogo | Peças aplicáveis, com marca, posição, preço-base e saldo |
| "Qual a tabela da Auto Center Central?" | Comercial | Tabela do cliente e descontos por categoria |
| "Faça uma cotação da RV-1002 para a Auto Center Central" | Catálogo → Comercial | Preço-base, desconto aplicado e preço final indicativo |
| "Preciso de amortecedor" | Catálogo | Solicita o veículo antes de responder, evitando indicação incorreta |
| Assunto fora do televendas | Mensagem padrão | Informa o escopo do assistente |

### 4.3 Princípios de projeto

**Resposta ancorada em dado real.** Os especialistas não geram informação por conta própria. Toda resposta vem de consulta às bases de conhecimento da Rodavale. Quando não encontra, o agente informa que não encontrou — não inventa.

**Somente consulta.** O assistente não altera cadastro, estoque ou preço, e não registra pedido, reserva ou aprovação de crédito. A operação transacional segue exclusivamente pelo ERP.

**O vendedor decide.** A ferramenta apresenta as opções; a recomendação e o fechamento continuam sendo do profissional. Observações técnicas de aplicação são sempre repassadas para evitar venda incorreta.

**Configuração, não programação.** Todo o comportamento dos agentes e o roteamento entre eles são definidos no portal do Microsoft Foundry, em instruções de texto e em um fluxo visual. Não há código proprietário a ser mantido pela equipe de TI da Rodavale.

---

## 5. Arquitetura da Solução

```text
                        Vendedor
                           |
                           v
                 Orquestrador (classifica)
                           |
        +------------+-----+------+--------------+
        |            |            |              |
    CATALOGO      COTACAO     COMERCIAL    FORA DO ESCOPO
        |            |            |              |
        v            v            v              v
   Catálogo e   Catálogo e    Comercial      Mensagem
    Estoque      Estoque          |          padrão
        |            |            |              |
        |            v            |              |
        |       Comercial         |              |
        +------------+------------+--------------+
                           |
                           v
                       Resposta
```

| Camada | Componente | Função |
|---|---|---|
| Interface | Microsoft Foundry | Onde o vendedor conversa com o assistente |
| Orquestração | Workflow do Foundry | Direciona a pergunta para o agente certo, sem código |
| Agentes | Foundry Agent Service | Três agentes com instruções e escopos distintos |
| Modelo | GPT-5-mini | Compreensão de linguagem natural e formatação da resposta |
| Conhecimento | File Search do Foundry | Bases de catálogo, índice de SKUs e condições comerciais |

### 5.1 Fluxo de uma cotação

1. O vendedor pergunta: "faça uma cotação da RV-1002 para a Auto Center Central".
2. O orquestrador classifica a pergunta como cotação e repassa apenas o que o vendedor informou.
3. O Especialista de Catálogo e Estoque localiza o SKU e devolve descrição, marca, categoria, posição, preço-base e saldo de referência.
4. O Especialista Comercial localiza o cliente, identifica a tabela de preço, aplica o desconto da categoria e apresenta o preço final.
5. A resposta registra que a cotação é indicativa e não cria pedido nem reserva.

### 5.2 Segurança e conformidade

**Sem alteração de dados.** Não existe caminho técnico pelo qual o assistente altere cadastro, estoque, preço ou situação de crédito.

**Escopo restrito por instrução.** Cada agente responde somente dentro do seu domínio, e o caminho padrão trata qualquer assunto fora do televendas com uma mensagem fixa.

**Rastreabilidade.** A plataforma registra cada interação — pergunta, agente acionado, trecho consultado e resposta — permitindo auditoria posterior e análise de qualidade.

**Residência de dados.** Na prova de conceito, as bases de conhecimento estão indexadas no projeto Foundry, provisionado na região East US por disponibilidade de modelos. Como os dados são fictícios, isso não representa risco nesta fase. Na implantação produtiva, o provisionamento em Brazil South mantém os dados da Rodavale em território nacional e deve ser tratado como requisito.

---

## 6. Escopo de Entrega

A entrega está organizada em duas etapas distintas: a prova de conceito, já construída e disponível para demonstração, e a implantação produtiva, cujo escopo é fechado após a descoberta.

### 6.1 Prova de conceito — já entregue

| Item | Situação |
|---|---|
| Três agentes configurados | Orquestrador, Catálogo e Estoque, e Comercial |
| Bases de conhecimento | Catálogo com 3.367 aplicações veiculares, índice de SKUs e base comercial com 90 clientes |
| Orquestração | Fluxo de roteamento com quatro caminhos, montado no portal |
| Validação | Seis casos de teste aprovados, com gabarito conferido nas bases |
| Documentação | Esta proposta e a documentação técnica da solução |

A prova de conceito opera sobre uma amostra representativa do catálogo, com posição de referência em 20/08/2026. Ela demonstra o comportamento do assistente e serve de base para o dimensionamento da implantação.

### 6.2 Implantação produtiva — escopo a fechar na descoberta

| Item | Descrição |
|---|---|
| Integração com o ERP | Extração e atualização do catálogo, estoque, clientes e tabelas de preço |
| Carga completa | Migração dos 18.000 SKUs e das aplicações veiculares correspondentes |
| Segurança e acesso | Controle de acesso por perfil e restrição das bases comerciais |
| Residência de dados | Provisionamento em Brazil South |
| Canal de atendimento | Publicação do assistente no ambiente de trabalho da equipe |
| Testes assistidos | Bateria de validação com casos reais fornecidos pela equipe comercial |
| Capacitação | Sessão de treinamento com a equipe de televendas |
| Acompanhamento | Suporte pós-implantação |

O esforço de cada item depende do que for encontrado na descoberta: formato de extração do ERP, qualidade dos dados de aplicação veicular e requisitos de segurança da Rodavale. Esta etapa não é cobrada como projeto à parte: ela está incluída na assinatura descrita na seção 8, e a descoberta do primeiro mês é o que confirma ou ajusta esse valor.

### 6.3 Fora do escopo

- Alterações no ERP atual ou em qualquer sistema legado da Rodavale
- Sincronização automática e contínua entre ERP e base de consulta (prevista para fase posterior)
- Atendimento direto ao cliente final por WhatsApp ou portal (prevista para fase posterior)
- Digitalização ou tratamento de catálogos de fabricante em papel
- Licenças de software de terceiros não mencionadas nesta proposta

---

## 7. Cronograma de Referência

As durações abaixo são referência para planejamento e são confirmadas ao final da descoberta.

**Fase 1 — Descoberta e modelagem.** Levantamento da estrutura de dados do ERP, definição do modelo de catálogo e mapeamento das regras de aplicação veicular. Entrevistas com a equipe de televendas para levantamento dos casos de uso mais frequentes. Ao final desta fase, o valor da assinatura é confirmado ou ajustado.

**Fase 2 — Integração e carga.** Extração a partir do ERP, carga completa do catálogo e definição da rotina de atualização.

**Fase 3 — Configuração dos agentes e da orquestração.** Ajuste do escopo e das instruções de cada agente sobre a base real, montagem do fluxo de roteamento e refinamento a partir de consultas reais.

**Fase 4 — Homologação.** Testes assistidos com a equipe comercial, correção de desvios e validação dos casos críticos.

**Fase 5 — Capacitação e entrada em produção.** Treinamento da equipe, liberação para uso e início do período de acompanhamento.

---

## 8. Investimento

### 8.1 Prova de conceito

Construída como demonstração, sem custo para a Rodavale. Ela existe para que a decisão de contratar seja tomada sobre algo funcionando, e não sobre uma descrição.

### 8.2 Modelo de contratação

**Assinatura mensal de R$ 4.500, com compromisso de doze meses. Sem investimento inicial.**

A implantação não é cobrada como projeto. Ela está incluída na assinatura, que cobre:

| Incluído na assinatura | Observação |
|---|---|
| Implantação e configuração | Agentes, orquestração e bases sobre o catálogo real |
| Integração com o ERP | Extração, carga completa e rotina de atualização |
| Sustentação | Correção de desvios e disponibilidade do assistente |
| Evolução | Ajuste de instruções, novas regras e refinamento a partir do uso real |

A escolha do modelo é deliberada. Uma implantação cobrada à vista concentra o risco no cliente, que paga antes de ver o resultado em operação. Na assinatura, a remuneração do fornecedor depende de o assistente continuar em pé e em uso.

**O primeiro mês é a descoberta.** Nele são levantados o ERP, o catálogo completo, o volume de atendimento e os perfis de acesso. Ao final, o valor da assinatura é confirmado ou ajustado, com a composição aberta, antes de o compromisso de doze meses passar a valer. Alterações de escopo identificadas depois dessa etapa seguem a regra da seção 11.

### 8.3 Custo de consumo em nuvem

Não está incluído na assinatura. É faturado pelo provedor diretamente à Rodavale e **dimensionado com a Calculadora do Azure**, conforme volume de consultas, tokens por consulta e uso de File Search.

Os fatores que determinam esse custo são:

| Fator | Observação |
|---|---|
| Volume de consultas | Estimativa inicial de 6.000 por mês, com base em 9 vendedores e 30 atendimentos diários |
| Tokens por consulta | Depende do tamanho das respostas e dos trechos recuperados das bases; medido sobre uso real |
| File Search | Cobrado à parte do consumo do modelo, conforme armazenamento indexado e uso de busca |
| Tipo de projeto e região | Afetam o preço unitário dos componentes |
| Recursos da integração | Banco de dados e rotina de atualização, quando a sincronização com o ERP entrar em escopo |

A medição do consumo real durante a prova de conceito e nos primeiros 90 dias de operação é o que permite converter esses fatores em um valor mensal confiável.

Referências: documentação do File Search e orientação de gestão de custos do Microsoft Foundry.

---

## 9. Retorno Esperado

### 9.1 Ganho de produtividade

A redução estimada do tempo médio de atendimento é de 11 para 7 minutos — quatro minutos por contato. Considerando 270 atendimentos diários e 22 dias úteis:

| Base de cálculo | Valor |
|---|---:|
| Atendimentos por dia | 270 |
| Minutos economizados por atendimento | 4 |
| Horas economizadas por mês | 396 |
| Custo-hora médio do televendas (com encargos) | R$ 25 |
| **Economia mensal estimada** | **R$ 9.900** |

### 9.2 Relação entre custo e ganho

| | Valor mensal |
|---|---:|
| Assinatura | R$ 4.500 |
| Economia estimada | R$ 9.900 |
| **Diferença** | **R$ 5.400** |

Sem investimento inicial, não há prazo de retorno a recuperar: a relação é positiva desde o primeiro mês em que a economia se concretizar. O número de R$ 9.900, porém, é **premissa de pré-venda, não medição**. A descoberta e os primeiros noventa dias de uso são o que converte essa premissa em dado — inclusive para baixo, se for o caso. O consumo em nuvem da seção 8.3 entra nessa conta assim que for dimensionado.

### 9.3 Ganhos adicionais não quantificados

**Recuperação de vendas perdidas por demora.** Parte dos 6% de pedidos hoje perdidos tende a ser convertida com resposta mais rápida.

**Redução do tempo de formação.** Novos vendedores tornam-se produtivos sem depender de anos de memorização de catálogo.

**Redução de devoluções.** Menos erro de aplicação significa menos retrabalho no pós-venda e menor custo logístico.

**Mitigação de risco.** O conhecimento deixa de estar concentrado em indivíduos.

---

## 10. Evolução Prevista

Esta proposta contempla a primeira fase. As etapas seguintes ficam registradas como evolução natural, a serem avaliadas após a consolidação do uso:

| Etapa | Descrição |
|---|---|
| Sincronização com o ERP | Atualização automática de catálogo, estoque e preços, eliminando a carga manual e substituindo a base estática por consulta ao dado vigente |
| Novos domínios | Inclusão de agentes para outras áreas da Rodavale, como RH ou financeiro, reaproveitando o mesmo orquestrador |
| Publicação no Teams | Disponibilização do assistente no ambiente onde a equipe já trabalha |
| Atendimento ao cliente final | Extensão do assistente ao WhatsApp, permitindo consulta direta pelas oficinas fora do expediente |
| Registro de pedido | Capacidade de iniciar o pedido a partir da conversa, com confirmação do vendedor |
| Análise de demanda | Uso do histórico de consultas para identificar peças procuradas e não disponíveis em estoque |

---

## 11. Premissas e Condições

- A Rodavale disponibilizará acesso aos dados de catálogo, estoque, clientes e tabelas de preço em formato estruturado.
- Será designado um responsável pela área comercial como ponto focal para validação funcional.
- A equipe de TI da Rodavale participará das fases de estruturação e homologação.
- Os custos de consumo dos serviços em nuvem são de responsabilidade da Rodavale e faturados diretamente pelo provedor, dimensionados conforme a seção 8.3. Eles não integram a assinatura.
- A qualidade das respostas do assistente é proporcional à qualidade e completude dos dados de aplicação veicular fornecidos.
- Enquanto a sincronização automática não for implantada, as bases de consulta representam uma posição datada, e não o estoque em tempo real.
- Alterações de escopo serão tratadas por aditivo, com estimativa de esforço previamente acordada.

---

## 12. Próximos Passos

1. **Reunião de alinhamento técnico.** Sessão com a equipe de TI para validar premissas de integração e acesso aos dados.
2. **Demonstração com dados da Rodavale.** Apresentação do assistente operando sobre uma amostra do catálogo real, para validação prática antes da contratação.
3. **Aprovação e início.** Assinatura da proposta e início do primeiro mês, dedicado à descoberta.

**Demonstração disponível.** Uma versão funcional dos três agentes já foi construída sobre uma amostra representativa do catálogo de autopeças, com dados de aplicação veicular, estoque, clientes e tabelas de preço, com posição de referência em 20/08/2026. A demonstração pode ser conduzida a qualquer momento.

---

Kumulus · Proposta Comercial 2026-014 (revisão 2) · Rodavale Distribuidora de Autopeças
Documento confidencial — reprodução não autorizada
