'''
SSL helper functions
Author: Philipp Schmitt <philipp@schmitt.co>
'''

import hashlib
import openssl_cmds as sslcmd
import os
from base64 import b64encode
from collections import namedtuple
from utils import shell_exec

# Where the keys are located
KEYSTORE = '/tmp'


def get_salt(length=1024, encoding='utf-8'):
    '''
    Get a random salt value
    '''
    # TODO CSPRNG python implementation to generate the salt
    return b64encode(os.urandom(length)).decode(encoding)


def keystore_path(username):
    '''
    Get the path to a user's keystore
    '''
    return os.path.join(KEYSTORE, username)


def get_keypair(username):
    '''
    Return a tuple holding both the private and the public key
    '''
    Keypair = namedtuple('keypair', ['public', 'private'])
    p = keystore_path(username)
    pub = p + '_public.pem' if os.path.isfile(p + '_public.pem') else None
    priv = p + '_private.pem' if os.path.isfile(p + '_private.pem') else None
    return Keypair(pub, priv)


def salt_hash(plaintext, salt=None, encoding='utf-8'):
    '''
    Hash a string
    If no salt is given, a default random one will be used
    Return the hashed string and salt
    '''
    if salt is None:
        salt = get_salt()
    hashed = hashlib.sha512((plaintext + salt).encode(encoding)).hexdigest()
    return hashed, salt


def rsa_enc(username, password, verbose=False):
    '''
    Encrypt a password using someone's RSA key
    username: Whose key to use
    password: The key to encrypt
    Return the encrypted password
    '''
    return shell_exec(sslcmd.RSA_ENCRYPT.format(username, password),
                      verbose=verbose)


def rsa_dec(username, cipher, verbose=False):
    '''
    Decrypt a password using someone's RSA key
    username: Whose key to use
    cipher: Encrypted password
    Return the password as plain text
    '''
    return shell_exec(sslcmd.RSA_DECRYPT.format(username, cipher),
                      verbose=verbose)


def rsa_gen(username, passphrase, key_length=4096, verbose=False):
    '''
    Generate a new RSA keypair
    username: Name of the keypair
    passphrase: Passphrase used to open the generated keypair
    key_length: Length of the keypair to generate
    '''
    shell_exec(sslcmd.RSA_GEN_PRIVATE.format(
        os.path.join(KEYSTORE, username), passphrase, key_length
    ), verbose=verbose)
    shell_exec(sslcmd.RSA_GEN_PUBLIC.format(
        os.path.join(KEYSTORE, username), passphrase
    ), verbose=verbose)
    return os.path.join(KEYSTORE, username)
