import sqlite3
import os

# Diretório base e caminho para o banco de dados
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'instance', 'taskmaster.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def consultar_tudo(email):
        query = """
                SELECT 
                    U1.email AS criador_email, 
                    Project.nome_projeto AS projeto_nome, 
                    GROUP_CONCAT(U2.email, ', ') AS usuarios_adicionados
                FROM Usuario AS U1
                INNER JOIN Project 
                    ON U1.id = Project.user_id
                LEFT JOIN rel_usuario_project 
                    ON Project.id = rel_usuario_project.project_id
                LEFT JOIN Usuario AS U2 
                    ON rel_usuario_project.user_id = U2.id
                WHERE U1.email = ?
                GROUP BY U1.email, Project.nome_projeto

                """
        cursor.execute(query, (email,))
        resultados = cursor.fetchall()
        print(f"Consultando Projetos CRIADOS Pelo Usuário: {email}")
        for i in resultados:
            
            print(i)
        print("\n\n")

        query2 = """SELECT 
                        Usuario.id, 
                        Usuario.email, 
                        GROUP_CONCAT(Project.nome_projeto, ', ') AS projetos
                    FROM Usuario
                    INNER JOIN rel_usuario_project 
                        ON Usuario.id = rel_usuario_project.user_id
                    INNER JOIN Project 
                        ON rel_usuario_project.project_id = Project.id
                    WHERE Usuario.email = ?
                    GROUP BY Usuario.id, Usuario.email
"""

        cursor.execute(query2, (email,))
        resultados2 = cursor.fetchall()
        print(f"Consultando projetos em que o usuário: {email} foi adicionado")
        for i in resultados2:
            print(i)
            

    consultar_tudo("pepa@gmail.com")
    conn.close()


except sqlite3.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
