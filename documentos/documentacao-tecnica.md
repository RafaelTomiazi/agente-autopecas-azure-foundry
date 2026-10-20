# Documentação Técnica da Solução

**Assistente Inteligente de Consulta ao Catálogo**

Cliente: Rodavale Distribuidora de Autopeças Ltda.
Plataforma: Microsoft Foundry
Versão do documento: 2.0
Público: Equipe técnica e responsáveis pela sustentação

Documento técnico de referência. Complementa a Proposta Comercial 2026-014 (revisão 2).

---

## 1. Visão Geral

Este documento descreve a arquitetura, os componentes e as decisões técnicas da solução de assistente conversacional construída para o televendas da Rodavale. Destina-se à equipe de sustentação e a qualquer profissional que precise operar, auditar ou evoluir a solução.

A solução é uma arquitetura multiagente: um agente orquestrador classifica a pergunta do vendedor e um fluxo visual encaminha a solicitação para o especialista adequado. Toda resposta é derivada de consulta às bases de conhecimento — não há geração de conteúdo sem lastro.

**O que mudou em relação à versão 1.0.** A primeira versão era um agente único que consultava um banco Azure SQL através de um servidor MCP hospedado em Azure Container Apps. A versão atual atende ao requisito de configuração sem código: os três agentes, suas bases de conhecimento e o roteamento entre eles são definidos inteiramente no portal do Microsoft Foundry. A seção 9 registra o que se ganhou e o que se perdeu nessa troca.

### 1.1 Componentes

| Componente | Serviço | Responsabilidade |
|---|---|---|
| Orquestrador | Foundry Agent Service | Classifica a solicitação e devolve a rota |
| Especialista de Catálogo e Estoque | Foundry Agent Service | Compatibilidade, SKU, marca, preço-base e saldo |
| Especialista Comercial | Foundry Agent Service | Cliente, tabela de preço, desconto e cotação indicativa |
| Modelo | Foundry Models — GPT-5-mini | Compreensão de linguagem natural nos três agentes |
| Conhecimento | File Search do Foundry | Indexação e busca nos arquivos de conhecimento |
| Orquestração | Workflow do Foundry (Preview) | Roteamento condicional entre os agentes |

### 1.2 Ambiente

Projeto Foundry `rafaeltomiazi-0258`, grupo de recursos `rg-rafael-tomiazi`, região `eastus` (por disponibilidade de modelos). Nesta configuração não há banco de dados nem serviço de integração provisionado: as bases de conhecimento são arquivos indexados pela própria plataforma.

---

## 2. Arquitetura

### 2.1 Desenho do fluxo

```text
Start
  |
  v
orquestrador-rodavale                       (devolve ROTA e CONTEXTO)
  |
  v
If / else condition
  |
  +-- ROTA: CATALOGO   --> especialista-catalogo-estoque-rodavale ---+
  |                                                                  |
  +-- ROTA: COTACAO    --> especialista-catalogo-estoque-rodavale    |
  |                            |                                     |
  |                            v                                     |
  |                        especialista-comercial-rodavale ----------+
  |                                                                  |
  +-- ROTA: COMERCIAL  --> especialista-comercial-rodavale ----------+
  |                                                                  |
  +-- Else             --> mensagem padrão de fora de escopo --------+
                                                                     |
                                                                     v
                                                                    End
```

### 2.2 Como o roteamento funciona

O orquestrador não chama os especialistas. Ele apenas classifica a pergunta e responde em formato fixo:

```text
ROTA: CATALOGO

CONTEXTO: resumo objetivo dos dados informados pelo vendedor
```

A resposta é gravada na variável `rota_orquestrador` do workflow. O nó de condição lê essa variável e decide o caminho. Quem executa o encaminhamento é o fluxo, não o modelo.

Essa é uma diferença importante em relação ao recurso Connected Agents, que existia no portal clássico e permitia que o próprio modelo decidisse a delegação. Esse recurso não está disponível no Foundry atual (ver seção 10). A consequência prática é positiva para auditoria: o caminho percorrido é explícito, visível no diagrama e verificável no rastreamento de cada execução.

### 2.3 Expressões de condição

As condições usam Power Fx. A variável que guarda a saída do agente é uma tabela de mensagens, e não um texto simples, o que exige selecionar a coluna e pegar a última mensagem:

```text
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: CATALOGO")
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: COTACAO")
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: COMERCIAL")
```

O caminho `Else` não tem condição: ele atende tanto solicitações fora do escopo quanto qualquer resposta do orquestrador que não siga o formato esperado.

### 2.4 Configuração dos nós

| Nó | Agente | Entrada | Saída salva em |
|---|---|---|---|
| 1 | orquestrador-rodavale | `System.LastMessageText` | `rota_orquestrador` |
| CATALOGO | especialista-catalogo-estoque-rodavale | `rota_orquestrador` | — |
| COTACAO (1º) | especialista-catalogo-estoque-rodavale | `rota_orquestrador` | `resposta_catalogo` |
| COTACAO (2º) | especialista-comercial-rodavale | `resposta_catalogo` | — |
| COMERCIAL | especialista-comercial-rodavale | `rota_orquestrador` | — |
| Else | Deliver a message | — | — |

Todos os nós de agente usam `System.ConversationId` como contexto de conversa. Por isso os agentes compartilham o mesmo histórico, o que permite que uma pergunta incompleta seja complementada na mensagem seguinte sem perder o contexto.

---

## 3. Bases de Conhecimento

As bases são arquivos Markdown indexados pelo File Search do Foundry, no índice `indice-catalogo-estoque-rodavale` (catálogo) e no índice do agente comercial.

| Arquivo | Tamanho | Conteúdo | Agente |
|---|---:|---|---|
| `catalogo_estoque_rodavale.md` | 1,2 MB | 3.367 aplicações veiculares, com montadora, modelo, motorização, faixa de anos, SKU, peça, marca, categoria, posição, preço-base e estoque por filial | Catálogo e Estoque |
| `indice_skus_rodavale.md` | 58 KB | Índice compacto por SKU, com descrição, marca, categoria, posição, preço-base e estoque | Catálogo e Estoque |
| `clientes_precos_rodavale.md` | 11 KB | 90 clientes, tabela de preço atribuída e 24 regras de desconto por categoria | Comercial |

### 3.1 Por que existem dois arquivos de catálogo

O arquivo grande responde bem a perguntas por veículo, porque as linhas de um mesmo modelo ficam próximas e a busca por trecho recupera o bloco certo. Ele falhou, porém, ao procurar um SKU isolado dentro de 3.367 linhas: a consulta pelo RV-1002 não retornava resultado, e a cotação quebrava.

O índice compacto resolve esse caso. Ele contém uma linha por SKU, o que torna a recuperação confiável. A instrução do agente define qual arquivo consultar em cada situação: índice de SKUs quando o vendedor informa um código, catálogo completo quando a pergunta é por veículo.

### 3.2 Convenções de preenchimento

- `Ano final` igual a **9999** indica veículo em linha; a aplicação é considerada vigente.
- `Motor` igual a **TODAS** indica que a peça atende todas as versões daquele modelo.
- Os dados representam uma posição de referência em **20/08/2026**. Não há atualização em tempo real, reserva ou confirmação de entrega.

### 3.3 Fórmula de precificação

```text
preco_final = preco_base × (1 − desconto_percentual / 100)
```

O desconto é determinado pelo cruzamento entre a tabela de preço do cliente (A, B ou C) e a categoria do produto.

### 3.4 Preparação dos dados de demonstração

Os dados da Rodavale são fictícios e foram gerados por script (`database/gerar_dados.py`), assim como os arquivos de conhecimento, extraídos desse mesmo conjunto. Essa preparação é anterior à solução e não faz parte dela: nenhum código é executado durante o atendimento. Em um cenário real, os arquivos seriam produzidos a partir da extração do ERP.

---

## 4. Configuração dos Agentes

### 4.1 Modelo

Foi selecionado o GPT-5-mini para os três agentes. A tarefa envolve interpretação de linguagem, busca em arquivo e formatação de resposta — não exige raciocínio complexo. Modelos de maior capacidade elevariam o custo por consulta sem ganho mensurável neste caso de uso.

Registro de compatibilidade: o modelo `gpt-6-astra` foi testado e não suporta a ferramenta File Search no portal, o que motivou a escolha do `gpt-5-mini`.

### 4.2 Orquestrador

| Diretriz | Objetivo |
|---|---|
| Responder somente com ROTA e CONTEXTO | Produzir uma saída que o fluxo consiga interpretar |
| Nunca responder à pergunta do vendedor | Impedir que o orquestrador opine sobre peça, preço ou qualquer assunto geral |
| Usar apenas fatos informados pelo vendedor | Evitar que ele inclua no contexto dados que não possui, como preço ou estoque |
| Classificar fora do escopo explicitamente | Garantir que assuntos alheios ao televendas sigam pelo caminho padrão |

Este agente não tem ferramentas nem arquivos. É deliberado: ele só classifica.

### 4.3 Especialista de Catálogo e Estoque

| Diretriz | Objetivo |
|---|---|
| Consultar o arquivo antes de responder | Impedir resposta gerada sem lastro |
| Aplicar todos os filtros | Ano dentro da faixa, motorização igual à pedida ou TODAS, posição e tipo de peça correspondentes |
| Apresentar até dez opções | Evitar omitir alternativas válidas quando há muitas compatíveis |
| Consultar o índice quando houver SKU | Tornar a busca por código determinística |
| Entregar apenas o handoff técnico na rota de cotação | Impedir que ele localize cliente, aplique desconto ou calcule preço final |
| Não oferecer reserva, pedido ou disponibilidade atual | Manter a resposta coerente com o caráter datado da base |

### 4.4 Especialista Comercial

| Diretriz | Objetivo |
|---|---|
| Consultar o arquivo antes de responder | Impedir resposta gerada sem lastro |
| Localizar o cliente por código, nome fantasia ou razão social | Cobrir as formas como o vendedor se refere ao cliente |
| Gerar a cotação a partir do handoff do Catálogo | Usar preço-base e categoria recebidos, sem redescobrir a peça |
| Considerar quantidade igual a uma unidade | Evitar pergunta desnecessária quando o vendedor não informa quantidade |
| Não confirmar compatibilidade ou estoque | Manter a fronteira com o domínio do Catálogo |
| Escrever valores monetários entre crases | Contornar uma limitação de renderização descrita na seção 9 |

### 4.5 Manutenção

Ajuste de comportamento não exige nova implantação. As instruções são editadas no portal e passam a valer na interação seguinte. O mesmo vale para o roteamento: incluir um novo domínio significa criar um agente, acrescentar uma rota no orquestrador e um caminho no fluxo.

---

## 5. Validação

Bateria executada no Preview do workflow, com gabarito extraído das bases.

| # | Pergunta | Resultado esperado | Status |
|---|---|---|---|
| 1 | Quais pastilhas de freio dianteiras servem no Chevrolet Onix 2018 1.4? | RV-1001, RV-1002, RV-1004, RV-1005 e RV-1006, sem o RV-1003 (motor 1.0) | Aprovado |
| 2 | Qual é a tabela de preço da Auto Center Central? | Cliente CLI-0008, tabela A | Aprovado |
| 3 | Faça uma cotação da RV-1002 para a Auto Center Central | Preço-base R$ 79,77, desconto de 19,63%, preço final R$ 64,11 | Aprovado |
| 4 | Qual é a previsão do tempo para amanhã? | Mensagem padrão de fora de escopo | Aprovado |
| 5 | "Preciso de amortecedor", depois "Onix 2016 1.4, dianteiro" | RV-1037, RV-1038 e RV-1040, sem o RV-1041 (válido até 2015) e sem os traseiros | Aprovado |
| 6 | Quais pastilhas servem numa Kia Sportage 2020? | Informar que não encontrou, sem sugerir peça | Aprovado |

Os testes 1, 5 e 6 verificam a precisão da busca em arquivo, que era o principal risco técnico da arquitetura sem banco de dados. O teste 5 verifica a preservação de contexto entre mensagens. O teste 3 verifica o encadeamento entre os dois especialistas.

---

## 6. Operação

### 6.1 Atualização do conhecimento

A carga é manual: gera-se o arquivo atualizado e envia-se ao índice do agente pelo portal, em Tools, Upload files. O índice aceita novos arquivos sem recriar o agente. A automação dessa sincronização está prevista como evolução.

### 6.2 Inclusão de um novo domínio

1. Criar o agente especialista com sua instrução e, se houver, seu arquivo de conhecimento.
2. Acrescentar a rota correspondente nas instruções do orquestrador.
3. Adicionar um caminho no nó de condição, com a expressão Power Fx da nova rota.
4. Ligar o caminho ao novo agente e salvar o workflow, que gera uma nova versão.

### 6.3 Monitoramento

| O que observar | Onde |
|---|---|
| Caminho percorrido em cada execução | Traces do workflow no portal |
| Erros de expressão ou de nó | Mensagem de falha na execução do workflow |
| Trecho de arquivo usado em cada resposta | Citações exibidas na resposta do agente |
| Consumo de tokens e custo | Painel de uso do projeto Foundry |

### 6.4 Versionamento

Cada Save do workflow cria uma versão imutável, acessível pelo seletor de versões. A versão validada nos testes descritos na seção 5 é a **versão 4** do workflow `televendas-rodavale`.

---

## 7. Segurança

**Sem alteração de dados.** Os agentes apenas consultam arquivos indexados. Não há gravação, nem caminho técnico para alterar cadastro, estoque ou preço.

**Escopo restrito por instrução.** Cada especialista responde somente dentro do seu domínio, e o caminho padrão trata qualquer assunto fora do televendas com mensagem fixa.

**Sem credenciais na solução.** Não há cadeia de conexão, chave de API ou segredo envolvido na configuração atual, uma vez que não existe serviço externo conectado.

**Rastreabilidade.** A plataforma registra cada execução do fluxo, os agentes acionados e as citações usadas na resposta.

**Ponto de atenção.** As bases de conhecimento contêm dados comerciais de clientes, incluindo tabelas de preço e descontos. O controle de acesso é o do próprio projeto Foundry: quem tem acesso ao projeto tem acesso às respostas. Em produção, o acesso deve ser restrito à equipe de televendas.

---

## 8. Infraestrutura da versão 1.0

Os recursos da primeira versão continuam provisionados e **não fazem parte da solução atual**:

| Recurso | Nome | Grupo de recursos | Situação |
|---|---|---|---|
| Azure SQL Database | `rodavale` em `sql-rodavale-rafael` | `rg-rafael-foundry` | Ativo, fora da solução |
| Azure Container App | `ca-rodavale-mcp` | `rg-rafael-foundry` | Ativo, fora da solução |
| Azure Container Registry | imagem do Data API Builder | `rg-rafael-foundry` | Ativo, fora da solução |

**Decisão pendente:** desligar esses recursos para encerrar o custo, ou mantê-los como base da evolução descrita na seção 11, que restabelece a consulta ao dado vigente. Enquanto a decisão não é tomada, eles continuam gerando custo sem uso.

Os artefatos dessa versão permanecem no repositório (`database/`, `integracao/`) como registro técnico.

---

## 9. Limitações Conhecidas

| Limitação | Impacto | Encaminhamento |
|---|---|---|
| Base é uma posição datada de 20/08/2026 | Estoque e preço podem divergir do ERP | Sincronização automatizada (seção 11) |
| Busca por trecho em arquivo grande | Falhou ao procurar SKU isolado no catálogo completo | Resolvido com o índice compacto de SKUs; novos casos podem exigir índices semelhantes |
| Limite de dez opções por resposta | Consultas com muitas peças compatíveis exibem apenas as dez primeiras | O agente oferece refinamento por marca, filial ou faixa de preço |
| A linha ROTA e CONTEXTO aparece no chat | O vendedor vê a classificação antes da resposta | Comportamento da plataforma, pois os agentes compartilham a conversa. Na demonstração, ajuda a evidenciar o roteamento |
| Renderização de valores monetários | O Preview interpretava `$` como fórmula matemática e quebrava o texto | Contornado com instrução para escrever valores entre crases |
| Sem controle de acesso por perfil | Qualquer usuário do projeto vê dados comerciais de clientes | Restrição de acesso ao projeto em produção |
| Bases indexadas na região East US | Não há residência de dados no Brasil nesta configuração. Os dados da prova de conceito são fictícios | Provisionamento em Brazil South na implantação produtiva |
| Base de demonstração é amostra do catálogo | Cobertura parcial de veículos e peças | Carga completa na implantação |

---

## 10. Prazos da Plataforma

Dois anúncios da Microsoft afetam a longevidade desta arquitetura e foram considerados na escolha:

| Recurso | Retirada anunciada | Efeito |
|---|---|---|
| Workflows do Foundry | 01/12/2026 | O roteamento visual usado nesta solução deixa de ser suportado no portal |
| Agentes e portal clássicos, onde existia o Connected Agents | 31/03/2027 | Não é alternativa de longo prazo |

O caminho indicado pela Microsoft para orquestração após essas datas é o Microsoft Agent Framework, que é baseado em código, ou o Azure Logic Apps, que é visual mas externo ao Foundry. Os agentes em si não são afetados: continuam válidos, com suas instruções e bases de conhecimento. O que precisará ser refeito é a camada de roteamento.

Essa é uma restrição da plataforma, não da solução: hoje não existe no Foundry um caminho de orquestração sem código com longevidade garantida. A arquitetura atual é a melhor opção disponível dentro da restrição de não usar código, e a migração do roteamento deve ser planejada para antes de dezembro de 2026.

---

## 11. Evolução Técnica

| Etapa | Descrição técnica |
|---|---|
| Sincronização automatizada | Rotina agendada de extração do ERP, regerando os arquivos de conhecimento ou restabelecendo a consulta direta ao banco |
| Retorno à consulta em tempo real | Reaproveitamento do Azure SQL e da camada Data API Builder da versão 1.0, quando a exigência de configuração sem código não for mais o critério dominante |
| Migração do roteamento | Substituição do Workflow por Microsoft Agent Framework ou Azure Logic Apps, antes de 01/12/2026 |
| Novos domínios | Inclusão de agentes de RH, financeiro ou suporte interno, reaproveitando o mesmo orquestrador |
| Publicação no Teams | Disponibilização do assistente no ambiente de trabalho da equipe |
| Controle de acesso | Restrição do projeto e, se necessário, separação de bases por perfil de usuário |
| Telemetria de negócio | Registro estruturado das consultas para identificar demanda por itens ausentes do catálogo ou sem estoque |

---

## 12. Referências

- Microsoft Foundry — Agent Service, File Search e Workflows
- Microsoft Foundry — aviso de retirada de Workflows e migração para o Microsoft Agent Framework
- Microsoft Foundry (clássico) — Connected Agents e aviso de retirada
- Power Fx — funções de texto e tabela usadas nas condições do fluxo

---

Kumulus · Documentação Técnica v2.0 · Rodavale Distribuidora de Autopeças
Documento confidencial — reprodução não autorizada
