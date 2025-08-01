from extensions import db
from entity.characters.Character import Character

async def character_name_in_use(name):
    """
    Comprueba si el nombre del personaje ya esta en uso.
    """
    character = db.session.query(Character).filter(Character.name == name).first()
    return character is not None

