import sqlite3
import os

# Diretório base e caminho para o banco de dados
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'instance', 'taskmaster.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Função para consultar os projetos de um usuário específico pelo email
    def consultar_projetos_usuario(email):
        query = """
        SELECT p.id, p.nome_projeto
        FROM project p
        JOIN usuario u ON p.user_id = u.id
        WHERE u.email = ?
        """
        cursor.execute(query, (email,))  # Correto: passando o email como uma tupla
        resultados = cursor.fetchall()

        print(f"\nProjetos do usuário com email {email}:")
        if resultados:
            for row in resultados:
                print(f"Projeto ID: {row[0]}, Nome: {row[1]}")
        else:
            print("Nenhum projeto encontrado para este usuário.")

    # Consultar os projetos do usuário com email 'pepa@gmail.com'
    consultar_projetos_usuario('azul@gmail.com')

    conn.close()

except sqlite3.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
