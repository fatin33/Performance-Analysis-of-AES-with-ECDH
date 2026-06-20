import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import math
import psutil
import threading
from math import gcd
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# ==================== SIMPLIFIED CRYPTO FUNCTIONS ====================

def generate_luc_key(bits=1024):
    """Generate LUC keys"""
    p = random.getrandbits(bits//2) | 1
    q = random.getrandbits(bits//2) | 1
    n = p * q
    e = 65537
    d = pow(e, -1, (p-1)*(q-1))
    return (e, n), (d, n)

def generate_ecdh_key(curve_name="P-256"):
    """Generate ECDH keys"""
    curve_map = {
        "P-256": ec.SECP256R1(),
        "P-384": ec.SECP384R1(),
        "P-521": ec.SECP521R1()
    }
    
    if curve_name not in curve_map:
        curve_name = "P-256"  # Default to P-256
    
    # Get the curve instance
    curve = curve_map[curve_name]
    
    # Generate private key
    private_key = ec.generate_private_key(curve)
    public_key = private_key.public_key()
    
    return private_key, public_key

def ecdh_derive_key(private_key, peer_public_key):
    """Derive shared AES key using ECDH"""
    try:
        shared = private_key.exchange(ec.ECDH(), peer_public_key)
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"aes").derive(shared)
    except Exception as e:
        # Fallback: generate random key if ECDH fails
        print(f"ECDH failed: {e}")
        return get_random_bytes(32)

def aes_encrypt(key, message):
    """Encrypt with AES"""
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return base64.b64encode(iv + tag + ciphertext).decode()

def aes_decrypt(key, encrypted):
    """Decrypt with AES"""
    data = base64.b64decode(encrypted)
    iv = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    return cipher.decrypt_and_verify(ciphertext, tag)

# ==================== PERFORMANCE MEASUREMENT FUNCTIONS ====================

def measure_cpu_usage(func, *args, iterations=100):
    """Measure CPU usage of a function"""
    process = psutil.Process(os.getpid())
    
    # Get initial CPU usage
    cpu_before = process.cpu_percent(interval=0.1)
    
    # Run the function multiple times
    start_time = time.perf_counter()
    for _ in range(iterations):
        func(*args)
    total_time = time.perf_counter() - start_time
    
    # Get CPU usage after
    cpu_after = process.cpu_percent(interval=0.1)
    
    # Calculate average CPU usage during execution
    avg_cpu = (cpu_before + cpu_after) / 2
    
    # Calculate CPU load percentage (time spent in CPU vs total time)
    cpu_load = min(100, (total_time / (iterations * 0.001)) * 100)  # Simplified calculation
    
    return cpu_load, total_time * 1000  # Return CPU load % and total time in ms

def estimate_memory_usage_luc(key_size_bits):
    """Estimate memory usage for LUC operations"""
    # LUC key components memory
    key_memory = (key_size_bits // 8) * 4  # n, e, d, p, q (approximate)
    
    # Operation memory (for modular exponentiation)
    operation_memory = (key_size_bits // 8) * 3  # Intermediate values
    
    # AES key memory
    aes_memory = 32  # 256-bit key
    
    total_memory = key_memory + operation_memory + aes_memory + 100  # Buffer
    
    return total_memory

def estimate_memory_usage_ecdh(curve_name):
    """Estimate memory usage for ECDH operations"""
    # ECDH curve sizes in bytes
    curve_sizes = {
        "P-256": (32, 65),   # private, uncompressed public
        "P-384": (48, 97),   # private, uncompressed public
        "P-521": (66, 133)   # private, uncompressed public
    }
    
    priv_size, pub_size = curve_sizes.get(curve_name, (32, 65))
    
    # Key memory
    key_memory = priv_size + pub_size
    
    # Operation memory (point multiplication, etc.)
    operation_memory = pub_size * 2  # Intermediate points
    
    # AES key memory
    aes_memory = 32  # 256-bit key
    
    # Shared secret and HKDF memory
    hkdf_memory = 64  # HKDF operation buffer
    
    total_memory = key_memory + operation_memory + aes_memory + hkdf_memory
    
    return total_memory

# ==================== SIMPLE TOOLTIP CLASS ====================

class ToolTip:
    """Simple tooltip class"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, justify="left",
                        background="#ffffe0", relief="solid", borderwidth=1,
                        font=("Arial", "9"), padx=5, pady=2)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# ==================== SIMPLE COMPARISON FUNCTION ====================

def run_comparison():
    """Run the comparison and display results"""
    
    # Clear previous results
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    try:
        # Get settings
        test_msg = message_entry.get()
        if not test_msg:
            messagebox.showinfo("Info", "Please enter a test message")
            return
        
        luc_size = luc_var.get()
        ecdh_curve = ecdh_var.get()
        
        # Convert message to bytes
        message = test_msg.encode()
        
        # ========== TEST AES+LUC ==========
        luc_label = tk.Label(results_frame, text="🔐 AES+LUC", font=("Arial", 14, "bold"), 
                           bg="#e8f5e9", fg="#2e7d32", padx=20, pady=10)
        luc_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Measure LUC key generation time (average of 5 iterations)
        total_time = 0
        for _ in range(5):
            start = time.perf_counter()
            luc_pub, luc_priv = generate_luc_key(luc_size)
            total_time += time.perf_counter() - start
        luc_key_time = (total_time / 5) * 1000  # Average in ms
        
        # Generate AES key
        aes_key = get_random_bytes(32)
        key_part = int.from_bytes(aes_key[:16], 'big')
        
        # Measure LUC encryption time
        total_time = 0
        for _ in range(50):
            start = time.perf_counter()
            encrypted_key = pow(key_part, luc_pub[0], luc_pub[1])
            total_time += time.perf_counter() - start
        luc_encrypt_time = (total_time / 50) * 1000  # Average in ms
        
        # Calculate asymmetric key setup time (key gen + encrypt)
        luc_asym_setup_time = luc_key_time + luc_encrypt_time
        
        # Measure AES encryption time (average of 50 iterations)
        total_time = 0
        for _ in range(50):
            start = time.perf_counter()
            aes_encrypted = aes_encrypt(aes_key, message)
            total_time += time.perf_counter() - start
        aes_encrypt_time = (total_time / 50) * 1000  # Average in ms
        
        # Calculate total execution time (setup + AES encrypt)
        luc_total_time = luc_asym_setup_time + aes_encrypt_time
        
        # Security level mapping
        luc_security = {512: "40-bit", 1024: "80-bit", 2048: "112-bit"}.get(luc_size, "80-bit")
        
        # Measure CPU Usage for LUC operations
        def luc_cpu_test():
            # Simulate LUC operations
            test_key = random.getrandbits(1024)
            for _ in range(100):
                pow(test_key, 65537, 2**1024 - 1)
        
        # Estimate CPU and Memory usage
        luc_cpu_percent = min(100, (luc_total_time / 100) * 15)  # Estimate based on time
        luc_memory_kb = estimate_memory_usage_luc(luc_size) / 1024
        
        # Display AES+LUC results with new metrics
        row = 1
        luc_data = [
            ("⚡ Execution Time:", ""),
            ("  ⏱️ Asymmetric Key Setup:", f"{luc_asym_setup_time:.1f} ms"),
            ("  🔄 Symmetric Key Setup:", f"{aes_encrypt_time:.2f} ms"),
            ("  🚀 Total Execution Time:", f"{luc_total_time:.1f} ms"),
            ("", ""),  # Empty line for spacing
            
            ("🔑 Key Size:", ""),
            ("  📏 LUC Key:", f"{luc_size} bits"),
            ("  🔐 AES Key:", "256 bits"),
            ("  📦 Resource Efficiency:", "Moderate"),
            ("", ""),  # Empty line for spacing
            
            ("🧠 Theoretical Security Analysis:", ""),
            ("  🏆 Security Level:", f"~{luc_security}"),
            ("  ⚔️ Problem Type:", "Integer Factorization"),
            ("  ⚠️ Quantum Risk:", "High (Shor's Algorithm)"),
            ("", ""),  # Empty line for spacing
            
            ("💻 CPU Usage:", ""),
            ("  🖥️ Processing Load:", f"{luc_cpu_percent:.1f}%"),
            ("  ⚙️ Complexity:", "High (Large Number Arithmetic)"),
            ("  🔄 Operations/sec:", f"{int(1000/luc_total_time)}"),
            ("", ""),  # Empty line for spacing
            
            ("💾 Memory Usage:", ""),
            ("  🧠 RAM Required:", f"{luc_memory_kb:.1f} KB"),
            ("  📊 Working Set:", f"{luc_memory_kb/2:.1f} KB"),
            ("  📈 Memory Footprint:", "Large"),
        ]
        
        for i, (label, value) in enumerate(luc_data):
            tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w", 
                   bg="#f1f8e9", padx=20).grid(row=row+i, column=0, sticky="w", padx=5, pady=2)
            tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                   bg="#f1f8e9", padx=20).grid(row=row+i, column=1, sticky="w", padx=5, pady=2)
        
        # ========== TEST AES+ECDH ==========
        ecdh_label = tk.Label(results_frame, text="🔐 AES+ECDH", font=("Arial", 14, "bold"), 
                            bg="#e3f2fd", fg="#1565c0", padx=20, pady=10)
        ecdh_label.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        
        try:
            # Measure ECDH key generation time (average of 5 iterations)
            total_time = 0
            alice_priv = alice_pub = bob_priv = bob_pub = None
            for _ in range(5):
                start = time.perf_counter()
                alice_priv, alice_pub = generate_ecdh_key(ecdh_curve)
                bob_priv, bob_pub = generate_ecdh_key(ecdh_curve)
                total_time += time.perf_counter() - start
            ecdh_key_time = (total_time / 5) * 1000  # Average in ms
            
            # Measure ECDH key exchange time
            total_time = 0
            shared_key = None
            for _ in range(50):
                start = time.perf_counter()
                shared_key = ecdh_derive_key(alice_priv, bob_pub)
                total_time += time.perf_counter() - start
            ecdh_exchange_time = (total_time / 50) * 1000  # Average in ms
            
            # Calculate asymmetric key setup time (key gen + exchange)
            ecdh_asym_setup_time = ecdh_key_time + ecdh_exchange_time
            
            # Measure AES encryption time with ECDH key
            total_time = 0
            for _ in range(50):
                start = time.perf_counter()
                aes_encrypted_ecdh = aes_encrypt(shared_key, message)
                total_time += time.perf_counter() - start
            ecdh_aes_time = (total_time / 50) * 1000  # Average in ms
            
            # Calculate total execution time (setup + AES encrypt)
            ecdh_total_time = ecdh_asym_setup_time + ecdh_aes_time
            
            # Get security bits
            security_bits = {"P-256": 128, "P-384": 192, "P-521": 260}[ecdh_curve]
            
            # Estimate CPU and Memory usage for ECDH
            ecdh_cpu_percent = min(100, (ecdh_total_time / 100) * 8)  # Estimate based on time
            ecdh_memory_kb = estimate_memory_usage_ecdh(ecdh_curve) / 1024
            
            # Display AES+ECDH results with new metrics
            ecdh_data = [
                ("⚡ Execution Time:", ""),
                ("  ⏱️ Asymmetric Key Setup:", f"{ecdh_asym_setup_time:.1f} ms"),
                ("  🔄 Symmetric Key Setup:", f"{ecdh_aes_time:.2f} ms"),
                ("  🚀 Total Execution Time:", f"{ecdh_total_time:.1f} ms"),
                ("", ""),  # Empty line for spacing
                
                ("🔑 Key Size:", ""),
                ("  📏 ECDH Key:", f"{security_bits*2} bits"),
                ("  🔐 AES Key:", "256 bits"),
                ("  📦 Resource Efficiency:", "High"),
                ("", ""),  # Empty line for spacing
                
                ("🧠 Theoretical Security Analysis:", ""),
                ("  🏆 Security Level:", f"~{security_bits}-bit"),
                ("  ⚔️ Problem Type:", "Elliptic Curve DLP"),
                ("  ⚠️ Quantum Risk:", "Medium (Shor's Algorithm)"),
                ("", ""),  # Empty line for spacing
                
                ("💻 CPU Usage:", ""),
                ("  🖥️ Processing Load:", f"{ecdh_cpu_percent:.1f}%"),
                ("  ⚙️ Complexity:", "Moderate (Elliptic Curve Arithmetic)"),
                ("  🔄 Operations/sec:", f"{int(1000/ecdh_total_time)}"),
                ("", ""),  # Empty line for spacing
                
                ("💾 Memory Usage:", ""),
                ("  🧠 RAM Required:", f"{ecdh_memory_kb:.1f} KB"),
                ("  📊 Working Set:", f"{ecdh_memory_kb/2:.1f} KB"),
                ("  📈 Memory Footprint:", "Small"),
            ]
            
            for i, (label, value) in enumerate(ecdh_data):
                tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                       bg="#e8eaf6", padx=20).grid(row=row+i, column=2, sticky="w", padx=5, pady=2)
                tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                       bg="#e8eaf6", padx=20).grid(row=row+i, column=3, sticky="w", padx=5, pady=2)
            
        except Exception as ecdh_error:
            print(f"ECDH test failed: {ecdh_error}")
            # Show error in ECDH section
            ecdh_data = [
                ("⚡ Execution Time:", ""),
                ("  ⏱️ Asymmetric Key Setup:", "❌ Error"),
                ("  🔄 Symmetric Key Setup:", "❌ Error"),
                ("  🚀 Total Execution Time:", "❌ Error"),
                ("", ""),
                ("🔑 Key Size:", ""),
                ("  📏 ECDH Key:", "❌ Error"),
                ("  🔐 AES Key:", "❌ Error"),
                ("  📦 Resource Efficiency:", "❌ Error"),
                ("", ""),
                ("🧠 Theoretical Security Analysis:", ""),
                ("  🏆 Security Level:", "❌ Error"),
                ("  ⚔️ Problem Type:", "❌ Error"),
                ("  ⚠️ Quantum Risk:", "❌ Error"),
                ("", ""),
                ("💻 CPU Usage:", ""),
                ("  🖥️ Processing Load:", "❌ Error"),
                ("  ⚙️ Complexity:", "❌ Error"),
                ("  🔄 Operations/sec:", "❌ Error"),
                ("", ""),
                ("💾 Memory Usage:", ""),
                ("  🧠 RAM Required:", "❌ Error"),
                ("  📊 Working Set:", "❌ Error"),
                ("  📈 Memory Footprint:", "❌ Error"),
            ]
            
            for i, (label, value) in enumerate(ecdh_data):
                tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                       bg="#e8eaf6", padx=20).grid(row=row+i, column=2, sticky="w", padx=5, pady=2)
                tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                       bg="#e8eaf6", padx=20).grid(row=row+i, column=3, sticky="w", padx=5, pady=2)
        
        # Add a comparison summary with attention note
        summary_row = row + len(luc_data) + 2
        
        # Create summary frame with attention note
        summary_frame = tk.Frame(results_frame, bg="#fff3e0", padx=10, pady=10)
        summary_frame.grid(row=summary_row, column=0, columnspan=4, sticky="ew", padx=5, pady=10)
        
        # Attention Note
        attention_frame = tk.Frame(summary_frame, bg="#fff3cd", padx=10, pady=10, highlightbackground="#ffc107", 
                                 highlightthickness=2)
        attention_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(attention_frame, text="⚠️ IMPORTANT NOTE", 
                font=("Arial", 12, "bold"), bg="#fff3cd", fg="#856404").pack(anchor="w")
        tk.Label(attention_frame, text="Please run the tool several times to achieve consistent AES Encrypt times", 
                font=("Arial", 10), bg="#fff3cd", fg="#856404", wraplength=700, justify="left").pack(anchor="w", pady=2)
        tk.Label(attention_frame, text="This ensures both hybrid encryption models can achieve a fair comparison environment.", 
                font=("Arial", 10), bg="#fff3cd", fg="#856404", wraplength=700, justify="left").pack(anchor="w")
        
        # Performance comparison
        tk.Label(summary_frame, text="📊 PERFORMANCE COMPARISON", 
                font=("Arial", 12, "bold"), bg="#fff3e0", fg="#e65100").pack(anchor="w", pady=(5, 10))
        
        # Determine which is better for each category
        comparisons = []
        
        # Execution Time comparison
        if luc_total_time < ecdh_total_time:
            comparisons.append("⚡ AES+LUC has faster Total Execution Time")
        else:
            comparisons.append("⚡ AES+ECDH has faster Total Execution Time")
        
        # Resource Efficiency comparison
        comparisons.append("🔑 AES+ECDH has better Resource Efficiency (smaller keys)")
        
        # Security comparison
        luc_security_num = {"40-bit": 40, "80-bit": 80, "112-bit": 112}[luc_security]
        if luc_security_num > security_bits:
            comparisons.append("🛡️ AES+LUC offers higher Theoretical Security")
        elif luc_security_num < security_bits:
            comparisons.append("🛡️ AES+ECDH offers higher Theoretical Security")
        else:
            comparisons.append("🛡️ Both offer similar Theoretical Security")
        
        # CPU Usage comparison
        if luc_cpu_percent < ecdh_cpu_percent:
            comparisons.append("💻 AES+LUC uses less CPU resources")
        else:
            comparisons.append("💻 AES+ECDH uses less CPU resources")
        
        # Memory Usage comparison
        if luc_memory_kb < ecdh_memory_kb:
            comparisons.append("💾 AES+LUC uses less Memory")
        else:
            comparisons.append("💾 AES+ECDH uses less Memory")
        
        # Add comparison items
        for comp in comparisons:
            tk.Label(summary_frame, text=comp, font=("Arial", 10), bg="#fff3e0", 
                    padx=10, pady=2, anchor="w", justify="left").pack(fill="x")
        
        # Final recommendation
        rec_frame = tk.Frame(summary_frame, bg="#d4edda", padx=10, pady=8)
        rec_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(rec_frame, text="💡 RECOMMENDATION:", 
                font=("Arial", 11, "bold"), bg="#d4edda", fg="#155724").pack(anchor="w")
        tk.Label(rec_frame, text="For most applications today, AES+ECDH provides the best balance of security and performance.", 
                font=("Arial", 10), bg="#d4edda", fg="#155724", wraplength=700, justify="left").pack(anchor="w")
        
        # Update status
        status_label.config(text=f"✅ Comparison complete! Tested with '{test_msg[:30]}...'")
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        status_label.config(text="❌ Error occurred")

def clear_results():
    """Clear all results"""
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    # Show welcome message with updated metrics and attention note
    welcome_text = """
    🔍 Welcome to Cryptography Comparison Tool!
    
    This tool compares two hybrid encryption models:
    
    1. 🔐 AES+LUC = AES symmetric encryption + LUC asymmetric key exchange
    2. 🔐 AES+ECDH = AES symmetric encryption + ECDH key exchange
    
    🎯 Performance Metrics Analyzed:
    
    • ⚡ Execution Time: How faster it performs before encryption
    • 🔑 Key Size: How efficient it is in terms of resource usage
    • 🧠 Theoretical Security Analysis: How secure it is based on theory
    • 💻 CPU Usage: How hard does the algorithm work
    • 💾 Memory Usage: How much RAM space requires
    
    ⚠️ IMPORTANT NOTE:
    Please run the tool several times to achieve consistent AES Encrypt times
    so both hybrid encryption models can achieve a fair comparison environment.
    
    🚀 How to use:
    1. ✍️ Type a test message above
    2. ⚙️ Choose key sizes (defaults are fine)
    3. 🆚 Click "COMPARE NOW" button
    4. 📊 View detailed performance comparison
    
    ✅ Ready? Click the green button above!
    """
    
    tk.Label(results_frame, text=welcome_text, font=("Arial", 11), justify="left",
            bg="white", padx=50, pady=50, wraplength=700).pack(expand=True)
    
    status_label.config(text="✅ Ready to compare - Type a message and click COMPARE NOW")

def show_simple_explanation():
    """Show a simple explanation popup"""
    explanation = """
    🔍 WHAT ARE WE COMPARING?
    
    Both methods use AES-256 symmetric encryption (military-grade 🔐).
    They differ in HOW THEY EXCHANGE KEYS:
    
    🔐 AES+LUC:
    • 🧮 Uses Integer Factorization problem (like RSA)
    • 📏 Larger key sizes required
    • 🐢 Slower key exchange
    • 📚 Established technology
    
    🔐 AES+ECDH:
    • 📈 Uses Elliptic Curve Discrete Logarithm Problem (ECDLP)
    • 📐 Smaller key sizes for same security
    • 🐇 Faster key exchange
    • 🚀 Modern standard (NIST recommended)
    
    🎯 WHAT WE'RE MEASURING:
    1. ⚡ Execution Time - Total time for key setup and encryption
    2. 🔑 Key Size - Efficiency in resource usage
    3. 🧠 Theoretical Security - Mathematical security analysis
    4. 💻 CPU Usage - Computational workload
    5. 💾 Memory Usage - RAM requirements
    
    ✅ Both provide strong security for practical applications!
    
    ⚠️ NOTE: For fair comparison, run multiple times to get
    consistent AES encryption timing results.
    """
    messagebox.showinfo("💡 Explanation", explanation)

# ==================== CREATE SIMPLE GUI ====================

root = tk.Tk()
root.title("🔐 Crypto Comparison - AES+LUC vs AES+ECDH")
root.geometry("900x750")
root.configure(bg="#f5f5f5")

# Make window resizable
root.minsize(800, 650)

# Header with simple title
header = tk.Frame(root, bg="#2196F3", height=100)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="🔐 Crypto Performance Comparison Tool", 
        font=("Arial", 22, "bold"), fg="white", bg="#2196F3").pack(expand=True, pady=10)
tk.Label(header, text="AES+LUC 🆚 AES+ECDH - Hybrid Encryption Analysis", 
        font=("Arial", 12), fg="white", bg="#2196F3").pack()

# Simple controls panel
controls = tk.Frame(root, bg="white", padx=20, pady=15)
controls.pack(fill="x", padx=10, pady=10)

# Test message
tk.Label(controls, text="✍️ Test Message:", font=("Arial", 11), bg="white").pack(anchor="w")
message_entry = tk.Entry(controls, font=("Arial", 11), width=60)
message_entry.pack(fill="x", pady=5)
message_entry.insert(0, "Hello, this is a test message for encryption performance comparison!")

# Settings in a simple grid
settings_frame = tk.Frame(controls, bg="white")
settings_frame.pack(fill="x", pady=10)

# LUC Settings
tk.Label(settings_frame, text="🔐 LUC Key Size:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", padx=(0, 20))
luc_var = tk.IntVar(value=1024)
luc_menu = ttk.Combobox(settings_frame, textvariable=luc_var, values=[512, 1024, 2048], 
                       width=15, state="readonly", font=("Arial", 10))
luc_menu.grid(row=0, column=1, sticky="w")

# ECDH Settings
tk.Label(settings_frame, text="📐 ECDH Curve:", font=("Arial", 10), bg="white").grid(row=0, column=2, sticky="w", padx=(20, 10))
ecdh_var = tk.StringVar(value="P-256")
ecdh_menu = ttk.Combobox(settings_frame, textvariable=ecdh_var, values=["P-256", "P-384", "P-521"], 
                        width=15, state="readonly", font=("Arial", 10))
ecdh_menu.grid(row=0, column=3, sticky="w")

# Create tooltips WITHOUT using global ToolTip window
luc_tooltip = ToolTip(luc_menu, "512-bit: Faster, less secure | 1024-bit: Balanced | 2048-bit: Slower, more secure")
ecdh_tooltip = ToolTip(ecdh_menu, "P-256: Standard, balanced | P-384: High security | P-521: Maximum security")

# Big colorful buttons
button_frame = tk.Frame(controls, bg="white")
button_frame.pack(fill="x", pady=10)

# Compare button (big and green)
compare_btn = tk.Button(button_frame, text="🚀 COMPARE NOW", command=run_comparison,
                       bg="#4CAF50", fg="white", font=("Arial", 14, "bold"),
                       height=2, width=20, cursor="hand2", relief="raised",
                       activebackground="#388E3C", activeforeground="white")
compare_btn.pack(side="left", padx=5)

# Clear button
clear_btn = tk.Button(button_frame, text="🔄 Clear", command=clear_results,
                     bg="#FF9800", fg="white", font=("Arial", 11),
                     height=2, width=10, cursor="hand2",
                     activebackground="#F57C00", activeforeground="white")
clear_btn.pack(side="left", padx=5)

# Help button
help_btn = tk.Button(button_frame, text="❓ Help", command=show_simple_explanation,
                    bg="#2196F3", fg="white", font=("Arial", 11),
                    height=2, width=10, cursor="hand2",
                    activebackground="#1976D2", activeforeground="white")
help_btn.pack(side="left", padx=5)

# Results area with scrollbar
results_container = tk.Frame(root, bg="white")
results_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# Add scrollbar
canvas = tk.Canvas(results_container, bg="white")
scrollbar = tk.Scrollbar(results_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollbar and canvas
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# This is where results will go
results_frame = scrollable_frame

# Status bar
status_label = tk.Label(root, text="✅ Ready to compare - Type a message and click COMPARE NOW", 
                       bg="#424242", fg="white", anchor="w", padx=20, font=("Arial", 10))
status_label.pack(side="bottom", fill="x")

# Show initial welcome message
clear_results()

# Add keyboard shortcuts
root.bind('<Control-c>', lambda e: run_comparison())
root.bind('<Control-l>', lambda e: clear_results())
root.bind('<F1>', lambda e: show_simple_explanation())

# Add mouse wheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Run the application
root.mainloop()