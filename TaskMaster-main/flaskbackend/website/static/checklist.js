document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('marcar-todas').onclick = function() {
        document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
            checkbox.checked = true;
        });
    };

    document.getElementById('desmarcar-todas').onclick = function() {
        document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
            checkbox.checked = false;
        });
    };
});

function toggleEdit(itemId) {
    const editForm = document.getElementById(`edit-form-${itemId}`);
    if (editForm.style.display === 'none' || editForm.style.display === '') {
        editForm.style.display = 'block'; // Mostra o formulário de edição
    } else {
        editForm.style.display = 'none'; // Oculta o formulário de edição
    }
}
