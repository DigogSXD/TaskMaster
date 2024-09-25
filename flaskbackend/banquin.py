import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'instance', 'taskmaster.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificando todas as tabelas existentes no banco de dados
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas_existentes = cursor.fetchall()
    print("Tabelas no banco de dados:")
    for tabela in tabelas_existentes:
        print(tabela[0])

except sqlite3.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")