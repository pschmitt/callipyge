'''
CallipygeBackend
Author: Philipp Schmitt
'''

from database import db_connect
from models import AccessRights
from models import Inventory
from models import Users
from keyring.backend import KeyringBackend
import keyring
import crypt


class CallipygeBackend(KeyringBackend):
    '''
    Super secret backend
    '''
    priority = 1

    def __init__(self, username, verbose=False):
        self.user = Users.get(username=username)
        self.verbose = verbose

    def get_encrypted_password(self, something):
        '''
        TODO What's this supposed to do?
        Return the encrypted password of a user?
        '''
        pass

    def get_access_password(self, service, username):
        '''
        TODO What's this supposed to do?
        '''
        pass

    def check_access_right(self, host, account_name):
        '''
        Check whether a given user has the right to access some credentials
        Return the ID of the corresponding AccessRights and -1 if not allowed
        '''
        pass

    def get_password(self, service, username):
        '''
        Read the LIST (!) of password
        '''
        access_id = self.check_access_right(service, username)
        if access_id != -1:
            # TODO
            cipher = self.get_encrypted_password(0)
            plaintext = crypt.rsa_dec(self.user, cipher)
        else:
            raise NameError("You don't have access to the requested host")
        return plaintext

    def set_password(self, service, username, password):
        '''
        Set a (new) password
        '''
        enc_pass = crypt.rsa_enc(self.user, password, verbose=self.verbose)
        Inventory.create(hostname=service, account_name=username,
                         account_password=enc_pass)

    def delete_password(self, service, username):
        '''
        Delete the password for the username of the service
        '''
        inv = Inventory.get(
            (Inventory.account_name) == username &
            (Inventory.hostname == service)
        )
        inv.delete_instance()

if __name__ == '__main__':
    db_connect()
    c = CallipygeBackend('root', True)
    keyring.set_keyring(c)
    keyring.set_password('test@localhost', 'root', 'test')
    assert keyring.get_password('test@localhost', 'root') == 'test'
    print('All tests passed')

# vim: set ft=python et ts=4 sw=4:
