'''
Credentials
Author: Philipp Schmitt
'''

from database import BaseModel
from peewee import CharField
from peewee import BlobField

class Credentials(BaseModel):

    '''
    Credentials
    '''
    access = CharField(db_column='access_id', max_length=45)
    password = BlobField()

    class Meta:
        db_table = 'credentials'
