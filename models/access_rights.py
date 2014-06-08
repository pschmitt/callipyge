'''
AccessRights
Author: Philipp Schmitt
'''

from models.inventory import Inventory
from models.users import Users
from database import BaseModel
from peewee import PrimaryKeyField
from peewee import ForeignKeyField


class AccessRights(BaseModel):
    '''
    AccessRights
    '''
    identifier = PrimaryKeyField(db_column='id')
    host = ForeignKeyField(db_column='host_id', rel_model=Inventory)
    user = ForeignKeyField(db_column='user_id', related_name='user', rel_model=Users)
    created_by = ForeignKeyField(db_column='created_by', related_name='created', rel_model=Users)

    class Meta:
        db_table = 'access_rights'
