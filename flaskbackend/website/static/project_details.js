// Funções para arrastar e soltar tarefas
function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function drop(event) {
    event.preventDefault();
    const data = event.dataTransfer.getData("text");
    const task = document.getElementById(data);
    event.target.appendChild(task);
}

// Função para adicionar tarefas em cada coluna
document.getElementById('addPrerequisite').addEventListener('click', function() {
    addTask('prerequisites', 'newPrerequisite');
});

document.getElementById('addInProduction').addEventListener('click', function() {
    addTask('inProduction', 'newInProduction');
});

document.getElementById('addCompleted').addEventListener('click', function() {
    addTask('completed', 'newCompleted');
});

// Função para adicionar tarefa com drag and drop habilitado
function addTask(listId, inputId) {
    const list = document.getElementById(listId);
    const newTaskInput = document.getElementById(inputId);
    const taskText = newTaskInput.value.trim();

    if (taskText !== '') {
        const newTask = document.createElement('li');
        newTask.textContent = taskText;
        newTask.setAttribute('id', Math.random().toString(36).substr(2, 9)); // Gera um ID único para cada tarefa
        newTask.setAttribute('draggable', 'true');
        newTask.setAttribute('ondragstart', 'drag(event)');
        list.appendChild(newTask);
        newTaskInput.value = ''; // Limpa o campo de entrada
    } else {
        alert('Por favor, insira uma tarefa válida.');
    }
}
