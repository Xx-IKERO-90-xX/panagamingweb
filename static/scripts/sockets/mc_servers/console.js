var socket = io();

// Recibe la salida del servidor de minecraft en tiempo real
socket.on('server_output', function(data) {
    var terminal = document.getElementById("terminal_vanilla_output");
    console.log(data)
    terminal.innerText += data.output + "\n";
    terminal.scrollTop = terminal.scrollHeight;
});

// Envia el comando al servidor.
document.getElementById("vanilla_command_form").addEventListener("submit", (event)=> {
    event.preventDefault();
    var command = document.getElementById("commandInput").value;
    socket.emit('send_vanilla_command', {"command": command});
    document.getElementById("commandInput").value = '';
});