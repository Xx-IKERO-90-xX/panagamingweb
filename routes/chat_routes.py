from entity.chat.Message import Message
from flask import Blueprint, render_template, session, request, redirect, url_for
from extensions import db
from entity.chat.PrivateRoom import PrivateRoom
from entity.Friendship import Friendship
import os
import sys

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app
from extensions import db

session = app.session
chat_bp = Blueprint('chat', __name__)

# Route to render the chat page
@chat_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        friendships = db.session.query(Friendship).filter(
            (Friendship.id_user1 == session['id']) | (Friendship.id_user2 == session['id'])
        ).all()
        private_rooms = db.session.query(PrivateRoom).filter(
            (PrivateRoom.user_1 == session['id']) | (PrivateRoom.user_2 == session['id'])
        ).all()

        return render_template(
            'paginas/chat/index.jinja',
            friendships=friendships,
            private_rooms=private_rooms,
            session=session
        )
    
    else:
        return redirect(url_for('auth.login'))
    