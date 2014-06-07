'''
AccessRights
Author: Philipp Schmitt
'''

from .inventory import Inventory
from .users import Users
from ..database import BaseModel
from peewee import PrimaryKeyField
from peewee import ForeignKeyField


class AccessRights(BaseModel):
    host = ForeignKeyField(db_column='host_id', rel_model=Inventory)
    user = ForeignKeyField(db_column='user_id', rel_model=Users)

    class Meta:
        db_table = 'access_rights'
