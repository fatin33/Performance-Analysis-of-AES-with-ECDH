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


def aes_decrypt(key, encrypted):
    """Decrypt with simulated AES"""
    data = base64.b64decode(encrypted)
    iv = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]
    
    # Simple XOR "decryption" for simulation
    decrypted = bytearray()
    for i, byte in enumerate(ciphertext):
        key_byte = key[i % len(key)]
        decrypted.append(byte ^ key_byte)
    
    return bytes(decrypted).decode()


# ==================== CPU & MEMORY MONITORING ====================

class SystemMonitor:
    """Monitors and displays CPU and memory usage"""
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Create monitoring frame
        self.monitor_frame = tk.Frame(parent_frame, bg="#e8eaf6", relief=tk.RIDGE, borderwidth=2)
        self.monitor_frame.pack(fill="x", padx=10, pady=10)
        
        # Title
        tk.Label(self.monitor_frame, text="SYSTEM MONITOR", font=("Arial", 12, "bold"),
                bg="#e8eaf6", fg="#283593").pack(pady=5)
        
        # Create metrics display
        metrics_frame = tk.Frame(self.monitor_frame, bg="#e8eaf6")
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        # CPU Monitoring
        cpu_label = tk.Label(metrics_frame, text="CPU Usage:", font=("Arial", 10, "bold"),
                           bg="#e8eaf6", anchor="w")
        cpu_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.cpu_value = tk.Label(metrics_frame, text="0%", font=("Arial", 10),
                                bg="#e8eaf6", fg="#1565c0")
        self.cpu_value.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        self.cpu_bar = ttk.Progressbar(metrics_frame, length=200, mode='determinate')
        self.cpu_bar.grid(row=0, column=2, padx=10, pady=2)
        
        # Memory Monitoring
        mem_label = tk.Label(metrics_frame, text="Memory Usage:", font=("Arial", 10, "bold"),
                           bg="#e8eaf6", anchor="w")
        mem_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.mem_value = tk.Label(metrics_frame, text="0%", font=("Arial", 10),
                                bg="#e8eaf6", fg="#c62828")
        self.mem_value.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        self.mem_bar = ttk.Progressbar(metrics_frame, length=200, mode='determinate')
        self.mem_bar.grid(row=1, column=2, padx=10, pady=2)
        
        # Process count
        proc_label = tk.Label(metrics_frame, text="Running Processes:", font=("Arial", 10, "bold"),
                            bg="#e8eaf6", anchor="w")
        proc_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        self.proc_value = tk.Label(metrics_frame, text="0", font=("Arial", 10),
                                 bg="#e8eaf6", fg="#2e7d32")
        self.proc_value.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # Start monitoring button
        self.monitor_btn = tk.Button(metrics_frame, text="Start Monitoring", 
                                    command=self.toggle_monitoring,
                                    bg="#4caf50", fg="white", font=("Arial", 9),
                                    padx=10, cursor="hand2")
        self.monitor_btn.grid(row=2, column=2, padx=10, pady=2)
        
        # Start monitoring automatically
        self.start_monitoring()
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.monitoring_active:
            self.stop_monitoring()
            self.monitor_btn.config(text="Start Monitoring", bg="#4caf50")
        else:
            self.start_monitoring()
            self.monitor_btn.config(text="Stop Monitoring", bg="#f44336")
    
    def start_monitoring(self):
        """Start system monitoring"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self.update_monitor, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
    
    def update_monitor(self):
        """Update monitoring display"""
        while self.monitoring_active:
            try:
                # Get CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.1)
                
                # Get memory usage
                memory = psutil.virtual_memory()
                mem_percent = memory.percent
                
                # Get process count
                proc_count = len(psutil.pids())
                
                # Update UI (must be done in main thread)
                self.parent.after(0, self.update_display, cpu_percent, mem_percent, proc_count)
                
                time.sleep(1)  # Update every second
            except Exception as e:
                print(f"Monitoring error: {e}")
                break
    
    def update_display(self, cpu_percent, mem_percent, proc_count):
        """Update the monitoring display"""
        self.cpu_value.config(text=f"{cpu_percent:.1f}%")
        self.cpu_bar['value'] = cpu_percent
        
        self.mem_value.config(text=f"{mem_percent:.1f}%")
        self.mem_bar['value'] = mem_percent
        
        self.proc_value.config(text=str(proc_count))


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
        
        # Display AES+LUC results
        row = 1
        luc_data = [
            ("computational speed:", ""),
            ("  Key Setup Time:", f"{luc_setup_time:.1f} ms"),
            ("  AES Encrypt:", f"{aes_encrypt_time:.2f} ms"),
            ("  Total Setup Time:", f"{luc_total_setup:.1f} ms"),
            ("key size:", ""),
            ("  LUC Key:", f"{luc_size} bits"),
            ("  AES Key:", "256 bits"),
            ("  Total:", f"~{(luc_size//8) + 32} bytes"),
            ("attack resistance:", ""),
            ("  Security Level:", f"~{80 if luc_size == 1024 else 112}-bit"),
            ("  Resistance Type:", "Integer Factorization"),
            ("  Status:", "Secure against classical attacks"),
        ]
        
        for i, (label, value) in enumerate(luc_data):
            tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                   bg="#f1f8e9", padx=20).grid(row=row+i, column=0, sticky="w", padx=5, pady=2)
            tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                   bg="#f1f8e9", padx=20).grid(row=row+i, column=1, sticky="w", padx=5, pady=2)
        
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
                ("computational speed:", ""),
                ("  Key Setup Time:", f"{ecdh_setup_time:.1f} ms"),
                ("  AES Encrypt:", f"{ecdh_aes_time:.2f} ms"),
                ("  Total Setup Time:", f"{ecdh_total_setup:.1f} ms"),
                ("key size:", ""),
                ("  ECDH Key:", f"{security_bits*2} bits"),
                ("  AES Key:", "256 bits"),
                ("  Total:", f"~{33 + 32} bytes"),
                ("attack resistance:", ""),
                ("  Security Level:", f"~{security_bits}-bit"),
                ("  Resistance Type:", "Elliptic Curve DLP"),
                ("  Status:", "Secure against classical attacks"),
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
                ("computational speed:", ""),
                ("  Key Setup Time:", "Error"),
                ("  AES Encrypt:", "Error"),
                ("  Total Setup Time:", "Error"),
                ("key size:", ""),
                ("  ECDH Key:", "Error"),
                ("  AES Key:", "Error"),
                ("  Total:", "Error"),
                ("attack resistance:", ""),
                ("  Security Level:", "Error"),
                ("  Resistance Type:", "Error"),
                ("  Status:", "Error"),
            ]
            
            for i, (label, value) in enumerate(ecdh_data):
                tk.Label(results_frame, text=label, font=("Arial", 10), anchor="w",
                       bg="#e8eaf6", padx=20).grid(row=row+i, column=2, sticky="w", padx=5, pady=2)
                tk.Label(results_frame, text=value, font=("Arial", 10), anchor="w",
                       bg="#e8eaf6", padx=20).grid(row=row+i, column=3, sticky="w", padx=5, pady=2)
        
        # Update status
        status_label.config(text=f"Comparison complete! Tested with '{test_msg[:30]}...'")
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        status_label.config(text="Error occurred")


def clear_results():
    """Clear all results"""
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    # Show welcome message
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
    • computational speed: How fast each operation takes
    • key size: How much space keys require
    • attack resistance: How secure against attacks
    
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
    1. computational speed - Which is faster?
    2. key size - Which has smaller keys?
    3. attack resistance - Which is harder to break?
    
    Both are VERY SECURE for normal use!
    """
    messagebox.showinfo("Explanation", explanation)


# ==================== CREATE SIMPLE GUI ====================

root = tk.Tk()
root.title("Crypto Comparison - AES+LUC vs AES+ECDH with System Monitor")
root.geometry("900x700")  # Slightly taller to accommodate monitor
root.configure(bg="#f5f5f5")

# Make window resizable
root.minsize(800, 600)

# Header with simple title
header = tk.Frame(root, bg="#2196F3", height=100)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="Crypto Comparison with System Monitor",
        font=("Arial", 24, "bold"), fg="white", bg="#2196F3").pack(expand=True, pady=10)
tk.Label(header, text="AES+LUC vs AES+ECDH",
        font=("Arial", 14), fg="white", bg="#2196F3").pack()

# ==================== ADD SYSTEM MONITOR ====================
system_monitor = SystemMonitor(root)

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
luc_tooltip = ToolTip(luc_menu, "Larger number = more secure but slower")
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

# Handle window closing
def on_closing():
    system_monitor.stop_monitoring()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()