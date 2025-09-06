from datetime import datetime
from extensions import db
from entity.Friendship import Friendship

def friendship_is_sended(id_user1, id_user2):
    friendship = db.session.query(Friendship).filter(
        ((Friendship.id_user1 == id_user1) & (Friendship.id_user2 == id_user2)) | 
        ((Friendship.id_user1 == id_user2) & (Friendship.id_user2 == id_user1))
    ).first()
    
    return friendship is not None