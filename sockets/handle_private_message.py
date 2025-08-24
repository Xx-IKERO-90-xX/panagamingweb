from extensions import mongodb, socketio
from datetime import datetime
import os
import sys

@socketio.on("send_message")
def handle_private_message(data):
    mongodb.insert_one({
        "sender": data['id'],
        "timestamp": datetime.utcnow(),
        "content": data['content']
    })
    emit('recieve_message', data, broadcast=True)
