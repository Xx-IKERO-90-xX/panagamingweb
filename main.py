from app import create_app, socketio
from bot import run_bot
import multiprocessing
from extensions import db

app = None

def run_flask():
    app = create_app()
    with app.app_context():
        db.create_all()
    
    socketio.run(
        app, 
        port=5000, 
        host='0.0.0.0', 
        debug=True,
        allow_unsafe_werkzeug=True
    )



if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    # Corre el bot de Discord en el proceso principal
    run_bot()

    flask_process.join()