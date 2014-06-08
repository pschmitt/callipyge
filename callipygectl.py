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
    group.add_argument('--purge',
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


def register_user(username, password, passphrase, verbose=False):
    '''
    Register a new user
    '''
    crypt.rsa_gen(username, passphrase, verbose=verbose)
    hashed_password, salt = crypt.salt_hash(password)
    Users.create(
        username=username,
        salt=str(salt),
        password=str(hashed_password)
    )


def unregister_user(username, password, passphrase, verbose=False):
    '''
    Unregister an existing user
    '''
    # TODO Access Control! Only the superuser should be allowed to remove
    # others
    u = Users.get(Users.username == username)
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
    if args.register:
        password = getpass.getpass('Password: ')
        passphrase = getpass.getpass('Passphrase: ')
        register_user(args.register, password, passphrase, verbose)
    if args.unregister:
        unregister_user(args.unregister, None, None, verbose)
    if args.grant:
        pass
    if args.purge:
        purge()
    if args.add:
        account_name, hostname = tuple(args.add.split('@', 1))
        user = input('Callipyge username: ')
        password = getpass.getpass('Password: ')
        account_password = getpass.getpass('Account password: ')
        add_credentials(
            hostname, user, password, account_name, account_password,
            verbose=verbose
        )
