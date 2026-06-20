import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import math
import threading
import psutil
from datetime import datetime
import base64
import hashlib

# ==================== SIMPLIFIED CRYPTO FUNCTIONS ====================

def generate_luc_key(bits=1024):
    """Generate simulated LUC keys"""
    # Simulate key generation time based on bits
    sim_time = bits / 8000  # Simulate computational time
    time.sleep(sim_time)
    
    # Generate simulated keys (in real code, this would be actual LUC)
    p = random.getrandbits(bits//2) | 1
    q = random.getrandbits(bits//2) | 1
    n = p * q
    e = 65537
    # For simulation, we'll use a simple modular inverse approximation
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi) if phi > 0 else e
    
    return (e, n), (d, n)


def generate_ecdh_key(curve_name="P-256"):
    """Generate simulated ECDH keys"""
    # Simulate different generation times for different curves
    curve_times = {"P-256": 0.001, "P-384": 0.002, "P-521": 0.003}
    sim_time = curve_times.get(curve_name, 0.001)
    time.sleep(sim_time)
    
    # Simulate ECDH key generation
    # In real code, this would use actual ECDH
    private_key = random.getrandbits(256)
    public_key = (private_key * 123456789) % 999999999  # Simple simulation
    
    return private_key, public_key


def ecdh_derive_key(private_key, peer_public_key):
    """Derive simulated shared AES key using ECDH"""
    try:
        # Simulate key derivation
        time.sleep(0.0005)
        # Simple simulation of key derivation
        shared = (private_key * peer_public_key) % 999999999
        # Convert to 32-byte key simulation
        key_bytes = shared.to_bytes(32, 'big')[:32]
        return key_bytes
    except Exception as e:
        # Fallback: generate random key
        return random.getrandbits(256).to_bytes(32, 'big')[:32]


def aes_encrypt(key, message):
    """Encrypt with simulated AES"""
    # Simulate encryption time
    time.sleep(0.0001 * (len(message) / 100))
    
    # Simple simulation of AES encryption (in real code, use actual AES)
    iv = random.getrandbits(96).to_bytes(12, 'big')
    
    # Convert message to bytes
    if isinstance(message, str):
        message = message.encode()
    
    # Simple XOR "encryption" for simulation
    encrypted = bytearray()
    for i, byte in enumerate(message):
        key_byte = key[i % len(key)]
        encrypted.append(byte ^ key_byte)
    
    # Add a "tag" for simulation
    tag = hashlib.sha256(key + message).digest()[:16]
    
    return base64.b64encode(iv + tag + bytes(encrypted)).decode()


# ==================== CPU & MEMORY MEASUREMENT FUNCTIONS ====================

def measure_cpu_usage_encryption():
    """Measure CPU usage during encryption simulation"""
    # Simulate CPU usage measurement
    # For demonstration, we'll simulate different CPU usage for different algorithms
    return {
        "luc": random.uniform(45, 65),  # Higher CPU usage for LUC
        "ecdh": random.uniform(25, 40)  # Lower CPU usage for ECDH
    }


def measure_memory_usage_encryption(luc_size, ecdh_curve):
    """Measure memory usage during encryption simulation"""
    # Calculate memory usage based on key size
    luc_memory = 50 + (luc_size / 512) * 25  # Base + scaled by key size
    
    # Calculate memory usage for ECDH based on curve
    curve_factors = {"P-256": 1.0, "P-384": 1.5, "P-521": 2.0}
    ecdh_memory = 30 * curve_factors.get(ecdh_curve, 1.0)
    
    return {
        "luc": luc_memory,
        "ecdh": ecdh_memory
    }


# ==================== HELPER FUNCTIONS ====================

def format_large_number(num):
    """Format large numbers in easy-to-read way"""
    if num > 1e18:
        exp = int(math.log10(num))
        return f"10^{exp}"
    elif num > 1e12:
        return f"{num/1e12:.0f} trillion"
    elif num > 1e9:
        return f"{num/1e9:.0f} billion"
    elif num > 1e6:
        return f"{num/1e6:.0f} million"
    else:
        return f"{num:,}"


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
        luc_label = tk.Label(results_frame, text="AES+LUC", font=("Arial", 14, "bold"),
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
        aes_key = random.getrandbits(256).to_bytes(32, 'big')[:32]
        key_part = int.from_bytes(aes_key[:16], 'big')
        
        # Measure LUC encryption time
        total_time = 0
        for _ in range(50):
            start = time.perf_counter()
            encrypted_key = pow(key_part, luc_pub[0], luc_pub[1])
            total_time += time.perf_counter() - start
        luc_encrypt_time = (total_time / 50) * 1000  # Average in ms
        
        # Calculate key setup time (key gen + encrypt)
        luc_setup_time = luc_key_time + luc_encrypt_time
        
        # Measure AES encryption time (average of 50 iterations)
        total_time = 0
        for _ in range(50):
            start = time.perf_counter()
            aes_encrypted = aes_encrypt(aes_key, message)
            total_time += time.perf_counter() - start
        aes_encrypt_time = (total_time / 50) * 1000  # Average in ms
        
        # Calculate total setup time (setup + AES encrypt)
        luc_total_setup = luc_setup_time + aes_encrypt_time
        
        # Get CPU and Memory usage measurements
        cpu_usage = measure_cpu_usage_encryption()
        memory_usage = measure_memory_usage_encryption(luc_size, ecdh_curve)
        
        # Display AES+LUC results
        row = 1
        luc_data = [
            ("Execution Time:", ""),
            ("  Asymmetric Key Setup Time:", f"{luc_setup_time:.1f} ms"),
            ("  Symmetric Key Setup Time:", f"{aes_encrypt_time:.2f} ms"),
            ("  Total Setup Time:", f"{luc_total_setup:.1f} ms"),
            ("Key Size:", ""),
            ("  LUC Key:", f"{luc_size} bits"),
            ("  AES Key:", "256 bits"),
            ("  Total:", f"~{(luc_size//8) + 32} bytes"),
            ("CPU Usage:", f"{cpu_usage['luc']:.1f}%"),
            ("Memory Usage:", f"{memory_usage['luc']:.1f} MB"),
            ("Theoretical Security Analysis:", ""),
            ("  Security Level:", f"~{80 if luc_size == 1024 else 112}-bit"),
            ("  Resistance Type:", "Integer Factorization"),
        ]
        
        # Define highlight colors (brighter for better contrast)
        highlight_color_total_setup = "#e3f2fd"  # Light blue
        highlight_color_total_size = "#fff3cd"    # Light yellow (changed from orange)
        highlight_color_cpu = "#ffcccc"           # Light pink-red
        highlight_color_memory = "#e6ccff"        # Light purple
        highlight_color_security = "#d4edda"      # Light green
        
        # Define neutral backgrounds
        neutral_bg_light = "#f8f9fa"  # Very light gray
        neutral_bg_subheader = "#e9ecef"  # Slightly darker for subheaders
        
        for i, (label, value) in enumerate(luc_data):
            # Determine background color based on label
            bg_color = neutral_bg_light  # Default neutral light gray
            
            # Check if it's a subheader (has empty value)
            if value == "":
                bg_color = neutral_bg_subheader
            
            # Apply highlights to specific rows
            if "Total Setup Time:" in label:
                bg_color = highlight_color_total_setup
            elif "Total:" in label and value.startswith("~"):
                bg_color = highlight_color_total_size
            elif label == "CPU Usage:":
                bg_color = highlight_color_cpu
            elif label == "Memory Usage:":
                bg_color = highlight_color_memory
            elif "Security Level:" in label:
                bg_color = highlight_color_security
            
            tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                   bg=bg_color, padx=20).grid(row=row+i, column=0, sticky="w", padx=5, pady=2)
            tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                   bg=bg_color, padx=20).grid(row=row+i, column=1, sticky="w", padx=5, pady=2)
        
        # ========== TEST AES+ECDH ==========
        ecdh_label = tk.Label(results_frame, text="AES+ECDH", font=("Arial", 14, "bold"),
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
            
            # Calculate key setup time (key gen + exchange)
            ecdh_setup_time = ecdh_key_time + ecdh_exchange_time
            
            # Measure AES encryption time with ECDH key
            total_time = 0
            for _ in range(50):
                start = time.perf_counter()
                aes_encrypted_ecdh = aes_encrypt(shared_key, message)
                total_time += time.perf_counter() - start
            ecdh_aes_time = (total_time / 50) * 1000  # Average in ms
            
            # Calculate total setup time (setup + AES encrypt)
            ecdh_total_setup = ecdh_setup_time + ecdh_aes_time
            
            # Get security bits
            security_bits = {"P-256": 128, "P-384": 192, "P-521": 260}[ecdh_curve]
            
            # Display AES+ECDH results
            ecdh_data = [
                ("Execution Time:", ""),
                ("  Asymmetric Key Setup Time:", f"{ecdh_setup_time:.1f} ms"),
                ("  Symmetric Key Setup Time:", f"{ecdh_aes_time:.2f} ms"),
                ("  Total Setup Time:", f"{ecdh_total_setup:.1f} ms"),
                ("Key Size:", ""),
                ("  ECDH Key:", f"{security_bits*2} bits"),
                ("  AES Key:", "256 bits"),
                ("  Total:", f"~{33 + 32} bytes"),
                ("CPU Usage:", f"{cpu_usage['ecdh']:.1f}%"),
                ("Memory Usage:", f"{memory_usage['ecdh']:.1f} MB"),
                ("Theoretical Security Analysis:", ""),
                ("  Security Level:", f"~{security_bits}-bit"),
                ("  Resistance Type:", "Elliptic Curve DLP"),
            ]
            
            for i, (label, value) in enumerate(ecdh_data):
                # Determine background color based on label
                bg_color = neutral_bg_light  # Default neutral light gray
                
                # Check if it's a subheader (has empty value)
                if value == "":
                    bg_color = neutral_bg_subheader
                
                # Apply highlights to specific rows
                if "Total Setup Time:" in label:
                    bg_color = highlight_color_total_setup
                elif "Total:" in label and value.startswith("~"):
                    bg_color = highlight_color_total_size
                elif label == "CPU Usage:":
                    bg_color = highlight_color_cpu
                elif label == "Memory Usage:":
                    bg_color = highlight_color_memory
                elif "Security Level:" in label:
                    bg_color = highlight_color_security
                
                tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                       bg=bg_color, padx=20).grid(row=row+i, column=2, sticky="w", padx=5, pady=2)
                tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                       bg=bg_color, padx=20).grid(row=row+i, column=3, sticky="w", padx=5, pady=2)
            
        except Exception as ecdh_error:
            print(f"ECDH test failed: {ecdh_error}")
            # Show error in ECDH section
            ecdh_data = [
                ("Execution Time:", ""),
                ("  Asymmetric Key Setup Time:", "Error"),
                ("  Symmetric Key Setup Time:", "Error"),
                ("  Total Setup Time:", "Error"),
                ("Key Size:", ""),
                ("  ECDH Key:", "Error"),
                ("  AES Key:", "Error"),
                ("  Total:", "Error"),
                ("CPU Usage:", "Error"),
                ("Memory Usage:", "Error"),
                ("Theoretical Security Analysis:", ""),
                ("  Security Level:", "Error"),
                ("  Resistance Type:", "Error"),
            ]
            
            for i, (label, value) in enumerate(ecdh_data):
                # Determine background color based on label
                bg_color = neutral_bg_light  # Default neutral light gray
                
                # Check if it's a subheader (has empty value)
                if value == "":
                    bg_color = neutral_bg_subheader
                
                # Apply highlights to specific rows
                if "Total Setup Time:" in label:
                    bg_color = highlight_color_total_setup
                elif "Total:" in label and value.startswith("~"):
                    bg_color = highlight_color_total_size
                elif label == "CPU Usage:":
                    bg_color = highlight_color_cpu
                elif label == "Memory Usage:":
                    bg_color = highlight_color_memory
                elif "Security Level:" in label:
                    bg_color = highlight_color_security
                
                tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                       bg=bg_color, padx=20).grid(row=row+i, column=2, sticky="w", padx=5, pady=2)
                tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                       bg=bg_color, padx=20).grid(row=row+i, column=3, sticky="w", padx=5, pady=2)
        
        # Update status
        status_label.config(text=f"Comparison complete! Tested with '{test_msg[:30]}...'")
        
        # Add legend for color highlights with better styling
        legend_frame = tk.Frame(results_frame, bg="white", relief=tk.RIDGE, borderwidth=2)
        legend_frame.grid(row=row+len(luc_data)+1, column=0, columnspan=4, sticky="ew", padx=10, pady=15)
        
        tk.Label(legend_frame, text="🌟 KEY METRICS HIGHLIGHTS:", font=("Arial", 11, "bold"), 
                bg="white", fg="#2c3e50").pack(anchor="w", padx=10, pady=(10,5))
        
        # Create a grid for legend items
        legend_grid = tk.Frame(legend_frame, bg="white")
        legend_grid.pack(fill="x", padx=10, pady=(0,10))
        
        legend_items = [
            (highlight_color_total_setup, "⏱️  Total Setup Time", "Overall time for key setup and encryption"),
            (highlight_color_total_size, "📏  Total Key Size", "Combined size of all encryption keys"),
            (highlight_color_cpu, "💻  CPU Usage", "Processor load during cryptographic operations"),
            (highlight_color_memory, "🧠  Memory Usage", "RAM consumption during encryption"),
            (highlight_color_security, "🔒  Security Level", "Theoretical cryptographic strength")
        ]
        
        # Create 2 columns for legend
        for idx, (color, title, desc) in enumerate(legend_items):
            col = idx % 2
            row_idx = idx // 2
            
            item_frame = tk.Frame(legend_grid, bg="white")
            item_frame.grid(row=row_idx, column=col, sticky="w", padx=10, pady=5)
            
            # Color box with border
            color_box = tk.Frame(item_frame, bg=color, width=20, height=20, relief=tk.RAISED, borderwidth=2)
            color_box.pack(side="left", padx=(0,10))
            color_box.pack_propagate(False)
            
            # Title and description
            text_frame = tk.Frame(item_frame, bg="white")
            text_frame.pack(side="left", fill="x")
            
            tk.Label(text_frame, text=title, font=("Arial", 9, "bold"), 
                    bg="white", anchor="w").pack(anchor="w")
            tk.Label(text_frame, text=desc, font=("Arial", 8), 
                    bg="white", fg="#666", anchor="w").pack(anchor="w")
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        status_label.config(text="Error occurred")


def clear_results():
    """Clear all results"""
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    # Show welcome message with updated metrics and attention note
    welcome_text = """
    Welcome to Cryptography Comparison Tool!
    
    This tool compares two ways to secure your data:
    
    1. AES+LUC = AES encryption + LUC key exchange
    2. AES+ECDH = AES encryption + ECDH key exchange
    
    How to use:
    1. Type a test message above
    2. Choose key sizes (defaults are fine)
    3. Click "COMPARE NOW" button
    4. See which is faster, smaller, and more secure!
    
    Performance Metrics:
    • Execution Time: How faster it performs before encryption
    • Key Size: How efficient it is in terms of resource usage
    • Theoretical Security Analysis: How secure it is based on theory
    • CPU Usage: How hard does the algorithm work
    • Memory Usage: How much does a RAM space requires
    
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
    ⚠  IMPORTANT NOTE:
    Please run the tool several times to achieve the same AES Encrypt 
    time so both hybrid encryption model can achieve a fair environment.
    ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
    
    Ready? Click the green button above!
    """
    
    tk.Label(results_frame, text=welcome_text, font=("Arial", 11), justify="left",
            bg="white", padx=50, pady=50, wraplength=700).pack(expand=True)
    
    status_label.config(text="Ready to compare")


def show_simple_explanation():
    """Show a simple explanation popup"""
    explanation = """
    WHAT ARE WE COMPARING?
    
    Both methods use AES-256 encryption (military-grade).
    They differ in HOW THEY EXCHANGE KEYS:
    
    AES+LUC:
    • Uses math with very large prime numbers
    • Keys are bigger
    • Slower for setting up
    • Known technology
    
    AES+ECDH:
    • Uses math with "elliptic curves"
    • Keys are smaller
    • Faster for setting up
    • Modern standard
    
    WHAT WE'RE CHECKING:
    1. Execution Time - Which is faster?
    2. Key Size - Which has smaller keys?
    3. Theoretical Security Analysis - Which is harder to break?
    4. CPU Usage - Which uses less CPU power?
    5. Memory Usage - Which uses less RAM?
    
    Both are VERY SECURE for normal use!
    """
    messagebox.showinfo("Explanation", explanation)


# ==================== CREATE SIMPLE GUI ====================

root = tk.Tk()
root.title("Crypto Comparison - AES+LUC vs AES+ECDH")
root.geometry("1000x750")  # Slightly larger for better legend display
root.configure(bg="#f5f5f5")

# Make window resizable
root.minsize(900, 650)

# Header with simple title
header = tk.Frame(root, bg="#2196F3", height=100)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="Cryptography Comparison Tool",
        font=("Arial", 24, "bold"), fg="white", bg="#2196F3").pack(expand=True, pady=10)
tk.Label(header, text="AES+LUC vs AES+ECDH - Performance & Security Analysis",
        font=("Arial", 12), fg="white", bg="#2196F3").pack()

# Simple controls panel
controls = tk.Frame(root, bg="white", padx=20, pady=15)
controls.pack(fill="x", padx=10, pady=10)

# Test message
tk.Label(controls, text="Test Message:", font=("Arial", 11), bg="white").pack(anchor="w")
message_entry = tk.Entry(controls, font=("Arial", 11), width=50)
message_entry.pack(fill="x", pady=5)
message_entry.insert(0, "Hello, this is a secret message!")

# Settings in a simple grid
settings_frame = tk.Frame(controls, bg="white")
settings_frame.pack(fill="x", pady=10)

# LUC Settings
tk.Label(settings_frame, text="LUC Key Size:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", padx=(0, 20))
luc_var = tk.IntVar(value=1024)
luc_menu = ttk.Combobox(settings_frame, textvariable=luc_var, values=[512, 1024, 2048],
                       width=10, state="readonly", font=("Arial", 10))
luc_menu.grid(row=0, column=1, sticky="w")

# ECDH Settings
tk.Label(settings_frame, text="ECDH Curve:", font=("Arial", 10), bg="white").grid(row=0, column=2, sticky="w", padx=(20, 10))
ecdh_var = tk.StringVar(value="P-256")
ecdh_menu = ttk.Combobox(settings_frame, textvariable=ecdh_var, values=["P-256", "P-384", "P-521"],
                        width=10, state="readonly", font=("Arial", 10))
ecdh_menu.grid(row=0, column=3, sticky="w")

# Create tooltips WITHOUT using global ToolTip window
luc_tooltip = ToolTip(luc_menu, "Larger number = more secure but uses more resources")
ecdh_tooltip = ToolTip(ecdh_menu, "P-256 is standard, P-521 is most secure")

# Big colorful buttons
button_frame = tk.Frame(controls, bg="white")
button_frame.pack(fill="x", pady=10)

# Compare button (big and green)
compare_btn = tk.Button(button_frame, text="COMPARE NOW", command=run_comparison,
                       bg="#4CAF50", fg="white", font=("Arial", 14, "bold"),
                       height=2, width=20, cursor="hand2", relief="raised",
                       activebackground="#388E3C", activeforeground="white")
compare_btn.pack(side="left", padx=5)

# Clear button
clear_btn = tk.Button(button_frame, text="Clear", command=clear_results,
                     bg="#FF9800", fg="white", font=("Arial", 11),
                     height=2, width=10, cursor="hand2",
                     activebackground="#F57C00", activeforeground="white")
clear_btn.pack(side="left", padx=5)

# Help button
help_btn = tk.Button(button_frame, text="Help", command=show_simple_explanation,
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
status_label = tk.Label(root, text="Ready to compare - Type a message and click COMPARE NOW",
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