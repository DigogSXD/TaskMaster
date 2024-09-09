// Função para adicionar uma nova tarefa na coluna de pré-requisitos
document.getElementById('addPrerequisite').addEventListener('click', function() {
    var taskText = document.getElementById('newPrerequisite').value;
    if (taskText.trim() !== '') {
        var taskItem = document.createElement('li');
        taskItem.textContent = taskText;
        document.getElementById('prerequisites').appendChild(taskItem);
        document.getElementById('newPrerequisite').value = ''; // Limpa o campo de texto
    }
});

// Função para adicionar uma nova tarefa na coluna Em Produção
document.getElementById('addInProduction').addEventListener('click', function() {
    var taskText = document.getElementById('newInProduction').value;
    if (taskText.trim() !== '') {
        var taskItem = document.createElement('li');
        taskItem.textContent = taskText;
        document.getElementById('inProduction').appendChild(taskItem);
        document.getElementById('newInProduction').value = ''; // Limpa o campo de texto
    }
});

// Função para adicionar uma nova tarefa na coluna Concluído
document.getElementById('addCompleted').addEventListener('click', function() {
    var taskText = document.getElementById('newCompleted').value;
    if (taskText.trim() !== '') {
        var taskItem = document.createElement('li');
        taskItem.textContent = taskText;
        document.getElementById('completed').appendChild(taskItem);
        document.getElementById('newCompleted').value = ''; // Limpa o campo de texto
    }
});
