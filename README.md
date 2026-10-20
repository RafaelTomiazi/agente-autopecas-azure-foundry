# Assistente Multiagente de Televendas — Autopeças

Arquitetura multiagente sobre **Microsoft Foundry**, configurada inteiramente no portal, sem código. Um agente orquestrador identifica o domínio da pergunta do vendedor e um fluxo visual encaminha para o especialista adequado.

---

## O problema

No mercado de reposição automotiva, o catálogo é organizado por código e descrição. O cliente, porém, pensa por veículo: *"preciso de pastilha de freio para um Onix 2018 1.4"*.

Essa tradução — de veículo para SKU — costuma acontecer na memória de vendedores experientes ou em catálogos de fabricante dispersos. O resultado é atendimento lento, dependência de poucas pessoas e erro de aplicação.

Este projeto torna esse conhecimento consultável.

---

## Arquitetura

```
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

| Agente | Responsabilidade | Conhecimento |
|---|---|---|
| `orquestrador-rodavale` | Classifica a solicitação e devolve a rota | Nenhum. Sem ferramentas e sem arquivos |
| `especialista-catalogo-estoque-rodavale` | Compatibilidade, SKU, marca, preço-base e saldo | Catálogo completo + índice de SKUs |
| `especialista-comercial-rodavale` | Cliente, tabela de preço, desconto e cotação | Base de clientes e condições comerciais |

| Camada | Componente |
|---|---|
| Orquestração | Workflow do Foundry — roteamento por condição Power Fx |
| Agentes | Foundry Agent Service |
| Modelo | GPT-5-mini |
| Conhecimento | File Search do Foundry |

**Nenhuma linha de código na solução.** Os agentes são definidos por instruções em texto, o conhecimento vem de arquivos indexados pela plataforma e o roteamento é um fluxo visual montado no portal.

---

## Como o roteamento funciona

O orquestrador não chama os especialistas. Ele apenas classifica e responde em formato fixo:

```
ROTA: CATALOGO

CONTEXTO: resumo objetivo dos dados informados pelo vendedor
```

A resposta é gravada na variável `rota_orquestrador` e lida pelo nó de condição:

```
StartsWith(Last(ShowColumns(Local.rota_orquestrador, Text)).Text, "ROTA: CATALOGO")
```

Quem executa o encaminhamento é o fluxo, não o modelo. O caminho percorrido fica explícito no diagrama e no rastreamento de cada execução.

---

## O que o assistente faz

| Pergunta | Rota | Resposta |
|---|---|---|
| *"Que pastilha dianteira serve num Onix 2018 1.4?"* | CATALOGO | Peças aplicáveis com marca, SKU, posição, preço-base e estoque |
| *"Qual a tabela de preço da Auto Center Central?"* | COMERCIAL | Tabela do cliente e descontos por categoria |
| *"Faça uma cotação da RV-1002 para a Auto Center Central"* | COTACAO | Catálogo entrega o handoff técnico, Comercial aplica o desconto |
| *"Preciso de amortecedor"* | CATALOGO | Solicita montadora, modelo e ano antes de responder |
| *"Qual a previsão do tempo?"* | Else | Mensagem padrão sobre o escopo do assistente |

---

## Validação

Bateria executada no Preview do workflow, com gabarito conferido nas bases.

| # | Pergunta | Esperado | Status |
|---|---|---|---|
| 1 | Pastilhas dianteiras para Onix 2018 1.4 | RV-1001, RV-1002, RV-1004, RV-1005, RV-1006 — sem o RV-1003 (motor 1.0) | Aprovado |
| 2 | Tabela de preço da Auto Center Central | CLI-0008, tabela A | Aprovado |
| 3 | Cotação da RV-1002 para a Auto Center Central | R$ 79,77 − 19,63% = R$ 64,11 | Aprovado |
| 4 | Previsão do tempo | Mensagem de fora de escopo | Aprovado |
| 5 | "Preciso de amortecedor" + "Onix 2016 1.4, dianteiro" | RV-1037, RV-1038, RV-1040 — sem o RV-1041 (até 2015) | Aprovado |
| 6 | Pastilhas para Kia Sportage 2020 | Informa que não encontrou, sem inventar | Aprovado |

---

## Estrutura do repositório

```
.
├── agentes/
│   ├── orquestrador.md                    # Instruções do orquestrador
│   ├── especialista-catalogo-estoque.md   # Instruções do especialista de catálogo
│   ├── especialista-comercial.md          # Instruções do especialista comercial
│   └── workflow.md                        # Configuração dos nós e condições
├── conhecimento/
│   ├── catalogo_estoque_rodavale.md       # 3.367 aplicações veiculares
│   ├── indice_skus_rodavale.md            # Índice compacto por SKU
│   └── clientes_precos_rodavale.md        # 90 clientes e 24 regras de desconto
├── documentos/
│   ├── proposta-comercial.md              # Fonte da proposta
│   ├── documentacao-tecnica.md            # Fonte da documentação
│   ├── apresentacao-conteudo.md           # Fonte da apresentação
│   ├── Proposta-Rodavale-Kumulus.pdf
│   ├── Documentacao-Tecnica-Rodavale.pdf
│   └── Apresentacao-Rodavale.pptx
├── configuracao_foundry_sem_codigo.md     # Rascunho da configuração, anterior a agentes/
├── database/                              # Versão 1 e preparação dos dados
│   ├── 01_schema.sql                      # DDL das tabelas e views
│   ├── 02_dados.sql                       # Carga dos dados de demonstração
│   ├── gerar_dados.py                     # Gerador dos dados fictícios
│   └── validar.py                         # Validação das consultas da versão 1
└── integracao/                            # Versão 1: servidor MCP
    ├── dab-config.json                    # Configuração do Data API Builder
    └── Dockerfile                         # Imagem publicada no Azure Container Apps
```

`database/` e `integracao/` pertencem à versão 1 e à preparação dos dados. Não fazem parte da solução entregue e ficam como registro técnico.

---

## Bases de conhecimento

| Arquivo | Conteúdo |
|---|---|
| `catalogo_estoque_rodavale.md` | Montadora, modelo, motorização, faixa de anos, SKU, peça, marca, categoria, posição, preço-base e estoque por filial |
| `indice_skus_rodavale.md` | Uma linha por SKU, para consulta direta por código |
| `clientes_precos_rodavale.md` | Cliente, tabela de preço atribuída e desconto por categoria |

**Por que dois arquivos de catálogo.** O arquivo completo responde bem por veículo, porque as linhas de um mesmo modelo ficam próximas e a busca recupera o bloco certo. Ele falhou ao procurar um SKU isolado entre 3.367 linhas, e a cotação quebrava. O índice compacto resolveu esse caso.

Convenções: `Ano final` igual a **9999** indica veículo em linha; `Motor` igual a **TODAS** indica que a peça atende todas as versões. Os dados são uma posição de referência em **20/08/2026**, sem atualização em tempo real.

---

## Como reproduzir

Não há infraestrutura a provisionar. Tudo é feito no portal do Microsoft Foundry.

1. **Criar os três agentes** com o modelo `gpt-5-mini`, colando as instruções de `agentes/`. O `gpt-6-astra` não suporta File Search.
2. **Anexar o conhecimento**: em Tools, adicionar File search e enviar `catalogo_estoque_rodavale.md` e `indice_skus_rodavale.md` ao especialista de catálogo, e `clientes_precos_rodavale.md` ao comercial. O orquestrador fica sem ferramentas e sem arquivos.
3. **Criar o workflow**: Agents → Workflows → Create → Blank workflow. Montar Start, nó do orquestrador, nó If/else com as quatro rotas e End, conforme `agentes/workflow.md`.
4. **Salvar e testar** no Preview, com a bateria da seção Validação. O Foundry não salva sozinho.

---

## Decisões técnicas

**Três agentes em vez de um.** Um agente com todos os assuntos mistura domínios: aplica desconto sem confirmar a peça, sugere peça sem checar a aplicação. Com escopos separados, o erro fica fácil de localizar.

**Orquestrador sem ferramentas.** Ele só classifica. Sem arquivos, não tem como inventar preço ou estoque. Na primeira versão das instruções ele chegou a incluir preço e desconto no contexto, dados que não possuía.

**Roteamento por condição, não por decisão do modelo.** O recurso Connected Agents, que deixava o próprio modelo delegar, ficou restrito ao portal clássico do Foundry, já descontinuado. O roteamento explícito é mais trabalhoso de montar, mas auditável.

**Modelo mini.** A tarefa é classificar, buscar em arquivo e formatar. Modelo maior custaria mais sem ganho.

---

## Limitações conhecidas

| Limitação | Encaminhamento |
|---|---|
| Base é uma posição datada, sem tempo real | Sincronização automatizada com o ERP |
| Bases indexadas em East US | Provisionamento em Brazil South na implantação |
| Sem controle de acesso por perfil | Restrição do acesso ao projeto em produção |
| Até dez opções por resposta | O agente oferece refinamento por marca, filial ou preço |
| A linha ROTA aparece no chat | Comportamento da plataforma: os agentes compartilham a conversa |
| Workflows do Foundry saem em 01/12/2026 | Migrar o roteamento para Microsoft Agent Framework ou Azure Logic Apps |

Os agentes e as bases não são afetados pela retirada dos Workflows. O que precisará ser refeito é a camada de roteamento.

---

## Evolução: versão 1 → versão 2

A primeira versão era um agente único consultando um **Azure SQL Database** através de um servidor **MCP** (Data API Builder) hospedado em **Azure Container Apps**. Ela funcionava. Os scripts de banco estão em [`database/`](./database) e a configuração do Data API Builder e o Dockerfile em [`integracao/`](./integracao). O histórico de commits deste repositório mostra as duas versões.

A revisão do desafio pediu uma arquitetura multiagente configurada no portal, sem código. A troca foi feita para atender ao requisito de configuração sem código. O que se ganhou: nenhuma infraestrutura a manter e nenhum código na entrega. O que se perdeu: consulta ao dado vigente e filtro exato por SQL, substituídos por busca em arquivo sobre uma base datada.

---

## Contexto

Projeto desenvolvido como desafio técnico, simulando um ciclo completo de pré-vendas e entrega: definição de um cliente, diagnóstico de um problema real do setor, elaboração de proposta comercial com arquitetura e investimento, e implementação da solução.

A empresa **Rodavale Distribuidora de Autopeças** é fictícia. Os dados de catálogo são gerados por script, mas modelados a partir de peças, marcas e veículos reais do mercado de reposição brasileiro. Essa geração é anterior à solução: nenhum código é executado durante o atendimento.

Os documentos comerciais e técnicos estão em [`documentos/`](./documentos).

---

## Autor

**Rafael Tomiazi** — [github.com/RafaelTomiazi](https://github.com/RafaelTomiazi)
