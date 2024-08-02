document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    console.log('Login:', { email, password });
    // Adicione aqui a lógica para autenticação
});

document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    console.log('Cadastro:', { email, password });
    // Adicione aqui a lógica para cadastro
});

document.getElementById('toSignupButton').addEventListener('click', function() {
    document.getElementById('loginContainer').style.display = 'none';
    document.getElementById('signupContainer').style.display = 'block';
});

document.getElementById('toLoginButton').addEventListener('click', function() {
    document.getElementById('signupContainer').style.display = 'none';
    document.getElementById('loginContainer').style.display = 'block';
});

// Inicialmente, mostrar o container de login
document.getElementById('loginContainer').style.display = 'block';
