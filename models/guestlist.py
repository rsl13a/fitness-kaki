from models.base_model import BaseModel
from models.user import User
from models.event import Event
import peewee as pw

class Guestlist(BaseModel):
    event = pw.ForeignKeyField(Event, backref='guests')
    guest = pw.ForeignKeyField(User, backref='events')