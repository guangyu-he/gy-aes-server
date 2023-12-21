import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def aes_encrypt(plaintext, key) -> dict:
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode("utf-8")
    encrypted_text = base64.b64encode(ciphertext).decode("utf-8")
    return {"iv": iv, "encrypted_text": encrypted_text}


def aes_decrypt(iv, encrypted_text, key):
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CBC, base64.b64decode(iv))
    decrypted_text = unpad(cipher.decrypt(base64.b64decode(encrypted_text)), AES.block_size)
    return decrypted_text.decode("utf-8")


if __name__ == "__main__":
    encryption_key = os.getenv("FASTAPI_AES_KEY")[:32]

    original_data = "Hello, this is a string to be encrypted!"

    encrypted_dict = aes_encrypt(original_data, encryption_key)
    iv = encrypted_dict["iv"]
    encrypted_data = encrypted_dict["encrypted_text"]
    print("encrypted data:", encrypted_data)

    decrypted_data = aes_decrypt(iv, encrypted_data, encryption_key)
    print("decrypted data:", decrypted_data)
