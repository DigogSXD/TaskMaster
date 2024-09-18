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
            // Redirecionar para a página inicial após o sucesso
            window.location.href = '/home';
        } else {
            alert('Erro ao atualizar as tarefas');
        }
    })
    .catch(error => {
        console.error('Erro ao salvar tarefas:', error);
    });
});
