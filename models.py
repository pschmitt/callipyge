'''
Models
Author: Philipp Schmitt
'''

from database import BaseModel
from models.inventory import Inventory
from models.users import Users
from models.users import Users
from peewee import BlobField
from peewee import CharField
from peewee import ForeignKeyField
from peewee import PrimaryKeyField


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



class Credentials(BaseModel):

    '''
    Credentials
    '''
    identifier = PrimaryKeyField(db_column='id')
    access = CharField(db_column='access_id', max_length=45)
    password = BlobField()

    class Meta:
        db_table = 'credentials'


class Inventory(BaseModel):
    '''
    Inventory
    '''
    identifier = PrimaryKeyField(db_column='id')
    account_name = CharField(max_length=100)
    account_password = BlobField()
    hostname = CharField(max_length=200)
    created_by = ForeignKeyField(rel_model=Users)

    class Meta:
        db_table = 'inventory'


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
