document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('projectForm');
    const projectNameInput = document.getElementById('projectName');
    const projectsTable = document.getElementById('projectsTable');

    let projects = [];

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const projectName = projectNameInput.value.trim();
        if (projectName !== '') {
            const projectId = new Date().getTime();
            projects.push({ id: projectId, name: projectName });
            addProjectToTable(projectId, projectName);
            projectNameInput.value = '';
        }
    });

    function addProjectToTable(id, name) {
        const row = projectsTable.insertRow();
        row.setAttribute('data-id', id);

        const cellName = row.insertCell(0);
        cellName.textContent = name;

        const cellActions = row.insertCell(1);
        cellActions.classList.add('actions');
        cellActions.innerHTML = `
            <button onclick="editProject(${id})" style="background-color: #337ab7; color: white;">Editar</button>
            <button onclick="deleteProject(${id})" style="background-color: red; color: white;">Deletar</button>
            <button onclick="manageProject(${id})" style="background-color: #337ab7; color: white;">Gerenciar</button>
        `;
    }

    window.editProject = function(id) {
        const project = projects.find(p => p.id === id);
        const newName = prompt('Edite o nome do projeto:', project.name);
        if (newName !== null && newName.trim() !== '') {
            project.name = newName.trim();
            const row = projectsTable.querySelector(`tr[data-id='${id}']`);
            row.cells[0].textContent = newName.trim();
        }
    }

    window.deleteProject = function(id) {
        if (confirm('Você tem certeza que deseja deletar este projeto?')) {
            projects = projects.filter(p => p.id !== id);
            const row = projectsTable.querySelector(`tr[data-id='${id}']`);
            projectsTable.deleteRow(row.rowIndex);
        }
    }

    window.manageProject = function(id) {
        // Redirecionar para a página de gerenciamento do projeto
        window.location.href = `/projeto/${id}`;
    }
});
