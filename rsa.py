import time
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

if __name__ == "__main__":
    codeStart = time.time()

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    data = "I met aliens in UFO. Here is the map.".encode("utf-8")
    recipient_key = RSA.import_key(public_key)
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    codeEnd = time.time()
    print("Execution time of code is: " + str(codeEnd - codeStart))
