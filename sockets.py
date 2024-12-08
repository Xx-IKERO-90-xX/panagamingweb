from flask_socketio import emit
import multiprocessing
import controller.McServersController as mcservers
from extensions import socketio
from app import app


# Maneja los mensajes enviados desde el chat publico de la pagina del servidor de Minecraft
@socketio.on('send_message')
def handle_public_chat_message(data):
    app.logger.info(f"Message: {data['message']} from {data['username']}")
    data['id'] = f"/usuario/{data['id']}"
    emit('receive_message', data, broadcast=True)


#Terminal de los servidores de minecraft
@socketio.on('send_vanilla_command')
def handle_send_command(cmd):  
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=mcservers.execute_vanilla_command, 
        args=(cmd['command'], result_queue)
    )
    
    process.start()
    process.join()

    response = result_queue.get()

    emit('server_output', {'output': response})