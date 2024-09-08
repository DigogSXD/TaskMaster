from flask import Flask, render_template

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

@app.route('/')
def index():
    return render_template('project.html')

@app.route('/projeto/<int:project_id>')
def gerenciar_projeto(project_id):
    project_name = f"Projeto {project_id}"
    return render_template('project_details.html', project_name=project_name)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')
if __name__ == '__main__':
    app.run(debug=True)

