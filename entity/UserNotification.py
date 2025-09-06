from datetime import datetime
from extensions import db

class UserNotification(db.Model):
    __tablename__ = 'user_notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__ (self, user_id, sender_id, type, content, is_read, created_at=None):
        self.user_id = user_id
        self.sender_id = sender_id
        self.type = type
        self.content = content
        self.is_read = is_read
        if created_at is None:
            created_at = datetime.utcnow()
        self.created_at = created_at