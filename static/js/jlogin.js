form = document.getElementById('login_form')
loginBtn = document.getElementById('loginBtn')
registerBtn = document.getElementById('registerBtn')

loginBtn.addEventListener('click', login)
registerBtn.addEventListener('click', register)

function login(e) {
    console.log('user login...');
    form.action = '/login';
    form.submit();
}

function register(e) {
    window.location.href = "/registerNew";
}