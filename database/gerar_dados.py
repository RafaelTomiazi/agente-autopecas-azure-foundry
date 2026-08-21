"""
Gera os INSERTs de dados ficticios da Rodavale.
Saida: 02_dados.sql
"""
import random

random.seed(42)  # reprodutivel

FILIAIS = ["CD Duque de Caxias", "Filial Campos"]

# ---------------------------------------------------------------
# Veiculos populares no mercado de reposicao brasileiro
# (montadora, modelo, [motorizacoes], ano_inicio, ano_fim, popularidade)
# A popularidade reflete o volume de frota circulante: carros mais
# vendidos tem muito mais opcoes de peca no mercado de reposicao.
# ---------------------------------------------------------------
VEICULOS = [
    ("Chevrolet", "Onix",        ["1.0", "1.4"],        2012, 2019, 10),
    ("Chevrolet", "Onix Plus",   ["1.0"],               2019, None,  7),
    ("Chevrolet", "Prisma",      ["1.0", "1.4"],        2013, 2019,  6),
    ("Chevrolet", "Tracker",     ["1.0", "1.2"],        2020, None,  4),
    ("Chevrolet", "S10",         ["2.5", "2.8"],        2012, None,  4),
    ("Chevrolet", "Spin",        ["1.8"],               2012, None,  3),
    ("Volkswagen", "Gol",        ["1.0", "1.6"],        2008, 2023, 10),
    ("Volkswagen", "Polo",       ["1.0", "1.4"],        2018, None,  6),
    ("Volkswagen", "Virtus",     ["1.0", "1.4"],        2018, None,  5),
    ("Volkswagen", "T-Cross",    ["1.0", "1.4"],        2019, None,  4),
    ("Volkswagen", "Saveiro",    ["1.6"],               2010, None,  6),
    ("Volkswagen", "Amarok",     ["2.0"],               2011, None,  3),
    ("Fiat", "Uno",              ["1.0", "1.4"],        2010, 2021,  8),
    ("Fiat", "Palio",            ["1.0", "1.4"],        2004, 2017,  9),
    ("Fiat", "Argo",             ["1.0", "1.3"],        2017, None,  6),
    ("Fiat", "Mobi",             ["1.0"],               2016, None,  4),
    ("Fiat", "Strada",           ["1.4"],               2013, None,  9),
    ("Fiat", "Toro",             ["1.8", "2.0"],        2016, None,  5),
    ("Fiat", "Cronos",           ["1.3"],               2018, None,  4),
    ("Ford", "Ka",               ["1.0", "1.5"],        2014, 2021,  6),
    ("Ford", "Fiesta",           ["1.0", "1.6"],        2010, 2019,  6),
    ("Ford", "Ranger",           ["2.2", "3.2"],        2012, None,  3),
    ("Hyundai", "HB20",          ["1.0", "1.6"],        2012, None,  9),
    ("Hyundai", "Creta",         ["1.6", "2.0"],        2016, None,  5),
    ("Renault", "Sandero",       ["1.0", "1.6"],        2014, None,  6),
    ("Renault", "Logan",         ["1.0", "1.6"],        2013, None,  5),
    ("Renault", "Kwid",          ["1.0"],               2017, None,  5),
    ("Renault", "Duster",        ["1.6", "2.0"],        2011, None,  4),
    ("Toyota", "Corolla",        ["1.8", "2.0"],        2014, None,  7),
    ("Toyota", "Hilux",          ["2.7", "2.8"],        2016, None,  5),
    ("Toyota", "Etios",          ["1.3", "1.5"],        2012, 2021,  5),
    ("Honda", "Civic",           ["1.8", "2.0"],        2012, None,  5),
    ("Honda", "Fit",             ["1.4", "1.5"],        2009, 2021,  4),
    ("Honda", "HR-V",            ["1.8"],               2015, None,  4),
    ("Nissan", "Kicks",          ["1.6"],               2016, None,  4),
    ("Nissan", "Versa",          ["1.6"],               2015, None,  3),
    ("Jeep", "Renegade",         ["1.8", "2.0"],        2015, None,  5),
    ("Jeep", "Compass",          ["2.0"],               2017, None,  4),
    ("Peugeot", "208",           ["1.2", "1.6"],        2013, None,  3),
    ("Citroen", "C3",            ["1.2", "1.6"],        2012, None,  3),
]

def sortear_veiculos(_n=None):
    """
    Decide, veiculo a veiculo, se o SKU tem aplicacao nele.
    A chance e proporcional a popularidade: um Gol (10) aparece em cerca
    de 80% dos SKUs, um C3 (3) em cerca de 24%. Isso reproduz o mercado
    real, onde carros de frota grande tem muito mais opcoes de peca.
    """
    escolhidos = [v for v in VEICULOS if random.random() < v[5] / 12.5]
    # garante um minimo, caso o sorteio venha vazio
    if len(escolhidos) < 3:
        escolhidos = random.sample(VEICULOS, k=3)
    return escolhidos

# ---------------------------------------------------------------
# Tipos de peca: (descricao, categoria, posicao, faixa_preco, marcas)
# ---------------------------------------------------------------
MARCAS_FREIO   = ["Bosch", "TRW", "Fras-le", "Cobreq", "Controil", "Varga"]
MARCAS_SUSP    = ["Cofap", "Monroe", "Nakata", "SKF", "Axios"]
MARCAS_MOTOR   = ["Mahle", "Gates", "Continental", "Schadek", "MTE-Thomson"]
MARCAS_FILTRO  = ["Tecfil", "Wega", "Mahle", "Fram"]
MARCAS_ELET    = ["Bosch", "Magneti Marelli", "NGK", "Valeo", "Moura"]
MARCAS_ARREF   = ["Valeo", "Visconde", "MTE-Thomson", "Behr"]
MARCAS_TRANS   = ["Sachs", "Luk", "Valeo", "SKF"]

TIPOS_PECA = [
    ("Pastilha de freio",          "Freios",        "Dianteira",  75, 320, MARCAS_FREIO),
    ("Pastilha de freio",          "Freios",        "Traseira",   65, 260, MARCAS_FREIO),
    ("Disco de freio ventilado",   "Freios",        "Dianteira", 130, 520, MARCAS_FREIO),
    ("Disco de freio solido",      "Freios",        "Traseira",  110, 390, MARCAS_FREIO),
    ("Lona de freio",              "Freios",        "Traseira",   58, 190, MARCAS_FREIO),
    ("Cilindro mestre de freio",   "Freios",        None,        180, 640, MARCAS_FREIO),
    ("Amortecedor",                "Suspensao",     "Dianteira", 190, 720, MARCAS_SUSP),
    ("Amortecedor",                "Suspensao",     "Traseira",  160, 610, MARCAS_SUSP),
    ("Mola helicoidal",            "Suspensao",     "Dianteira", 140, 480, MARCAS_SUSP),
    ("Kit batente e coifa",        "Suspensao",     "Dianteira",  70, 240, MARCAS_SUSP),
    ("Coxim do amortecedor",       "Suspensao",     "Dianteira",  85, 290, MARCAS_SUSP),
    ("Bandeja da suspensao",       "Suspensao",     "Dianteira", 210, 690, MARCAS_SUSP),
    ("Pivo da suspensao",          "Suspensao",     "Dianteira",  62, 210, MARCAS_SUSP),
    ("Terminal de direcao",        "Direcao",       None,         58, 195, MARCAS_SUSP),
    ("Bieleta estabilizadora",     "Suspensao",     "Dianteira",  45, 160, MARCAS_SUSP),
    ("Correia dentada",            "Motor",         None,         75, 280, MARCAS_MOTOR),
    ("Kit correia dentada",        "Motor",         None,        220, 780, MARCAS_MOTOR),
    ("Bomba d agua",               "Motor",         None,        130, 460, MARCAS_MOTOR),
    ("Junta do cabecote",          "Motor",         None,        110, 420, MARCAS_MOTOR),
    ("Correia do alternador",      "Motor",         None,         38, 140, MARCAS_MOTOR),
    ("Tensor da correia",          "Motor",         None,        120, 390, MARCAS_MOTOR),
    ("Filtro de oleo",             "Filtros",       None,         22,  85, MARCAS_FILTRO),
    ("Filtro de ar do motor",      "Filtros",       None,         35, 130, MARCAS_FILTRO),
    ("Filtro de combustivel",      "Filtros",       None,         28, 145, MARCAS_FILTRO),
    ("Filtro de cabine",           "Filtros",       None,         32, 110, MARCAS_FILTRO),
    ("Vela de ignicao",            "Eletrica",      None,         26,  95, MARCAS_ELET),
    ("Bobina de ignicao",          "Eletrica",      None,        135, 480, MARCAS_ELET),
    ("Bateria 60Ah",               "Eletrica",      None,        380, 620, MARCAS_ELET),
    ("Alternador",                 "Eletrica",      None,        620, 1850, MARCAS_ELET),
    ("Motor de partida",           "Eletrica",      None,        540, 1620, MARCAS_ELET),
    ("Sensor de rotacao",          "Eletrica",      None,         95, 340, MARCAS_ELET),
    ("Radiador",                   "Arrefecimento", None,        310, 980, MARCAS_ARREF),
    ("Valvula termostatica",       "Arrefecimento", None,         48, 175, MARCAS_ARREF),
    ("Reservatorio de agua",       "Arrefecimento", None,         65, 210, MARCAS_ARREF),
    ("Eletroventilador",           "Arrefecimento", None,        290, 890, MARCAS_ARREF),
    ("Kit embreagem",              "Transmissao",   None,        420, 1450, MARCAS_TRANS),
    ("Rolamento de embreagem",     "Transmissao",   None,         95, 330, MARCAS_TRANS),
    ("Junta homocinetica",         "Transmissao",   None,        180, 620, MARCAS_TRANS),
    ("Coifa da homocinetica",      "Transmissao",   None,         38, 125, MARCAS_TRANS),
    ("Rolamento da roda",          "Suspensao",     "Dianteira",  88, 320, MARCAS_SUSP),
]

CIDADES_RJ = [
    ("Duque de Caxias", "RJ"), ("Nova Iguacu", "RJ"), ("Sao Joao de Meriti", "RJ"),
    ("Belford Roxo", "RJ"), ("Nilopolis", "RJ"), ("Rio de Janeiro", "RJ"),
    ("Campos dos Goytacazes", "RJ"), ("Macae", "RJ"), ("Cabo Frio", "RJ"),
    ("Petropolis", "RJ"), ("Teresopolis", "RJ"), ("Niteroi", "RJ"),
    ("Sao Goncalo", "RJ"), ("Itaborai", "RJ"), ("Volta Redonda", "RJ"),
]

TIPOS_CLIENTE = ["Oficina mecanica", "Auto center", "Retifica", "Frotista"]

PREFIXOS_NOME = [
    "Auto Center", "Oficina", "Mecanica", "Auto Pecas", "Centro Automotivo",
    "Retifica", "Auto Service", "Garagem",
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues",
    "Almeida", "Nascimento", "Lima", "Araujo", "Fernandes", "Carvalho",
    "Gomes", "Martins", "Rocha", "Ribeiro", "Alves", "Monteiro", "Barbosa",
    "Progresso", "Central", "Nova Era", "Sao Jorge", "Bandeirante",
    "Real", "Uniao", "Estrela", "Primavera", "Horizonte",
]


def esc(v):
    """Escapa string para SQL."""
    if v is None:
        return "NULL"
    return "'" + str(v).replace("'", "''") + "'"


# ===============================================================
# 1. Produtos + aplicacoes
# ===============================================================
produtos = []
aplicacoes = []
sku_seq = 1000

for desc, categoria, posicao, pmin, pmax, marcas in TIPOS_PECA:
    # cada tipo de peca existe em todas as marcas que o fornecem
    for marca in marcas:
        sku_seq += 1
        sku = f"RV-{sku_seq}"
        preco = round(random.uniform(pmin, pmax), 2)
        cod_orig = f"{random.randint(10000, 99999)}{random.choice('ABCDEFG')}" \
            if random.random() < 0.6 else None

        produtos.append((sku, desc, marca, categoria, posicao, preco, "UN", cod_orig, 1))

        # cada SKU serve de 5 a 12 veiculos, ponderado por popularidade
        for montadora, modelo, motores, ano_i, ano_f, _pop in sortear_veiculos(
            random.randint(5, 12)
        ):
            # metade das pecas serve todas as motorizacoes do modelo (NULL)
            motor = random.choice(motores) if random.random() < 0.5 else None
            # a aplicacao pode cobrir um recorte do periodo do veiculo
            ini = ano_i
            fim = ano_f
            if random.random() < 0.25 and ano_f:
                meio = (ano_i + ano_f) // 2
                if random.random() < 0.5:
                    fim = meio
                else:
                    ini = meio
            obs = None
            if random.random() < 0.12:
                obs = random.choice([
                    "Verificar diametro do disco antes da venda",
                    "Nao serve versao com freio a disco traseiro",
                    "Somente versoes com ar-condicionado",
                    "Conferir numero do chassi",
                    "Aplicavel apenas em cambio manual",
                ])
            aplicacoes.append((sku, montadora, modelo, motor, ini, fim, obs))

# ===============================================================
# 2. Estoque
# ===============================================================
estoque = []
for p in produtos:
    sku = p[0]
    for filial in FILIAIS:
        # CD tem mais estoque que a filial
        if filial.startswith("CD"):
            qtd = random.choices([0, random.randint(1, 8), random.randint(9, 60)],
                                 weights=[5, 25, 70])[0]
            minimo = random.randint(4, 12)
            loc = f"R{random.randint(1,18):02d}-P{random.randint(1,6)}"
        else:
            qtd = random.choices([0, random.randint(1, 5), random.randint(6, 22)],
                                 weights=[15, 40, 45])[0]
            minimo = random.randint(2, 6)
            loc = f"F{random.randint(1,8):02d}-{random.randint(1,4)}"
        estoque.append((sku, filial, qtd, minimo, loc))

# ===============================================================
# 3. Clientes
# ===============================================================
clientes = []
for i in range(1, 91):
    codigo = f"CLI-{i:04d}"
    tipo = random.choices(TIPOS_CLIENTE, weights=[55, 25, 10, 10])[0]
    prefixo = random.choice(PREFIXOS_NOME)
    sobrenome = random.choice(SOBRENOMES)
    fantasia = f"{prefixo} {sobrenome}"
    razao = f"{fantasia} Ltda"
    cidade, uf = random.choice(CIDADES_RJ)
    # frotistas e retificas compram mais -> tabela melhor
    if tipo == "Frotista":
        tabela = random.choice(["A", "A", "B"])
        limite = round(random.uniform(30000, 90000), 2)
    elif tipo == "Retifica":
        tabela = random.choice(["A", "B"])
        limite = round(random.uniform(15000, 45000), 2)
    elif tipo == "Auto center":
        tabela = random.choice(["B", "B", "C"])
        limite = round(random.uniform(8000, 30000), 2)
    else:
        tabela = random.choice(["C", "C", "B"])
        limite = round(random.uniform(3000, 15000), 2)
    clientes.append((codigo, razao, fantasia, tipo, cidade, uf, tabela, limite, 1))

# ===============================================================
# 4. Precos por tabela e categoria
# ===============================================================
CATEGORIAS = sorted({p[3] for p in produtos})
DESCONTOS = {"A": (18, 26), "B": (10, 17), "C": (3, 9)}

precos = []
for tabela, (dmin, dmax) in DESCONTOS.items():
    for categoria in CATEGORIAS:
        precos.append((tabela, categoria, round(random.uniform(dmin, dmax), 2)))

# ===============================================================
# Geracao do SQL
# ===============================================================
linhas = []
add = linhas.append

add("/* ============================================================")
add("   Rodavale — carga de dados ficticios")
add(f"   {len(produtos)} produtos | {len(aplicacoes)} aplicacoes | "
    f"{len(estoque)} registros de estoque | {len(clientes)} clientes")
add("   ============================================================ */")
add("")
add("DELETE FROM dbo.precos_cliente;")
add("DELETE FROM dbo.aplicacoes;")
add("DELETE FROM dbo.estoque;")
add("DELETE FROM dbo.produtos;")
add("DELETE FROM dbo.clientes;")
add("GO")
add("")


def bloco(tabela, colunas, registros, tamanho=200):
    """Gera INSERTs em lotes (SQL Server limita 1000 linhas por INSERT)."""
    add(f"/* ---- {tabela} ---- */")
    for i in range(0, len(registros), tamanho):
        lote = registros[i:i + tamanho]
        add(f"INSERT INTO dbo.{tabela} ({', '.join(colunas)}) VALUES")
        vals = []
        for r in lote:
            campos = []
            for v in r:
                if v is None:
                    campos.append("NULL")
                elif isinstance(v, (int, float)):
                    campos.append(str(v))
                else:
                    campos.append(esc(v))
            vals.append("(" + ", ".join(campos) + ")")
        add(",\n".join(vals) + ";")
        add("GO")
    add("")


bloco("produtos",
      ["sku", "descricao", "marca", "categoria", "posicao",
       "preco_base", "unidade", "codigo_original", "ativo"],
      produtos)

bloco("clientes",
      ["codigo", "razao_social", "nome_fantasia", "tipo",
       "cidade", "uf", "tabela_preco", "limite_credito", "ativo"],
      clientes)

bloco("aplicacoes",
      ["sku", "montadora", "modelo", "motorizacao",
       "ano_inicio", "ano_fim", "observacao"],
      aplicacoes)

bloco("estoque",
      ["sku", "filial", "quantidade", "estoque_minimo", "localizacao"],
      estoque)

bloco("precos_cliente",
      ["tabela_preco", "categoria", "desconto_percentual"],
      precos)

with open("02_dados.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(linhas))

print(f"produtos:   {len(produtos)}")
print(f"aplicacoes: {len(aplicacoes)}")
print(f"estoque:    {len(estoque)}")
print(f"clientes:   {len(clientes)}")
print(f"precos:     {len(precos)}")
print(f"categorias: {CATEGORIAS}")
