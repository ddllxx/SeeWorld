id = document.getElementById('IDrecord').value;
comments = {}

title = document.getElementById('title');
description = document.getElementById('description');
detail = document.getElementById('detail');

commentBtn = document.getElementById('commentBtn');

async function updateMessage(id) {
    f = await fetch('/getMessage?id=' + id);
    data = await f.json();
    if (data['code'] == 0) {
        return;
    }
    data = data['message'];
    title.innerText = data[0];
    description.innerText = data[1];
    detail.innerText = data[2];
    messageOwn = data[3];

    f = await fetch('/isMe');
    data = await f.json();
    if (data['code'] == 0) {
        return;
    }
    uid = data['id'];
    f = await fetch('/getComment?id=' + id);
    data = await f.json();
    if (data['code'] == 0) {
        return;
    }
    data = data['comment'];
    clist = document.getElementById('commentList')
    for (c of data) {
        item = document.createElement('li');
        item.setAttribute('class', 'list-group-item comment');
        p = document.createElement('p');
        p.innerHTML = '<span>' + c[0] + ': </span>' + c[1];
        item.appendChild(p);
        p = document.createElement('p');
        p.innerHTML = c[4];
        p.setAttribute('class', 'card-text cardMessageDate')
        item.appendChild(p);
        if (uid == c[2] || uid == messageOwn) {
            b = document.createElement('button');
            b.setAttribute('class', 'btn btn-danger');
            b.innerText = 'delete';
            b.commentID = c[3]
            b.addEventListener('click', deleteComment);
            item.appendChild(b);
        }
        comments[c[3]] = item;
        clist.appendChild(item);
    }
    // loadList();
}

function loadList()
{
    clist.innerText = ''
    for (i in comments) {
        clist.appendChild(comments[i]);
    }
}

function deleteComment(e)
{
    fetch('/delComment?id=' + e.target.commentID);
    delete comments[e.target.commentID];
    loadList();
}

updateMessage(id);