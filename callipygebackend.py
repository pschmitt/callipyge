'''

'''

from database import db_connect
from models.access_rights import AccessRights
from models.credentials import Credentials
from models.inventory import Inventory
from models.users import Users
from utils import shell_exec
from keyring.backend import KeyringBackend
import hashlib
import keyring
import os


class CallipygeBackend(KeyringBackend):
    '''
    Super secret backend
    '''
    priority = 1

    def __init__(self, username):
        self.user = username

    def getencrPwd(self, something):
        pass

    def getAccesspwd(self, service, username):
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
            cipher = self.getencrPwd(0)
            decrPwd = shell_exec('openssl rsautl -decrypt -inkey ' +
                                 username + '_private.pem <<<' + cipher)
        else:
            raise NameError("You don't have access to the requested host")
        return decrPwd

    def set_password(self, service, username, password):
        '''
        Set a (new) password
        '''
        str = 'openssl rsautl -encrypt -inkey ' + self.user + \
              '_public.pem -pubin <<< ' + password
        res = shell_exec(str, verbose=True)
        Inventory.create(hostname=service, account_name=username,
                         account_password=res)

    def delete_password(self, service, username):
        '''
        Delete the password for the username of the service
        '''
        pass

    def define_access_rights(self, service, user, account):
        inv = Inventory.get(hostname=service, account_name=account)
        ar = AccessRights.create(created_by=self.user.id,
                                 user=user.id, host=inv.id)
        cmd = 'openssl rsautl -decrypt -inkey PATH/' + self.user + \
              '_private.pem <<< ' + inv.account_password
        plain = shell_exec(cmd, verbose=True)
        cmd = 'openssl rsautl -encrypt -inkey ' + user + '_public.pem -pubin ' + \
              '<<< ' + plain
        cipher = shell_exec(cmd, verbose=True)
        Credentials.create(access=ar.identifier, password=cipher)

    def register_user(username, password, passphrase):
        shell_exec('openssl genrsa -aes256 -out ' + username +
                   '_private.pem -passout pass:' + passphrase + ' 4096')
        shell_exec('openssl rsa -in ' + username +
                   '_private.pem -outform PEM -pubout -out ' +
                   username + '_public.pem')
        # TODO find some CSPRNG in python to feed the salt
        salt = os.urandom(512)
        pwd = hashlib.sha512(password.encode('utf-8')+salt).hexdigest()
        Users.create(username=username, salt=salt, password=pwd)

if __name__ == '__main__':
    db_connect()
    c = CallipygeBackend('root')
    keyring.set_keyring(c)
    keyring.set_password('test@localhost', 'root', 'test')
    assert keyring.get_password('test@localhost', 'root') == 'test'
    print('All tests passed')
