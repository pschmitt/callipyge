'''
Various helper functions
'''

import subprocess
import sys


def decompose(string):
    '''
    Decompose a string like "user@host"
    '''
    dec = string.split('@', 1)
    return dec[0], dec[1]


def shell_exec(cmd, verbose=False):
    '''
    Execute a shell command an return its output
    Returns a list
    '''
    if verbose:
        print('Execute shell command %s' % cmd)
    try:
        output = subprocess.check_output(cmd, shell=True)
    except Exception as err:
        if verbose:
            print('Caught an exception {}'.format(err), file=sys.stderr)
        return None
    if verbose:
        print('Output: %s' % output)
    return output

if __name__ == '__main__':
    assert decompose('root@localhost') == ('root', 'localhost')
    assert shell_exec('echo -en test') == b'test'
    print('All test passed successfully')

