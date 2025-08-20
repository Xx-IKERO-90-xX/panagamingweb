from entity.chat.Message import Message
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from extensions import db
from entity.chat.PrivateRoom import PrivateRoom
from entity.Friendship import Friendship
from entity.User import User
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

        friendships1 = db.session.query(Friendship, User).filter(
            (Friendship.id_user1 == int(session['id'])) & 
            (Friendship.status == 'accepted')
        ).join(User, User.id == Friendship.id_user2).all()

        friendships2 = db.session.query(Friendship, User).filter(
            (Friendship.id_user2 == int(session['id'])) & 
            (Friendship.status == 'accepted')
        ).join(User, User.id == Friendship.id_user1).all()

        friendships = friendships1 + friendships2

        friendships_pending = db.session.query(Friendship, User).filter(
            (Friendship.id_user2 == int(session['id'])) & 
            (Friendship.status == 'pending')
        ).join(User, Friendship.id_user1 == User.id).all()

        print(friendships_pending)
        for friendship, user in friendships_pending:
            print("Pending Friendship:", friendship.id, "with User:", user.username)


        private_rooms1 = db.session.query(PrivateRoom).filter(
            (PrivateRoom.user_1 == int(session['id']))
        ).all()
        private_rooms2 = db.session.query(PrivateRoom).filter(
            (PrivateRoom.user_2 == int(session['id']))
        ).all()

        private_rooms = private_rooms1 + private_rooms2

        return render_template(
            'paginas/chat/index.jinja',
            friendships=friendships,
            friendships_pending=friendships_pending,
            private_rooms=private_rooms,
            session=session
        )
    
    else:
        return redirect(url_for('auth.login'))
    