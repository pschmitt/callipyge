import keyring
from peewee import PostgresqlDatabase
from peewee import Model

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'callipyge'
DB_USER = 'callipyge'
DB_PASS = keyring.get_password('db-' + DB_HOST, DB_USER)

# Defer loading
db = PostgresqlDatabase(None, threadlocals=True)


def db_connect(host=None, port=None, database=None,
               user=None, password=None):
    '''
    Initialize our database
    '''
    if host is None:
        host = DB_HOST
    if port is None:
        port = DB_PORT
    if database is None:
        database = DB_NAME
    if user is None:
        user = DB_USER
    if password is None:
        password = DB_PASS
    db.init(database,
            port=port,
            host=host,
            user=user,
            password=password)


class BaseModel(Model):
    '''
    Base model for the selected database backend.
    '''
    class Meta:
        database = db
