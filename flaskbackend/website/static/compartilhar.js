function mostrarFormulario(projectId) {
    var form = document.getElementById('compartilhar-form-' + projectId);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
