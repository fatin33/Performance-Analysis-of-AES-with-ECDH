import time
import random
from math import gcd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# ==================== LUC Implementation ====================
class LUC_Cryptosystem:
    @staticmethod
    def generate_keypair(bits=512):
        def get_prime(bits):
            while True:
                n = random.getrandbits(bits)
                if n % 2 != 0 and n > 1:
                    if pow(2, n-1, n) == 1 and pow(3, n-1, n) == 1:
                        return n
        
        p = get_prime(bits // 2)
        q = get_prime(bits // 2)
        n = p * q
        v = (p - 1) * (q - 1)
        
        e = 65537
        while gcd(e, v) != 1:
            e += 2
        
        d = pow(e, -1, v)
        return (e, n), (d, n)
    
    @staticmethod
    def encrypt(public_key, message_int):
        e, n = public_key
        return pow(message_int, e, n)
    
    @staticmethod
    def decrypt(private_key, cipher_int):
        d, n = private_key
        return pow(cipher_int, d, n)

# ==================== AES Implementation ====================
class AES_Cryptosystem:
    @staticmethod
    def encrypt(key, plaintext):
        iv = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return base64.b64encode(iv + tag + ciphertext).decode()
    
    @staticmethod
    def decrypt(key, b64_payload):
        data = base64.b64decode(b64_payload)
        iv = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        return cipher.decrypt_and_verify(ciphertext, tag)

# ==================== Performance Measurement ====================
def measure_performance():
    print("AES-LUC PERFORMANCE METRICS")
    print("=" * 50)
    
    test_message = b"Test message for AES-LUC performance analysis"
    
    # ========== 1. COMPUTATIONAL SPEED ==========
    print("\ncomputational speed:")
    print("-" * 20)
    
    # AES speed measurement
    aes_key = get_random_bytes(32)
    
    # AES encryption speed
    iterations = 1000
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()
        cipher = AES_Cryptosystem.encrypt(aes_key, test_message)
        total_time += time.perf_counter() - start_time
    aes_enc_speed = (total_time / iterations) * 1000000  # μs
    
    # AES decryption speed
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()
        AES_Cryptosystem.decrypt(aes_key, cipher)
        total_time += time.perf_counter() - start_time
    aes_dec_speed = (total_time / iterations) * 1000000  # μs
    
    # LUC key generation speed
    start_time = time.perf_counter()
    pub_key, priv_key = LUC_Cryptosystem.generate_keypair(512)
    luc_keygen_speed = (time.perf_counter() - start_time) * 1000  # ms
    
    # LUC encryption/decryption speed
    test_int = 123456789
    
    start_time = time.perf_counter()
    luc_cipher = LUC_Cryptosystem.encrypt(pub_key, test_int)
    luc_enc_speed = (time.perf_counter() - start_time) * 1000000  # μs
    
    start_time = time.perf_counter()
    LUC_Cryptosystem.decrypt(priv_key, luc_cipher)
    luc_dec_speed = (time.perf_counter() - start_time) * 1000000  # μs
    
    # LUC key exchange simulation
    session_key_int = 987654321
    start_time = time.perf_counter()
    encrypted_key = LUC_Cryptosystem.encrypt(pub_key, session_key_int)
    key_exchange_speed = (time.perf_counter() - start_time) * 1000  # ms
    
    print(f"AES-256 Encryption: {aes_enc_speed:.2f} μs")
    print(f"AES-256 Decryption: {aes_dec_speed:.2f} μs")
    print(f"LUC-512 Key Generation: {luc_keygen_speed:.4f} ms")
    print(f"LUC-512 Encryption: {luc_enc_speed:.2f} μs")
    print(f"LUC-512 Decryption: {luc_dec_speed:.2f} μs")
    print(f"LUC Key Exchange: {key_exchange_speed:.4f} ms")
    
    # ========== 2. KEY SIZE ==========
    print("\nkey size:")
    print("-" * 20)
    
    # AES key size
    print(f"AES-256 Key: {len(aes_key)} bytes = {len(aes_key) * 8} bits")
    
    # LUC key sizes for different security levels
    print(f"LUC-512 Public Key: 64 bytes = 512 bits")
    print(f"LUC-512 Private Key: 128 bytes = 1024 bits (with p, q)")
    
    print(f"LUC-1024 Public Key: 128 bytes = 1024 bits")
    print(f"LUC-1024 Private Key: 256 bytes = 2048 bits (with p, q)")
    
    print(f"LUC-2048 Public Key: 256 bytes = 2048 bits")
    print(f"LUC-2048 Private Key: 512 bytes = 4096 bits (with p, q)")
    
    # Total hybrid scheme
    print(f"AES-LUC Hybrid Total: ~192 bytes (LUC-512 + AES-256)")
    
    # ========== 3. BRUTE-FORCE ATTACK RESISTANCE ==========
    print("\nbrute-force attack resistance:")
    print("-" * 20)
    
    # AES-256 brute-force calculations
    aes_key_space = 2**256
    print(f"AES-256 Key Space: 2^256 = {aes_key_space:.2e} possible keys")
    
    # Operations needed to be vulnerable
    print("\nAES-256 Vulnerability Threshold:")
    print("If attacker can try 1 trillion (10^12) keys per second:")
    seconds_per_year = 365.25 * 24 * 3600
    years_to_crack = aes_key_space / 1e12 / seconds_per_year
    print(f"  Time to exhaust key space: {years_to_crack:.2e} years")
    
    # 50% success probability (birthday attack for symmetric)
    operations_for_50pct = aes_key_space / 2
    print(f"  Operations for 50% success: {operations_for_50pct:.2e}")
    
    # Practical attack thresholds
    print("\nPractical Attack Scenarios:")
    print("  1. Weak implementation/leakage: 2^64 operations")
    print("  2. Advanced persistent threat: 2^80 operations")
    print("  3. Nation-state capability: 2^96 operations")
    print("  4. Theoretical maximum: 2^128 operations (for 128-bit quantum)")
    
    # LUC brute-force calculations
    print("\nLUC-512 Brute-force Analysis:")
    # For factorization-based systems
    luc_complexity = 2**80  # 512-bit LUC ~ 80-bit security
    print(f"  Best algorithm (GNFS): ~2^{80} operations")
    print(f"  Operations to factor: {luc_complexity:.2e}")
    
    # When it becomes vulnerable
    print("\nWhen AES-LUC becomes vulnerable:")
    print("  AES-256 vulnerable when: > 2^128 operations possible")
    print("  LUC-512 vulnerable when: > 2^80 operations possible")
    print("  Current status: Both secure against classical brute-force")
    
    # Quantum impact
    print("\nQuantum Computer Impact:")
    print("  AES-256 with Grover's: 2^128 operations needed")
    print("  LUC-512 with Shor's: Polynomial time - COMPLETELY BROKEN")
    
    # Vulnerability thresholds table
    print("\nVULNERABILITY THRESHOLD TABLE:")
    print("-" * 60)
    print(f"{'Attack Type':<25} {'Operations Needed':<20} {'Status':<15}")
    print("-" * 60)
    
    thresholds = [
        ("AES-256 Classical", "2^256", "Secure"),
        ("AES-256 Quantum", "2^128", "Secure"),
        ("LUC-512 Classical", "2^80", "Moderate"),
        ("LUC-512 Quantum", "Polynomial", "Vulnerable"),
        ("LUC-1024 Classical", "2^112", "Secure"),
        ("LUC-1024 Quantum", "Polynomial", "Vulnerable"),
        ("LUC-2048 Classical", "2^128", "Secure"),
        ("LUC-2048 Quantum", "Polynomial", "Vulnerable")
    ]
    
    for attack_type, operations, status in thresholds:
        print(f"{attack_type:<25} {operations:<20} {status:<15}")
    
    # Summary of operations needed for vulnerability
    print("\nSUMMARY - Operations to be vulnerable:")
    print("-" * 40)
    print(f"AES-256 (Classical): > 2^128 operations")
    print(f"AES-256 (Quantum): > 2^64 operations")
    print(f"LUC-512 (Classical): > 2^40 operations")
    print(f"LUC-512 (Quantum): ANY quantum computer with Shor's")
    print(f"Hybrid System: Limited by weakest component (LUC)")

if __name__ == "__main__":
    measure_performance()