import time
import binascii
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

if __name__ == "__main__":
    codeStart = time.time()

    # key generate
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()

    # encryption
    data = b"my data to encrypt."
    encryptor = PKCS1_OAEP.new(public_key)
    encrypt = encryptor.encrypt(data)
    print("Encrypted:", binascii.hexlify(encrypt))

    # decryption
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(encrypt)
    print('Decrypted:', decrypted)

    codeEnd = time.time()
    print("Execution time of code is: " + str(codeEnd - codeStart))
