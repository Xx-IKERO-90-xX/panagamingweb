const sendBtn = document.getElementById('send');
const cancelBtn = document.getElementById('cancel');
const messageInput = document.getElementById('myMessage');

document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

    socket.on('receive_message', (data) => {
        let msgTemplate = document.getElementById('messageTemplate').content.cloneNode(true);
        let msgDiv = msgTemplate.getElementById('msg');

        msgTemplate.getElementById('msgImg').src = data.imgUrl;
        msgTemplate.getElementById('msgName').href = data.id;
        msgTemplate.getElementById('msgName').innerHTML = data.username

        msgTemplate.getElementById('content').innerHTML = data.message;
        document.getElementById('messages').append(msgDiv);
    })

    window.sendMessage = function () {

        let userName = document.getElementById('idName').value;
        let idUser = document.getElementById('idUser').value;
        let imgUrl = document.getElementById('imgUrl').value;
        let msg = messageInput.value;

        socket.emit('send_message', {
            id: idUser,
            username: userName,
            imgUrl: imgUrl,
            message: msg
        });
        messageInput.value = '';
    }
})

cancelBtn.addEventListener('click', () => {
    messageInput.value = '';
});