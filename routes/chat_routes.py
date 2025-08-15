from entity.chat.Message import Message
from flask import Blueprint, render_template, session, request, redirect, url_for
from extensions import db
from entity.chat.PrivateRoom import PrivateRoom
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
        return render_template('paginas/chat/index.jinja')
    else:
        return redirect(url_for('auth.login'))
    