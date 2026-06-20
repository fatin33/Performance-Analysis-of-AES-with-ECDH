# Simple LUC public-key algorithm (educational)
# Note: This is not optimized and not secure for production use

import random
from math import gcd

def generate_keypair(bits=512):
    # generate primes p and q
    def get_prime():
        while True:
            n = random.getrandbits(bits//2)
            if n % 2 != 0:
                if pow(2, n-1, n) == 1:  # Fermat test
                    return n

    p = get_prime()
    q = get_prime()

    n = p * q
    v = (p - 2)*(q - 2)            # LUC equivalent to φ(n)

    e = 65537                      # public exponent
    d = pow(e, -1, v)              # modular inverse

    return (e, n), (d, n)

def encrypt(public_key, message_int):
    e, n = public_key
    return pow(message_int, e, n)

def decrypt(private_key, cipher_int):
    d, n = private_key
    return pow(cipher_int, d, n)


# Example usage
if __name__ == "__main__":
    pub, priv = generate_keypair()

    message = 12345
    cipher = encrypt(pub, message)
    plain = decrypt(priv, cipher)

    print("Cipher:", cipher)
    print("Plain:", plain)
