/* ============================================================
   Rodavale Distribuidora de Autopecas
   Schema do catalogo — Azure SQL Database

   Ordem de criacao respeita as dependencias de FK.
   ============================================================ */

/* ------------------------------------------------------------
   Limpeza (permite reexecutar o script do zero)
   ------------------------------------------------------------ */
IF OBJECT_ID('dbo.precos_cliente', 'U') IS NOT NULL DROP TABLE dbo.precos_cliente;
IF OBJECT_ID('dbo.aplicacoes', 'U')     IS NOT NULL DROP TABLE dbo.aplicacoes;
IF OBJECT_ID('dbo.estoque', 'U')        IS NOT NULL DROP TABLE dbo.estoque;
IF OBJECT_ID('dbo.produtos', 'U')       IS NOT NULL DROP TABLE dbo.produtos;
IF OBJECT_ID('dbo.clientes', 'U')       IS NOT NULL DROP TABLE dbo.clientes;
GO

/* ------------------------------------------------------------
   produtos — o catalogo de SKUs
   ------------------------------------------------------------ */
CREATE TABLE dbo.produtos (
    sku             VARCHAR(20)   NOT NULL PRIMARY KEY,
    descricao       VARCHAR(200)  NOT NULL,
    marca           VARCHAR(60)   NOT NULL,
    categoria       VARCHAR(60)   NOT NULL,
    posicao         VARCHAR(30)   NULL,          -- dianteira, traseira, esquerda...
    preco_base      DECIMAL(10,2) NOT NULL,
    unidade         VARCHAR(10)   NOT NULL DEFAULT 'UN',
    codigo_original VARCHAR(40)   NULL,          -- codigo da montadora, quando existe
    ativo           BIT           NOT NULL DEFAULT 1
);
GO

CREATE INDEX ix_produtos_categoria ON dbo.produtos (categoria);
CREATE INDEX ix_produtos_marca     ON dbo.produtos (marca);
GO

/* ------------------------------------------------------------
   aplicacoes — qual SKU serve qual veiculo
   Esta e a tabela central: resolve "que peca serve no meu carro".
   Um SKU serve varios veiculos; um veiculo aceita varios SKUs.
   ------------------------------------------------------------ */
CREATE TABLE dbo.aplicacoes (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    sku           VARCHAR(20)  NOT NULL,
    montadora     VARCHAR(40)  NOT NULL,
    modelo        VARCHAR(60)  NOT NULL,
    motorizacao   VARCHAR(20)  NULL,             -- 1.0, 1.4, 2.0 ...
    ano_inicio    SMALLINT     NOT NULL,
    ano_fim       SMALLINT     NULL,             -- NULL = ainda em linha
    observacao    VARCHAR(200) NULL,
    CONSTRAINT fk_aplicacoes_produto FOREIGN KEY (sku) REFERENCES dbo.produtos (sku)
);
GO

CREATE INDEX ix_aplicacoes_veiculo ON dbo.aplicacoes (montadora, modelo, ano_inicio, ano_fim);
CREATE INDEX ix_aplicacoes_sku     ON dbo.aplicacoes (sku);
GO

/* ------------------------------------------------------------
   estoque — saldo por SKU e filial
   ------------------------------------------------------------ */
CREATE TABLE dbo.estoque (
    sku             VARCHAR(20) NOT NULL,
    filial          VARCHAR(40) NOT NULL,
    quantidade      INT         NOT NULL DEFAULT 0,
    estoque_minimo  INT         NOT NULL DEFAULT 0,
    localizacao     VARCHAR(20) NULL,             -- endereco no CD: rua/prateleira
    CONSTRAINT pk_estoque PRIMARY KEY (sku, filial),
    CONSTRAINT fk_estoque_produto FOREIGN KEY (sku) REFERENCES dbo.produtos (sku)
);
GO

/* ------------------------------------------------------------
   clientes — oficinas, autocenters, frotistas
   ------------------------------------------------------------ */
CREATE TABLE dbo.clientes (
    codigo          VARCHAR(15)  NOT NULL PRIMARY KEY,
    razao_social    VARCHAR(150) NOT NULL,
    nome_fantasia   VARCHAR(100) NULL,
    tipo            VARCHAR(30)  NOT NULL,        -- oficina, autocenter, retifica, frotista
    cidade          VARCHAR(60)  NOT NULL,
    uf              CHAR(2)      NOT NULL,
    tabela_preco    VARCHAR(20)  NOT NULL,        -- A, B ou C
    limite_credito  DECIMAL(12,2) NOT NULL DEFAULT 0,
    ativo           BIT          NOT NULL DEFAULT 1
);
GO

/* ------------------------------------------------------------
   precos_cliente — desconto por tabela e categoria
   O preco final = preco_base * (1 - desconto_percentual/100)
   ------------------------------------------------------------ */
CREATE TABLE dbo.precos_cliente (
    id                   INT IDENTITY(1,1) PRIMARY KEY,
    tabela_preco         VARCHAR(20)  NOT NULL,
    categoria            VARCHAR(60)  NOT NULL,
    desconto_percentual  DECIMAL(5,2) NOT NULL DEFAULT 0,
    CONSTRAINT uq_precos_cliente UNIQUE (tabela_preco, categoria)
);
GO

CREATE INDEX ix_precos_cliente_tabela ON dbo.precos_cliente (tabela_preco);
GO
