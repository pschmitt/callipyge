'''
Inventory
Author: Philipp Schmitt
'''

from ..database import BaseModel
from .users import Users
from peewee import BlobField
from peewee import CharField
from peewee import ForeignKeyField


class Inventory(BaseModel):
    '''
    Inventory
    '''
    account_name = CharField(max_length=100)
    account_password = BlobField()
    hostname = CharField(max_length=200)
    created_by = ForeignKeyField(rel_model=Users)

    class Meta:
        db_table = 'inventory'
