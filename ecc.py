import time
import random
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

if __name__ == "__main__":
    codeStart = time.time()

    privateKey = generate_eth_key()
    publicKey = privateKey.public_key
    secret = b'hello world'
    encrytSecret = encrypt(publicKey.to_hex(), secret)
    print(decrypt(privateKey.to_hex(), encrytSecret))

    codeEnd = time.time()
    print("Execution time of code is: " + str(codeEnd - codeStart))
