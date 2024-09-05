document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    console.log('Cadastro:', { email, password });

    fetch('/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Corrija isso
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        console.log('Resposta bruta:', response);  // Verifique a resposta bruta aqui
        return response.json();
    })
    .then(data => {
        console.log('Dados:', data);  // Verifique os dados aqui
        if (data.redirect) {
            window.location.href = data.redirect;
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Erro:', error));
});

document.getElementById('toLoginButton').addEventListener('click', function() {
    window.location.href = '/auth/login';
});
