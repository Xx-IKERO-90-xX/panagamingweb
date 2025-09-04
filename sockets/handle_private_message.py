from extensions import mongodb, socketio
from datetime import datetime
import os
import sys

@socketio.on("send_private_message")
def handle_private_message(data):
    mongodb.insert_one({
        "sender": data['id'],
        "timestamp": datetime.utcnow(),
        "content": data['content']
    })
    print(data)
    emit('receive_message', data, broadcast=True)

