// Permitir o drop (soltar) em uma área válida
function allowDrop(event) {
    event.preventDefault(); // Permite que o elemento seja solto
}

// Definir os dados do elemento que está sendo arrastado
function drag(event) {
    event.dataTransfer.setData("task_id", event.target.id); // Armazena o id do elemento arrastado
}

// Lidar com o drop (soltar) e adicionar o elemento na nova coluna
function drop(event, status) {
    event.preventDefault(); // Previne o comportamento padrão

    // Obtém o id da tarefa que está sendo arrastada
    let taskId = event.dataTransfer.getData("task_id");

    // Obtém o elemento da tarefa pelo id
    let taskElement = document.getElementById(taskId);

    // Adiciona a tarefa na nova coluna (onde foi solta)
    event.target.appendChild(taskElement);

    // Chama a função para atualizar o status da tarefa no servidor
    updateTaskStatus(taskId, status);
}

// Função para atualizar o status da tarefa no backend
function updateTaskStatus(taskId, status) {
    fetch(`/atualizar_tarefa/${taskId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token() }}"  // Se estiver usando CSRF no Flask
        },
        body: JSON.stringify({status: status}) // Envia o novo status da tarefa
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Status da tarefa atualizado com sucesso");
        } else {
            console.error("Erro ao atualizar o status da tarefa");
        }
    })
    .catch(error => {
        console.error("Erro na requisição:", error);
    });
}

// Adiciona um event listener ao botão "Salvar"
document.getElementById('SalvarProj').addEventListener('click', function() {
    // Coletar todas as tarefas e seus novos status
    let tasks = [];

    // Coletar tarefas de 'Pré-requisitos'
    document.querySelectorAll('#prerequisites li').forEach(function(task) {
        tasks.push({
            id_task: task.id,
            status: 'Pré-requisitos'
        });
    });

    // Coletar tarefas de 'Em Produção'
    document.querySelectorAll('#inProduction li').forEach(function(task) {
        tasks.push({
            id_task: task.id,
            status: 'Em Produção'
        });
    });

    // Coletar tarefas de 'Concluído'
    document.querySelectorAll('#completed li').forEach(function(task) {
        tasks.push({
            id_task: task.id,
            status: 'Concluído'
        });
    });

    // Enviar as tarefas atualizadas para o backend
    fetch('/atualizar_tarefas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // Se estiver usando CSRF no Flask
        },
        body: JSON.stringify({ tasks: tasks })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirecionar para a página inicial após salvar com sucesso
            window.location.href = '/home';
        } else {
            alert('Erro ao salvar as tarefas');
        }
    })
    .catch(error => {
        console.error('Erro ao salvar tarefas:', error);
    });
});








// Facilidade e importancia

document.addEventListener("DOMContentLoaded", function() {
    // Função para atualizar a seleção de Importância
    const importanceButtons = document.querySelectorAll('.importance-btn');
    importanceButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove a classe 'selected' de todos os botões
            importanceButtons.forEach(btn => btn.classList.remove('selected'));
            // Adiciona a classe 'selected' ao botão clicado
            this.classList.add('selected');
            // Atualiza o valor do input hidden de importância
            document.getElementById('importance').value = this.getAttribute('data-value');
        });
    });

    // Função para atualizar a seleção de Facilidade
    const easeButtons = document.querySelectorAll('.ease-btn');
    easeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove a classe 'selected' de todos os botões
            easeButtons.forEach(btn => btn.classList.remove('selected'));
            // Adiciona a classe 'selected' ao botão clicado
            this.classList.add('selected');
            // Atualiza o valor do input hidden de facilidade
            document.getElementById('ease').value = this.getAttribute('data-value');
        });
    });

    // Verificar se os valores foram selecionados antes de enviar o formulário de criação/edição de tarefas
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Verifica se o formulário contém campos de importância e facilidade
            const importanceInput = form.querySelector('#importance');
            const easeInput = form.querySelector('#ease');

            // Se o formulário tiver os campos de importância e facilidade, validá-los
            if (importanceInput && easeInput) {
                const importance = importanceInput.value;
                const ease = easeInput.value;

                if (importance === '' || ease === '') {
                    event.preventDefault();  // Impede o envio do formulário
                    alert('Por favor, selecione a Importância e a Facilidade.');
                }
            }
        });
    });
});