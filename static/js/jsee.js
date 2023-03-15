list = document.getElementById('messageList')
const count = 5;

function getType(type) {
    switch (type) {
        case 1:
            return 'Current Affairs News';
        case 2:
            return 'Community Discussion';
        case 3:
            return 'Mutual Assistance Area';
        default:
            return 'Unknow'
    }
}

function generacteMessage(title, description, id, user_id, name, date, type) {
    card = document.createElement('div');
    card.setAttribute('class', 'card m-2');
    titleE = document.createElement('div');
    titleE.setAttribute('class', 'card-header');
    a = document.createElement('a');
    a.setAttribute('href', 'detail?id=' + id);
    a.setAttribute('class', 'link');
    a.innerText = title;
    titleE.appendChild(a);
    a = document.createElement('a');
    a.setAttribute('href', 'user2?id=' + user_id)
    a.setAttribute('class', 'link');
    a.innerText = ' @' + name;
    titleE.appendChild(a);
    card.appendChild(titleE);
    bodyE = document.createElement('div');
    bodyE.setAttribute('class', 'card-body');
    p = document.createElement('p');
    p.setAttribute('class', 'card-text cardMessageDate');
    p.innerText = getType(type);
    bodyE.appendChild(p);
    p = document.createElement('p');
    p.setAttribute('class', 'card-text');
    p.innerText = description;
    bodyE.appendChild(p);
    p = document.createElement('p');
    p.setAttribute('class', 'card-text cardMessageDate');
    p.innerText = date;
    bodyE.appendChild(p);
    card.appendChild(bodyE);
    return card;
}

async function loadMessage() {
    page = document.getElementById('page').innerText;
    if (page == 1) {
        document.getElementById('prev').setAttribute('hidden', 'true');
    }
    f = await fetch('/getAllWorld?start=' + count * (page - 1) + '&count=' + count + '&type=' + document.getElementById('typeInput').value);
    data = await f.json();
    if (data['code'] == 1) {
        if (data['message'].length < count) {
            document.getElementById('next').setAttribute('hidden', 'true');
        }
        for (d of data['message']) {
            currM = generacteMessage(d[4], d[5], d[3], d[0], d[1], d[2], d[6]);
            list.appendChild(currM);
        }
    }
}

async function generateList(e) {
    window.location.href = '/see?page=1&type=' + e.target.value;
}

document.getElementById('typeInput').addEventListener('change', generateList)

loadMessage();