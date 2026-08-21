"""Carrega o SQL gerado em SQLite e testa as consultas que o agente fara."""
import re
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript("""
CREATE TABLE produtos (sku TEXT PRIMARY KEY, descricao TEXT, marca TEXT, categoria TEXT, posicao TEXT, preco_base REAL, unidade TEXT, codigo_original TEXT, ativo INT);
CREATE TABLE aplicacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT, montadora TEXT, modelo TEXT, motorizacao TEXT, ano_inicio INT, ano_fim INT, observacao TEXT);
CREATE TABLE estoque (sku TEXT, filial TEXT, quantidade INT, estoque_minimo INT, localizacao TEXT);
CREATE TABLE clientes (codigo TEXT PRIMARY KEY, razao_social TEXT, nome_fantasia TEXT, tipo TEXT, cidade TEXT, uf TEXT, tabela_preco TEXT, limite_credito REAL, ativo INT);
CREATE TABLE precos_cliente (id INTEGER PRIMARY KEY AUTOINCREMENT, tabela_preco TEXT, categoria TEXT, desconto_percentual REAL);
""")

sql = open("02_dados.sql", encoding="utf-8").read()
sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.S).replace("dbo.", "")
for bloco in sql.split("GO"):
    for stmt in bloco.split(";"):
        stmt = stmt.strip()
        if stmt.upper().startswith("INSERT"):
            cur.execute(stmt)
con.commit()

print("=" * 62)
print("VOLUMETRIA")
print("=" * 62)
for t in ["produtos", "aplicacoes", "estoque", "clientes", "precos_cliente"]:
    print(f"  {t:16s} {cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>6}")

print()
print("=" * 62)
print("1. Que pastilha serve num Onix 2018 1.4?")
print("=" * 62)
rows = cur.execute("""
    SELECT p.sku, p.marca, p.posicao, p.preco_base,
           (SELECT SUM(quantidade) FROM estoque e WHERE e.sku = p.sku) AS est
    FROM produtos p
    JOIN aplicacoes a ON a.sku = p.sku
    WHERE a.montadora = 'Chevrolet' AND a.modelo = 'Onix'
      AND 2018 BETWEEN a.ano_inicio AND COALESCE(a.ano_fim, 9999)
      AND (a.motorizacao = '1.4' OR a.motorizacao IS NULL)
      AND p.descricao LIKE 'Pastilha%'
    ORDER BY p.posicao, p.preco_base
""").fetchall()
for r in rows:
    print(f"  {r[0]:9s} {r[1]:18s} {str(r[2]):10s} R$ {r[3]:8.2f}  estoque: {r[4]}")
print(f"  -> {len(rows)} opcoes")

print()
print("=" * 62)
print("2. Cobertura por veiculo (top 10)")
print("=" * 62)
rows = cur.execute("""
    SELECT a.montadora || ' ' || a.modelo AS veiculo, COUNT(DISTINCT a.sku) AS skus
    FROM aplicacoes a GROUP BY veiculo ORDER BY skus DESC LIMIT 10
""").fetchall()
for r in rows:
    print(f"  {r[0]:28s} {r[1]:>4} SKUs")

print()
print("=" * 62)
print("3. Preco final para um cliente (com desconto da tabela)")
print("=" * 62)
cli = cur.execute("""
    SELECT codigo, nome_fantasia, tipo, tabela_preco FROM clientes
    WHERE tabela_preco = 'A' LIMIT 1
""").fetchone()
print(f"  Cliente: {cli[0]} — {cli[1]} ({cli[2]}, tabela {cli[3]})")
rows = cur.execute("""
    SELECT p.sku, p.descricao, p.marca, p.preco_base, pc.desconto_percentual,
           ROUND(p.preco_base * (1 - pc.desconto_percentual/100.0), 2) AS preco_final
    FROM produtos p
    JOIN precos_cliente pc ON pc.categoria = p.categoria AND pc.tabela_preco = ?
    WHERE p.categoria = 'Freios' LIMIT 4
""", (cli[3],)).fetchall()
for r in rows:
    print(f"  {r[0]:9s} {r[1][:22]:24s} base R$ {r[3]:7.2f}  -{r[4]:.1f}%  ->  R$ {r[5]:7.2f}")

print()
print("=" * 62)
print("4. Itens abaixo do estoque minimo (alerta de reposicao)")
print("=" * 62)
n = cur.execute("""
    SELECT COUNT(*) FROM estoque WHERE quantidade < estoque_minimo
""").fetchone()[0]
print(f"  {n} registros abaixo do minimo")

print()
print("=" * 62)
print("5. Integridade referencial")
print("=" * 62)
orfas = cur.execute("""
    SELECT COUNT(*) FROM aplicacoes a
    LEFT JOIN produtos p ON p.sku = a.sku WHERE p.sku IS NULL
""").fetchone()[0]
orfas_est = cur.execute("""
    SELECT COUNT(*) FROM estoque e
    LEFT JOIN produtos p ON p.sku = e.sku WHERE p.sku IS NULL
""").fetchone()[0]
sem_est = cur.execute("""
    SELECT COUNT(*) FROM produtos p
    LEFT JOIN estoque e ON e.sku = p.sku WHERE e.sku IS NULL
""").fetchone()[0]
cats_sem_preco = cur.execute("""
    SELECT COUNT(DISTINCT p.categoria) FROM produtos p
    LEFT JOIN precos_cliente pc ON pc.categoria = p.categoria
    WHERE pc.id IS NULL
""").fetchone()[0]
print(f"  aplicacoes orfas:            {orfas}")
print(f"  estoque orfao:               {orfas_est}")
print(f"  produtos sem estoque:        {sem_est}")
print(f"  categorias sem tabela preco: {cats_sem_preco}")
