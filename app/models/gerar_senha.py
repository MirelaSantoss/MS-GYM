import hashlib
import secrets


senha = "123456"

salt = secrets.token_bytes(16)

hash_senha = hashlib.pbkdf2_hmac(
    "sha256",
    senha.encode("utf-8"),
    salt,
    600000
)

print(
    "pbkdf2_sha256$600000$"
    + salt.hex()
    + "$"
    + hash_senha.hex()
)