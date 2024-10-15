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
