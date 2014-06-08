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


def parse_args():
    '''
    Parse the command line args
    '''
    parser = argparse.ArgumentParser(description='Process args')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--register',
                       action='store',
                       help='Register a new user')
    group.add_argument('--unregister',
                       action='store',
                       help='Unregister an existing user')
    group.add_argument('--grant',
                       action='store',
                       help='Grant access to credentials to USER')
    parser.add_argument('--login',
                        action='store',
                        help='Check credentials by logging in')
    parser.add_argument('--purge',
                        action='store_true',
                        help='Truncate all tables (remove ALL data)')
    group.add_argument('--add',
                       action='store',
                       help='Add new credentials')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Verbose output')
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
    db_connect()
    if args.purge:
        purge()
    if args.login:
        password = getpass.getpass('Password: ')
        if log_in(args.login, password):
            print('Success')
        else:
            print('Failure')
    if args.register:
        password = getpass.getpass('Password: ')
        # passphrase = getpass.getpass('Passphrase: ')
        register_user(args.register, password, verbose=verbose)
    if args.unregister:
        root_password = getpass.getpass('Admin password: ')
        unregister_user(args.unregister, root_password, verbose)
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
