'''
This file holds the openssl commands to be executed by the keyring backend
'''

RSA_DECRYPT = 'openssl rsautl -decrypt -inkey {}_private.pem <<< {}'
RSA_ENCRYPT = 'openssl rsautl -encrypt -inkey {}_public.pem -pubin <<< {}'

RSA_GEN_PRIVATE = 'openssl genrsa -aes256 -out {}_private.pem \
                   -passout pass:{} {}'
RSA_GEN_PUBLIC = 'openssl rsa -in {0}_private.pem -outform PEM -pubout \
                  -passin pass:{1} -out {0}_public.pem'
