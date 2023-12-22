import secrets
import base64


def generate_aes256_gcm_key():
    key_length = 32  # 256 bits key length
    key = secrets.token_bytes(key_length)
    return base64.b64encode(key).decode()


if __name__ == "__main__":
    aes_key = generate_aes256_gcm_key()
    print("Base64 key:", aes_key)
