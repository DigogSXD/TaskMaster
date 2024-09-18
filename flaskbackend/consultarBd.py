import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'instance', 'taskmaster.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Função para consultar e exibir os dados de uma tabela específica:
    def consultar_tabela(tabela):
        cursor.execute(f"SELECT * FROM {tabela}")
        resultados = cursor.fetchall()
        print(f"\nDados da tabela {tabela}:")
        if resultados:
            for row in resultados:
                print(row)
        else:
            print(f"A tabela {tabela} está vazia.")

    tabelas = ['usuario', 'project', 'task']
    for tabela in tabelas:
        consultar_tabela(tabela)
    conn.close()
    
except sqlite3.Error as e:
    # Exibindo a mensagem de erro no terminal.
    print(f"Erro ao conectar ao banco de dados: {e}")
