'''
Inventory
Author: Philipp Schmitt
'''

from ..database import BaseModel
from peewee import CharField
from peewee import BlobField


class Inventory(BaseModel):
    '''
    Inventory
    '''
    account_name = CharField(max_length=100)
    account_password = BlobField()
    hostname = CharField(max_length=200)

    class Meta:
        db_table = 'inventory'
