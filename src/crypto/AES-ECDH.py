import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# ==================== ECDH Implementation ====================
class ECDH_Cryptosystem:
    @staticmethod
    def generate_keypair(curve_name="SECP256R1"):
        curve_map = {
            "SECP256R1": ec.SECP256R1,
            "SECP384R1": ec.SECP384R1,
            "SECP521R1": ec.SECP521R1,
        }
        curve_class = curve_map.get(curve_name, ec.SECP256R1)
        private_key = ec.generate_private_key(curve_class())
        return private_key, private_key.public_key()
    
    @staticmethod
    def derive_shared_secret(private_key, peer_public_key):
        return private_key.exchange(ec.ECDH(), peer_public_key)
    
    @staticmethod
    def derive_aes_key(shared_secret):
        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"aes-ecdh",
        ).derive(shared_secret)

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
    print("AES-ECDH PERFORMANCE METRICS")
    print("=" * 50)
    
    test_message = b"Test message for AES-ECDH performance analysis"
    
    # ========== 1. COMPUTATIONAL SPEED ==========
    print("\ncomputational speed:")
    print("-" * 20)
    
    # Generate ECDH keys
    alice_priv, alice_pub = ECDH_Cryptosystem.generate_keypair("SECP256R1")
    bob_priv, bob_pub = ECDH_Cryptosystem.generate_keypair("SECP256R1")
    
    # Measure ECDH key exchange
    iterations = 1000
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()
        shared_secret = ECDH_Cryptosystem.derive_shared_secret(alice_priv, bob_pub)
        aes_key = ECDH_Cryptosystem.derive_aes_key(shared_secret)
        total_time += time.perf_counter() - start_time
    ecdh_exchange_speed = (total_time / iterations) * 1000000  # μs
    
    # AES speed with derived key
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()
        cipher = AES_Cryptosystem.encrypt(aes_key, test_message)
        total_time += time.perf_counter() - start_time
    aes_enc_speed = (total_time / iterations) * 1000000  # μs
    
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()
        AES_Cryptosystem.decrypt(aes_key, cipher)
        total_time += time.perf_counter() - start_time
    aes_dec_speed = (total_time / iterations) * 1000000  # μs
    
    # Key generation speed
    start_time = time.perf_counter()
    ECDH_Cryptosystem.generate_keypair("SECP256R1")
    ecdh_keygen_speed = (time.perf_counter() - start_time) * 1000000  # μs
    
    print(f"ECDH-P256 Key Generation: {ecdh_keygen_speed:.2f} μs")
    print(f"ECDH Key Exchange: {ecdh_exchange_speed:.2f} μs")
    print(f"AES-256 Encryption: {aes_enc_speed:.2f} μs")
    print(f"AES-256 Decryption: {aes_dec_speed:.2f} μs")
    print(f"Total Setup Time: {ecdh_keygen_speed + ecdh_exchange_speed:.2f} μs")
    
    # ========== 2. KEY SIZE ==========
    print("\nkey size:")
    print("-" * 20)
    
    # ECDH key sizes for different curves
    curves = [
        ("P-256 (SECP256R1)", 256, 32, 33),
        ("P-384 (SECP384R1)", 384, 48, 49),
        ("P-521 (SECP521R1)", 521, 66, 67),
    ]
    
    for curve_name, bits, priv_bytes, pub_bytes in curves:
        print(f"ECDH-{curve_name}:")
        print(f"  Private Key: {priv_bytes} bytes = {priv_bytes * 8} bits")
        print(f"  Public Key: {pub_bytes} bytes = {pub_bytes * 8} bits (compressed)")
    
    # AES key size
    print(f"\nAES-256 Key: 32 bytes = 256 bits")
    
    # Total sizes
    print(f"\nAES-ECDH Hybrid (P-256):")
    print(f"  ECDH Private: 32 bytes")
    print(f"  ECDH Public: 33 bytes")
    print(f"  AES Session Key: 32 bytes")
    print(f"  Total: ~97 bytes")
    
    # ========== 3. BRUTE-FORCE ATTACK RESISTANCE ==========
    print("\nbrute-force attack resistance:")
    print("-" * 20)
    
    # AES-256 brute-force calculations
    aes_key_space = 2**256
    print(f"AES-256 Key Space: 2^256 = {aes_key_space:.2e} possible keys")
    
    # Operations needed to be vulnerable
    print("\nAES-256 Vulnerability Threshold:")
    print("Standard assumption: 1 trillion (10^12) keys/second")
    seconds_per_year = 365.25 * 24 * 3600
    
    # Calculate different vulnerability thresholds
    thresholds = {
        "Theoretical limit": 2**256,
        "50% probability": 2**255,
        "Practical limit (classical)": 2**128,
        "Quantum limit (Grover's)": 2**128,
        "Current feasible": 2**80
    }
    
    for scenario, operations in thresholds.items():
        years = operations / 1e12 / seconds_per_year
        print(f"  {scenario:<25}: {operations:.2e} operations = {years:.2e} years")
    
    # ECDH brute-force (ECDLP)
    print("\nECDH-P256 Brute-force (ECDLP):")
    ecdl_complexity = 2**128  # 256-bit curve provides 128-bit security
    print(f"  Best classical algorithm (Pollard's Rho): 2^{128} operations")
    print(f"  Operations to solve ECDLP: {ecdl_complexity:.2e}")
    
    # When it becomes vulnerable
    print("\nWhen AES-ECDH becomes vulnerable:")
    print("  AES-256 vulnerable when attacker can perform > 2^128 operations")
    print("  ECDH-P256 vulnerable when attacker can perform > 2^64 operations")
    print("  Current status: Secure against classical attacks")
    
    # Quantum impact
    print("\nQuantum Computer Impact:")
    print("  AES-256 with Grover's: 2^128 operations needed")
    print("  ECDH-P256 with Shor's: 2^64 operations needed")
    
    # Vulnerability thresholds table
    print("\nVULNERABILITY THRESHOLD TABLE:")
    print("-" * 70)
    print(f"{'Component':<15} {'Attack Type':<20} {'Operations to Break':<25} {'Status':<10}")
    print("-" * 70)
    
    thresholds_data = [
        ("AES-256", "Classical Brute-force", "2^256", "Secure"),
        ("AES-256", "Quantum (Grover's)", "2^128", "Secure"),
        ("ECDH-P256", "Classical (Pollard's)", "2^128", "Secure"),
        ("ECDH-P256", "Quantum (Shor's)", "2^64", "Vulnerable*"),
        ("ECDH-P384", "Classical", "2^192", "Secure"),
        ("ECDH-P384", "Quantum", "2^96", "Moderate"),
        ("ECDH-P521", "Classical", "2^260", "Very Secure"),
        ("ECDH-P521", "Quantum", "2^130", "Secure"),
    ]
    
    for component, attack_type, operations, status in thresholds_data:
        print(f"{component:<15} {attack_type:<20} {operations:<25} {status:<10}")
    
    # Summary of operations needed for vulnerability
    print("\nSUMMARY - Operations needed to be vulnerable:")
    print("-" * 50)
    print(f"AES-256 (Classical attack): > 2^128 operations")
    print(f"AES-256 (Quantum attack): > 2^64 operations")
    print(f"ECDH-P256 (Classical): > 2^64 operations")
    print(f"ECDH-P256 (Quantum): > 2^32 operations")
    print(f"ECDH-P384 (Quantum): > 2^48 operations")
    print(f"ECDH-P521 (Quantum): > 2^65 operations")
    
    # Practical implications
    print("\nPRACTICAL IMPLICATIONS:")
    print("-" * 30)
    print("For classical computers today:")
    print("  Safe threshold: < 2^80 operations")
    print("  Warning threshold: 2^80 - 2^96 operations")
    print("  Vulnerable threshold: > 2^96 operations")
    
    print("\nFor quantum computers (future):")
    print("  Safe threshold: < 2^64 operations")
    print("  Warning threshold: 2^64 - 2^80 operations")
    print("  Vulnerable threshold: > 2^80 operations")
    
    # Current security assessment
    print("\nCURRENT SECURITY ASSESSMENT:")
    print("-" * 30)
    print("AES-256 + ECDH-P256:")
    print("  Classical: Requires > 2^128 operations - SECURE")
    print("  Quantum: Requires > 2^64 operations - MODERATE RISK")
    
    print("\nAES-256 + ECDH-P521:")
    print("  Classical: Requires > 2^260 operations - VERY SECURE")
    print("  Quantum: Requires > 2^130 operations - SECURE")

if __name__ == "__main__":
    measure_performance()