import os
import sys
from flask import request, Flask, render_template, current_app, redirect, session, url_for, Blueprint
from werkzeug.utils import secure_filename
from entity.User import User
from entity.UserStyle import UserStyle
from entity.Friendship import Friendship
from extensions import db

# Chech if the user is a friend
async def is_friend(user_id, session_id):
    if user_id == session_id:
        return True
    friendship = db.session.query(Friendship).filter(
        ((Friendship.id_user1 == user_id) & (Friendship.id_user2 == session_id)) |
        ((Friendship.id_user1 == session_id) & (Friendship.id_user2 == user_id))
    ).first()
    return friendship is not None and friendship.status == 'accepted'
