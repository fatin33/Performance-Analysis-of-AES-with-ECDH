# Simple LUC public-key cryptosystem (educational version)

import random
from math import gcd

# --- LUC Key Generation ---
def generate_keypair(bits=256):
    # Very simple prime generator (for learning only)
    def get_prime():
        while True:
            n = random.getrandbits(bits // 2)
            if n % 2 != 0 and pow(2, n-1, n) == 1:  # Fermat test
                return n

    p = get_prime()
    q = get_prime()

    n = p * q
    v = (p - 2) * (q - 2)       # Lucas totient equivalent

    e = 65537                   # public exponent
    d = pow(e, -1, v)           # modular inverse

    return (e, n), (d, n)


# --- LUC Encryption ---
def encrypt(public_key, m):
    e, n = public_key
    return pow(m, e, n)


# --- LUC Decryption ---
def decrypt(private_key, c):
    d, n = private_key
    return pow(c, d, n)


# --- Test Example ---
if __name__ == "__main__":
    pub, priv = generate_keypair()

    message = 12345
    cipher = encrypt(pub, message)
    plain = decrypt(priv, cipher)

    print("Public key:", pub)
    print("Private key:", priv)
    print("Ciphertext:", cipher)
    print("Decrypted:", plain)
