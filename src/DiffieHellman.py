from Crypto.PublicKey import ECC
from Crypto.Hash import SHAKE128
from Crypto.Protocol.DH import key_agreement
import time

#TODO implement socket between alice and bob and account for network delays

# This KDF has been agreed in advance
def kdf(x):
        return SHAKE128.new(x).read(32)

start_time = time.time()

# Alice private key
private_key = ECC.generate(curve='secp256r1')

# Alice receives this public key from Bob
public_key = ECC.generate(curve='secp256r1').public_key()

# Alice derives session key
session_key = key_agreement(static_priv=private_key, static_pub=public_key, kdf=kdf)

end_time = time.time() - start_time

print("\n", end_time, "\n")
print(session_key)

# session_key is an AES-256 key
# Code taken from pycryptodome's website