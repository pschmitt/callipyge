'''
Users
Author: Philipp Schmitt
'''

from ..database import BaseModel
from peewee import CharField
from peewee import TextField


class Users(BaseModel):
    '''
    Users
    '''
    password = CharField(max_length=200)
    public_key = TextField()
    salt = CharField(max_length=100)
    username = CharField(max_length=100)

    class Meta:
        db_table = 'users'

