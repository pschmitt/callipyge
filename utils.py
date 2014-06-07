'''

'''

def decompose(string):
    '''
    Decompose a string like "user@host"
    '''
    dec = string.split('@', 1)
    return dec[0], dec[1]

if __name__ == '__main__':
    assert decompose('root@localhost') == ('root', 'localhost')
    print('All test passed successfully')
