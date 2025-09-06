from entity.chat.Message import Message
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from extensions import db, mongodb
from entity.chat.PrivateRoom import PrivateRoom
from entity.Friendship import Friendship
from entity.User import User
import os
import sys
from datetime import datetime

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
        friendships.sort(key=lambda x: x.Friendship.last_message_date if x.Friendship.last_message_date else datetime(2000, 1, 1), reverse=True)

        friendships_pending = db.session.query(Friendship, User).filter(
            (Friendship.id_user2 == int(session['id'])) & 
            (Friendship.status == 'pending')
        ).join(User, Friendship.id_user1 == User.id).all()

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

# Route to open a private chat room
@chat_bp.route('/private/<int:user_id>', methods=['GET'])
async def private_room(user_id):
    if 'id' in session:
        friendship = db.session.query(Friendship).filter(
            ((Friendship.id_user1 == session['id']) & (Friendship.id_user2 == user_id) | 
            (Friendship.id_user2 == session['id']) & (Friendship.id_user1 == user_id)) & 
            (Friendship.status == 'accepted')
        ).first()

        if not friendship:
            return redirect(url_for('chat.index'))
        else:
            me = None
            friend = None
            
            if friendship.id_user2 == session['id']:
                user_1 = db.session.query(User).filter_by(id=user_id).first()
                user_2 = db.session.query(User).filter_by(id=session['id']).first()
                
                me = user_2
                friend = user_1
            
            else:
                user_1 = db.session.query(User).filter_by(id=session['id']).first()
                user_2 = db.session.query(User).filter_by(id=user_id).first()

                me = user_1
                friend = user_2

            private_room_name = f'private_room_{user_1.id}_{user_2.id}'
            private_room = mongodb[private_room_name]
            messages = private_room.find()


            return render_template(
                'paginas/chat/private_room.jinja',                
                me=me,
                friend=friend,
                messages=messages,
                friendship=friendship,
                private_room=private_room_name,
                session=session
            )
    else:
        return redirect(url_for('auth.login'))