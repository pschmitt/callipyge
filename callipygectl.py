#!/usr/bin/python
# -*- coding: utf-8 -*-

from callipygebackend import CallipygeBackend
from database import db_connect
from models.access_rights import AccessRights
from models.inventory import Inventory
from models.credentials import Credentials
from models.users import Users
import argparse
import crypt
import getpass
import keyring

PASSWORD_DEFAULT = 'SOMERANDOMGIBBERISH'


def parse_args():
    '''
    Parse the command line args
    '''
    parser = argparse.ArgumentParser(description='Process args')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--register',
                       action='store',
                       help='Register a new user')
    group.add_argument('--unregister',
                       action='store',
                       help='Unregister an existing user')
    group.add_argument('-g', '--grant',
                       action='store',
                       help='Grant access to credentials to USER')
    parser.add_argument('-l', '--login',
                        action='store_true',
                        help='Check credentials by logging in')
    parser.add_argument('--purge',
                        action='store_true',
                        help='Truncate all tables (remove ALL data)')
    group.add_argument('-a', '--add',
                       action='store',
                       help='Add new credentials')
    group.add_argument('--init',
                       action='store_true',
                       help='Initialise the database')
    parser.add_argument('-u', '--user',
                        action='store',
                        help='Callipyge username')
    parser.add_argument('-p', '--password',
                        action='store',
                        nargs='?',
                        const=PASSWORD_DEFAULT,
                        help='Callipyge username')
    parser.add_argument('-H', '--db-host',
                        dest='db_host',
                        action='store',
                        help='Database host (host:port)')
    parser.add_argument('-N', '--db-name',
                        dest='db_name',
                        action='store',
                        help='Database to connect to')
    parser.add_argument('-U', '--db-user',
                        dest='db_user',
                        action='store',
                        help='Database username')
    parser.add_argument('-P', '--db-password',
                        dest='db_password',
                        action='store',
                        nargs='?',
                        const=PASSWORD_DEFAULT,
                        help='Database password')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Verbose output')
    parser.add_argument('-D', '--debug',
                        action='store_true',
                        help=argparse.SUPPRESS)
    return parser.parse_args()


def grant(hostname, user, account_name, verbose=False):
    '''
    Grant access to some credentials
    '''
    inv = Inventory.get(hostname=hostname, account_name=account_name)
    ar = AccessRights.create(created_by=user.identifier,
                             user=user.identifier, host=inv.identifier)
    plaintext = crypt.rsa_dec(user, inv.account_password, verbose)
    cipher = crypt.rsa_enc(user, plaintext)
    Credentials.create(access=ar.identifier, password=cipher)


def register_user(username, password, passphrase=None, verbose=False):
    '''
    Register a new user
    '''
    if passphrase is None:
        passphrase = password
    crypt.rsa_gen(username, passphrase, verbose=verbose)
    hashed_password, salt = crypt.salt_hash(password)
    Users.create(
        username=username,
        salt=salt,
        password=hashed_password
    )


def log_in(username, password, verbose=False):
    '''
    Try to log in using the specified credentials
    If login is successfull the corresponding Users row is returned
    Else False is returned
    '''
    try:
        user = Users.get(Users.username == username)
        hashed_password, salt = crypt.salt_hash(
            plaintext=password,
            salt=user.salt
        )
        # if verbose:
        #     print('HASHED_PW:', hashed_password, '\n',
        #           'USER PW: ', user.password, '\n',
        #           'SALT:    ', salt, '\n'
        #           'USER SALT', user.salt, '\n',
        #           'PASSWORD :', password, '\n',
        #           file=sys.stderr)
        if user.password == hashed_password:
            return user
        else:
            return False
    except Users.DoesNotExist:
        return False
    return False


def unregister_user(username, password, control_user=None, verbose=False):
    '''
    Unregister an existing user
    '''
    if control_user is not None:
        # Try to log in as admin
        if not log_in(control_user, password):
            return False
    u = log_in(username, password)
    if not u:
        return False
    u.delete_instance()
    # TODO remove RSA Keypair


def purge():
    '''
    Truncate all tables
    '''
    Users.delete().execute()
    Inventory.delete().execute()
    AccessRights.delete().execute()
    Credentials.delete().execute()


def add_credentials(user, password, hostname, account_name,
                    account_password, verbose=False):
    '''
    Add a new Inventory item
    '''
    c = CallipygeBackend(user, verbose)
    keyring.set_keyring(c)
    c.set_password(account_name, account_password)


if __name__ == '__main__':
    args = parse_args()
    verbose = args.verbose

    user = args.user
    password = args.password
    # Prompt for password if no password was provided
    if password == PASSWORD_DEFAULT:
        password = getpass.getpass('Callipyge password: ')

    # Connect to database
    db_host = db_port = None
    if args.db_host is not None:
        db_host, db_port = args.db_host.split(':', 1)
    # Prompt for password if no password was provided
    db_password = args.db_password
    if db_password == PASSWORD_DEFAULT:
        db_password = getpass.getpass('Database password: ')
    db_connect(
        host=db_host,
        port=db_port,
        database=args.db_name,
        user=args.db_user,
        password=db_password
    )

    # The real action start here
    if args.purge:
        purge()
    if args.login:
        if log_in(user, password):
            print('Success')
        else:
            print('Failure')
    if args.register:
        password = getpass.getpass('Password: ')
        # passphrase = getpass.getpass('Passphrase: ')
        register_user(args.register, password, verbose=verbose)
    if args.unregister:
        root_password = getpass.getpass('Admin password: ')
        unregister_user(
            args.unregister,
            password=root_password,
            verbose=verbose
        )
    if args.grant:
        pass
    if args.add:
        account_name, hostname = tuple(args.add.split('@', 1))
        user = input('Callipyge username: ')
        password = getpass.getpass('Password: ')
        account_password = getpass.getpass('Account password: ')
        add_credentials(
            hostname, user, password, account_name, account_password,
            verbose=verbose
        )
