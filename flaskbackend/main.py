from flask import Flask, render_template,request

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')


# Simulação de armazenamento de projetos (dicionário para projetos)
projects = {}

@app.route('/')
def index():
    # Certifique-se de passar o dicionário 'projects' para o template
    return render_template('project.html', projects=projects)

@app.route('/projeto/<int:project_id>')
def gerenciar_projeto(project_id):
    project_name = projects.get(project_id)  # Buscar o nome do projeto pelo ID
    if not project_name:
        project_name = "Projeto não encontrado"
    return render_template('project_details.html', project_name=project_name)

@app.route('/adicionar_projeto', methods=['POST'])
def adicionar_projeto():
    # Adicionar o projeto ao dicionário 'projects'
    project_id = len(projects) + 1  # Gerar um ID único com base no número de projetos
    project_name = request.form['project_name']
    projects[project_id] = project_name  # Armazenar o nome do projeto com o ID no dicionário 'projects'
    return redirect('/')



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    app.run(debug=True)