logInOutLink = document.getElementById('logInOutLink')

async function updateLoginStatus() {
    f = await fetch('/isMe');
    data = await f.json();
    if (data['code'] == 1) {
        logInOutLink.innerText = 'Profile';
        logInOutLink.setAttribute('href', '/user')
    }
}

updateLoginStatus();