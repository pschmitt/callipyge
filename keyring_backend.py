'''

'''

import keyring
from keyring.backend import KeyringBackend


class CallipygeBackend(KeyringBackend):
    '''
    Super secret backend
    '''
    priority = 1

    def __init__(self):
        pass

    def get_password(self, service, username):
        '''
        Read the LIST (!) of password
        '''
	list=username.split('@',1)
	if len(list) !=2
		raise NameError("host format must be user@host")
	bool=getAccesspwd(list[0],list[1])
	if bool:
        	cipher=getencrPwd(list[0])
        	decrPwd=echo "$cipher" | openssl rsautl -decrypt -inkey $USERNAME_private.pem
        	connectTo(this.user,host,decrPwd)
        else:
		raise NameError("you don't have access to requested host using this user")
	pass

    def set_password(self, service, username, password):
        '''
        Set a (new) password
        '''
        pass

    def delete_password(self, service, username):
        '''
        Delete the password for the username of the service
        '''
        pass


if __name__ == '__main__':
    c = CallipygeBackend()
    keyring.set_keyring(c)
    keyring.set_password('test@localhost', 'root', 'test')
    assert keyring.get_password('test@localhost', 'root') == 'test'
    print('All tests passed')
