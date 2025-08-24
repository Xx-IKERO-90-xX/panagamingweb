let sendBtn = document.getElementById('send');
let cancelBtn = document.getElementById('cancel');
let messageInput = document.getElementById('myMessage');

document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

    socket.on('receive_message', (data) => {
        let msgTemplate = document.getElementById('messageTemplate').content.cloneNode(true);
        let msgDiv = msgTemplate.getElementById('msg');

        if (data.imgUrl === '' || data.imgUrl === null || data.imgUrl === undefined || data.imgUrl === 'None') {
            msgTemplate.getElementById('msgImg').src = '/static/img/userlog.jpg'
        }
        else {
            msgTemplate.getElementById('msgImg').src = `/static/uploads/${data.imgUrl}`;
        }
        msgTemplate.getElementById('msgName').href = `${data.id}`;
        msgTemplate.getElementById('msgName').innerHTML = data.username

        msgTemplate.getElementById('content').innerHTML = data.message;
        document.getElementById('messages').append(msgDiv);
    })

    window.sendMessage = function () {
        let userName = document.getElementById('idName').value;
        let idUser = document.getElementById('idUser').value;
        let imgUrl = document.getElementById('imgUrl').value;
        let msg = messageInput.value;

        socket.emit('send_private_message', {
            id: idUser,
            username: userName,
            imgUrl: imgUrl,
            content: msg
        });
        messageInput.value = '';
    }
})

cancelBtn.addEventListener('click', () => {
    messageInput.value = '';
});