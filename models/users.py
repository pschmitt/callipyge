'''
Users
Author: Philipp Schmitt
'''

from database import BaseModel
from peewee import CharField
from peewee import PrimaryKeyField


class Users(BaseModel):
    '''
    Users
    '''
    identifier = PrimaryKeyField(db_column='id')
    password = CharField(max_length=200)
    salt = CharField(max_length=100)
    username = CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'users'
