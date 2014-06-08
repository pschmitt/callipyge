'''
Credentials
Author: Philipp Schmitt
'''

from database import BaseModel
from peewee import CharField
from peewee import BlobField
from peewee import PrimaryKeyField


class Credentials(BaseModel):

    '''
    Credentials
    '''
    identifier = PrimaryKeyField(db_column='id')
    access = CharField(db_column='access_id', max_length=45)
    password = BlobField()

    class Meta:
        db_table = 'credentials'
