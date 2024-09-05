import sqlite3

# Conectando ao banco de dados
conn = sqlite3.connect('instance/db.sqlite')
cursor = conn.cursor()

# Criando a tabela user manualmente
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# Confirmando as alterações
conn.commit()

# Verificando se a tabela foi criada
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tabelas no banco de dados:", tables)

# Fechando a conexão
conn.close()
