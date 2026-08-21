# Agente de Consulta ao Catálogo de Autopeças

Assistente conversacional que responde, em linguagem natural, quais peças de reposição atendem determinado veículo — com marca, preço, saldo em estoque e restrições técnicas de aplicação.

Construído sobre **Microsoft Foundry**, com dados em **Azure SQL Database** expostos por um servidor **MCP (Model Context Protocol)** hospedado em **Azure Container Apps**.

---

## O problema

No mercado de reposição automotiva, o catálogo é organizado por código e descrição. O cliente, porém, pensa por veículo: *"preciso de pastilha de freio para um Onix 2018 1.4"*.

Essa tradução — de veículo para SKU — costuma acontecer na memória de vendedores experientes ou em catálogos de fabricante dispersos. O resultado é atendimento lento, dependência de poucas pessoas e erro de aplicação.

Este projeto torna esse conhecimento consultável.

---

## O que o assistente faz

| Pergunta | Resposta |
|---|---|
| *"Que pastilha serve num Onix 2018 1.4?"* | Peças aplicáveis com marca, posição, preço e estoque, ordenadas por preço |
| *"Tem estoque do RV-1002?"* | Saldo por filial, com localização física |
| *"Quanto fica para o cliente CLI-0001?"* | Preço final já com o desconto da tabela comercial |
| *"Preciso de amortecedor"* | Solicita o veículo antes de responder |
| *"Tem turbina para Ferrari?"* | Informa que não há peças para essa montadora |

**Exemplo de resposta real:**

```
Para Onix 2018 1.4, encontrei estas opções de pastilha de freio dianteira:

SKU       Marca      Posição     Preço      Estoque
RV-1002   TRW        Dianteira   R$  79,77  36
RV-1001   Bosch      Dianteira   R$ 231,66   5
RV-1005   Controil   Dianteira   R$ 245,50  18
RV-1006   Varga      Dianteira   R$ 258,51  43
RV-1004   Cobreq     Dianteira   R$ 288,47  18

Observações:
- RV-1006: somente versões com ar-condicionado
- RV-1004: estoque zerado no CD, 18 un. na Filial Campos
```

---

## Arquitetura

```
Vendedor
   │  linguagem natural
   ▼
Foundry Agent Service  ·  GPT-5.4-mini
   │  Model Context Protocol / HTTPS
   ▼
Azure Container Apps  →  SQL MCP Server (Data API Builder)
   │  TDS
   ▼
Azure SQL Database  ·  Brazil South
```

| Camada | Componente | Função |
|---|---|---|
| Agente | Foundry Agent Service | Interpreta a pergunta e orquestra as consultas |
| Modelo | GPT-5.4-mini | Compreensão de linguagem natural |
| Integração | Data API Builder 2.0.12 | Expõe o banco como ferramentas MCP tipadas |
| Hospedagem | Azure Container Apps | Executa a camada de integração |
| Dados | Azure SQL Database | Catálogo, aplicações, estoque, clientes e preços |

**Nenhum código de aplicação foi escrito.** A camada de integração é gerada a partir de configuração declarativa; o comportamento do agente é definido por instruções em linguagem natural.

---

## Estrutura do repositório

```
.
├── database/
│   ├── 01_schema.sql        # DDL das tabelas e views
│   ├── 02_dados.sql         # Carga de dados de demonstração
│   ├── gerar_dados.py       # Gerador dos dados fictícios
│   └── validar.py           # Validação das consultas do agente
├── integracao/
│   ├── dab-config.json      # Configuração do Data API Builder
│   └── Dockerfile           # Imagem da camada de integração
├── agente/
│   └── instrucoes.md        # Instruções que definem o comportamento do agente
└── documentos/
    ├── Proposta-Comercial.pdf
    ├── Documentacao-Tecnica.pdf
    └── Apresentacao.pptx
```

---

## Modelo de dados

| Tabela | Conteúdo |
|---|---|
| `produtos` | Catálogo: SKU, descrição, marca, categoria, posição, preço base |
| `aplicacoes` | **Relação peça–veículo**: montadora, modelo, motorização, faixa de anos |
| `estoque` | Saldo, estoque mínimo e localização por filial |
| `clientes` | Cadastro comercial com tabela de preço aplicável |
| `precos_cliente` | Desconto por combinação de tabela e categoria |

Duas views consolidam as regras de negócio:

- **`vw_pecas_veiculo`** — aplicação + produto + estoque numa linha só
- **`vw_preco_cliente`** — preço final já com desconto calculado

A base de demonstração contém 194 produtos, 3.367 aplicações veiculares, 388 registros de estoque e 90 clientes.

---

## Como reproduzir

**Pré-requisitos:** Azure CLI, .NET SDK 9, .NET Runtime 8, Data API Builder CLI.

### 1. Provisionar os recursos

```bash
az group create --name rg-rodavale --location brazilsouth

az sql server create --name <servidor> --resource-group rg-rodavale \
  --location brazilsouth --admin-user <usuario> --admin-password <senha>

az sql db create --name rodavale --server <servidor> \
  --resource-group rg-rodavale --service-objective Basic
```

### 2. Carregar o banco

Execute `database/01_schema.sql` e depois `database/02_dados.sql` contra o banco criado.

### 3. Publicar a camada de integração

```bash
export DAB_CONN="<connection string>"

az acr create --name <registry> --resource-group rg-rodavale --sku Basic --admin-enabled true
az acr build --registry <registry> --image rodavale-mcp:v1 ./integracao

az containerapp env create --name env-rodavale --resource-group rg-rodavale --location brazilsouth

az containerapp create --name ca-rodavale-mcp --resource-group rg-rodavale \
  --environment env-rodavale --image <registry>.azurecr.io/rodavale-mcp:v1 \
  --target-port 5000 --ingress external --env-vars "DAB_CONN=$DAB_CONN"
```

### 4. Configurar o agente

No portal do Microsoft Foundry: criar o agente, adicionar uma ferramenta MCP apontando para `https://<container>/mcp` e colar o conteúdo de `agente/instrucoes.md` no campo de instruções.

> A connection string nunca é gravada em arquivo nem embutida na imagem — é referenciada por `@env('DAB_CONN')` e injetada como variável de ambiente do container.

---

## Decisões técnicas

**Componentes gerenciados em vez de código proprietário.**
O cliente do cenário tem dois profissionais de TI. Propor código próprio significaria transferir a ele um passivo de manutenção. A camada de integração é gerada por configuração, não programada.

**Views resolvendo as regras de negócio.**
As primeiras tentativas falhavam: o agente montava filtros OData compostos — com intervalos de ano e tratamento de nulo — e errava a sintaxe. Mover essa lógica para views no banco fez o agente executar consultas simples e planas. Menos superfície para erro.

**Modelo mini.**
A tarefa é orquestração e formatação, não raciocínio complexo. Um modelo de maior capacidade elevaria o custo por consulta sem ganho mensurável.

**Somente leitura.**
Todas as entidades são publicadas apenas com permissão de consulta. Não existe caminho técnico para o agente alterar dados — a operação transacional permanece no ERP.

**Brazil South.**
Banco e camada de integração no Brasil, atendendo requisito de residência de dados.

---

## Limitações conhecidas

| Limitação | Encaminhamento |
|---|---|
| Endpoint de integração público e sem autenticação | Identidade gerenciada e restrição de rede |
| Carga de dados manual | Sincronização automatizada com o ERP |
| Consumo de ~17 mil tokens por consulta | Redução de contexto e cache de descoberta de esquema |
| Base de demonstração é amostra do catálogo | Carga completa na implantação |

---

## Contexto

Projeto desenvolvido como desafio técnico, simulando um ciclo completo de pré-vendas e entrega: definição de um cliente, diagnóstico de um problema real do setor, elaboração de proposta comercial com arquitetura e investimento, e implementação da solução.

A empresa **Rodavale Distribuidora de Autopeças** é fictícia. Os dados de catálogo são gerados, mas modelados a partir de peças, marcas e veículos reais do mercado de reposição brasileiro.

Os documentos comerciais e técnicos estão em [`documentos/`](./documentos).

---

## Autor

**Rafael Tomiazi** — [github.com/RafaelTomiazi](https://github.com/RafaelTomiazi)
