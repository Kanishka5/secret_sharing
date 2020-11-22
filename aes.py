import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

if __name__ == "__main__":
    codeStart = time.time()

    key = get_random_bytes(32)

    # encryption
    data = b"my data to encrypt."
    encryptCipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = encryptCipher.encrypt_and_digest(data)
    print(ciphertext, tag, encryptCipher.nonce)

    # decryption
    decryptCipher = AES.new(key, AES.MODE_EAX, encryptCipher.nonce)
    data = decryptCipher.decrypt_and_verify(ciphertext, tag)
    print(data)

    codeEnd = time.time()
    print("Execution time of code is: " + str(codeEnd - codeStart))
