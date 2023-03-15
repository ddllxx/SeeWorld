choose = 'infoPane'

infoPane = document.getElementById('infoPane')
worldPane = document.getElementById('worldPane')
focusPane = document.getElementById('focusPane')

infoBtn = document.getElementById('basicInfoBtn')
focusBtn = document.getElementById('focusBtn')
worldBtn = document.getElementById('worldBtn')
logoutBtn = document.getElementById('logoutBtn')
followBtn = document.getElementById('followBtn')

function dealHandler(e) {
    let pane = choose
    switch (e.target.innerText) {
    case 'Basic Info':
        pane = 'infoPane'
        break;
    case 'Focus':
        pane = 'focusPane'
        break;
    case 'World':
        pane = 'worldPane'
        break;
    default:
        break;
    }
    document.getElementById(choose).setAttribute('hidden', 'true');
    document.getElementById(pane).removeAttribute('hidden');
    choose = pane;
}

infoBtn.addEventListener('click', dealHandler)
focusBtn.addEventListener('click', dealHandler)
worldBtn.addEventListener('click', dealHandler)
if (logoutBtn) {
    logoutBtn.addEventListener('click', e => window.location.href = '/logout');
}
if (followBtn) {
    id = document.getElementById('ID').innerText;
    flag = 2;
    async function check() {
        url = '/checkFocus?id=' + id;
        f = await fetch(url)
        data = await f.json();
        flag = data['code']
        if (flag == 1) {
            followBtn.innerText = "UnFollow";
            followBtn.setAttribute('class', 'btn btn-danger')
        } else if (flag == 2 || flag == -1) {
            followBtn.remove()
        }
        followBtn.addEventListener('click', e => {
            if (flag == 0) {
                fetch('/follow?flag=1&id=' + id);
                followBtn.innerText = "UnFollow";
                followBtn.setAttribute('class', 'btn btn-danger');
                flag = 0;
            } else if (flag == 1) {
                fetch('/follow?flag=0&id=' + id);
                followBtn.innerText = "Follow";
                followBtn.setAttribute('class', 'btn btn-info')
                flag = 1;
            }
        })
    }
    check();
}

function generacteMessage(id, title, description, detail) {
    card = document.createElement('div');
    card.setAttribute('class', 'card');
    body = document.createElement('div');
    body.setAttribute('class', 'card-body');
    t = document.createElement('a');
    t.setAttribute('class', 'card-title link');
    t.innerText = title;
    t.setAttribute('href', '/detail?id=' + id);
    p = document.createElement('p');
    p.setAttribute('class', 'card-text');
    p.innerText = description;
    body.appendChild(t);
    body.appendChild(p);
    card.appendChild(body);
    return card;
}

async function setUserInfo(id) {
    id = document.getElementById('ID').innerText;
    url = '/getUserInfo?id=' + id;
    f = await fetch(url);
    data = await f.json();
    document.getElementById('name').innerText = data['name'];
    document.getElementById('ID').innerText = data['id']
    document.getElementById('sex').innerText = data['sex']
    document.getElementById('age').innerText = data['age']
    document.getElementById('profession').innerText = data['profession']
    document.getElementById('nation').innerText = data['nation']
    document.getElementById('introduction').innerText = data['introduction']

    url = '/getFocus?id=' + id;
    f = await fetch(url);
    data = await f.json();
    if (data['code'] == 1) {
        focusList = document.getElementById('focusList');
        for (fid of data['focus']) {
            url = '/getUserInfo?id=' + fid;
            ff = await fetch(url);
            fdata = await ff.json();
            item = document.createElement('li');
            item.setAttribute('class', 'list-group-item');
            link = document.createElement('a');
            link.setAttribute('href', '/user2?id=' + fid);
            link.innerText = fdata['name']
            item.appendChild(link);
            focusList.appendChild(item);
        }
    }

    url = '/getUserWorld?id=' + id;
    f = await fetch(url);
    data = await f.json();
    ml = document.getElementById('messageList');
    if (data['code'] == 1) {
        data = data['message'];
        for (d of data) {
            ml.appendChild(generacteMessage(d[1], d[2], d[3], d[4]))
        }
    }
}

setUserInfo();