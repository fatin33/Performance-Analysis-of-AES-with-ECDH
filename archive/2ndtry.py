import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import math
import random
import psutil  # For CPU/Memory monitoring
from datetime import datetime
import hashlib
import base64
import os

# ==================== SIMPLE CRYPTO FUNCTIONS (No External Dependencies) ====================

class SimpleCrypto:
    """Simple cryptographic functions without external dependencies"""
    
    @staticmethod
    def simple_hash(data):
        """Simple hash function using SHA256"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def simple_encrypt(text, key):
        """Simple XOR encryption (for demonstration only)"""
        key = key.encode()
        text = text.encode()
        encrypted = bytearray()
        for i in range(len(text)):
            encrypted.append(text[i] ^ key[i % len(key)])
        return base64.b64encode(encrypted).decode()
    
    @staticmethod
    def simple_decrypt(encrypted, key):
        """Simple XOR decryption (for demonstration only)"""
        encrypted = base64.b64decode(encrypted)
        key = key.encode()
        decrypted = bytearray()
        for i in range(len(encrypted)):
            decrypted.append(encrypted[i] ^ key[i % len(key)])
        return decrypted.decode()
    
    @staticmethod
    def simulate_luc_encryption(text, bits=1024):
        """Simulate LUC encryption process"""
        # This is a simulation for demonstration
        start_time = time.time()
        # Simulate encryption time based on key size
        simulated_time = bits / 10000
        time.sleep(simulated_time)
        
        # Return simulated encrypted text
        encrypted = base64.b64encode(f"LUC-ENC:{text}".encode()).decode()
        return encrypted, (time.time() - start_time) * 1000
    
    @staticmethod
    def simulate_ecdh_encryption(text, curve="P-256"):
        """Simulate ECDH encryption process"""
        start_time = time.time()
        
        # Simulate different speeds for different curves
        curve_speeds = {"P-256": 0.001, "P-384": 0.002, "P-521": 0.003}
        simulated_time = curve_speeds.get(curve, 0.001)
        time.sleep(simulated_time)
        
        # Return simulated encrypted text
        encrypted = base64.b64encode(f"ECDH-ENC:{text}".encode()).decode()
        return encrypted, (time.time() - start_time) * 1000

# ==================== CPU & MEMORY MONITORING ====================

class SystemMonitor:
    """Monitors system CPU and memory usage"""
    
    def __init__(self):
        self.cpu_history = []
        self.memory_history = []
        self.max_history = 50
        
    def get_cpu_usage(self):
        """Get current CPU usage percentage"""
        return psutil.cpu_percent(interval=0.1)
    
    def get_memory_usage(self):
        """Get current memory usage percentage"""
        return psutil.virtual_memory().percent
    
    def get_memory_details(self):
        """Get detailed memory information"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'free': mem.free
        }
    
    def get_process_count(self):
        """Get number of running processes"""
        return len(psutil.pids())
    
    def get_system_info(self):
        """Get general system information"""
        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'platform': os.name
        }

# ==================== MAIN APPLICATION ====================

class CryptoComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Comparison with System Monitor")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize monitors
        self.crypto = SimpleCrypto()
        self.sys_monitor = SystemMonitor()
        
        # Variables
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Create GUI
        self.create_gui()
        
        # Start system monitoring
        self.start_system_monitoring()
    
    def create_gui(self):
        """Create the main GUI layout"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab1 = tk.Frame(self.notebook, bg='#f0f0f0')
        self.tab2 = tk.Frame(self.notebook, bg='#f0f0f0')
        self.tab3 = tk.Frame(self.notebook, bg='#f0f0f0')
        
        self.notebook.add(self.tab1, text='System Monitor')
        self.notebook.add(self.tab2, text='Crypto Comparison')
        self.notebook.add(self.tab3, text='Performance Analysis')
        
        # Build each tab
        self.build_system_monitor_tab()
        self.build_crypto_comparison_tab()
        self.build_performance_analysis_tab()
    
    def build_system_monitor_tab(self):
        """Build system monitoring tab"""
        # Header
        header = tk.Label(self.tab1, text="SYSTEM MONITOR", 
                         font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        header.pack(fill='x', padx=5, pady=5)
        
        # Create main container with two columns
        container = tk.Frame(self.tab1, bg='#f0f0f0')
        container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left column - CPU and Memory gauges
        left_frame = tk.Frame(container, bg='#f0f0f0')
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # CPU Gauge
        cpu_frame = tk.LabelFrame(left_frame, text="CPU USAGE", font=('Arial', 12, 'bold'),
                                 bg='white', relief=tk.RAISED, borderwidth=2)
        cpu_frame.pack(fill='both', expand=True, pady=10)
        
        self.cpu_label = tk.Label(cpu_frame, text="0%", font=('Arial', 36, 'bold'),
                                 fg='#2c3e50', bg='white')
        self.cpu_label.pack(pady=20)
        
        self.cpu_canvas = tk.Canvas(cpu_frame, width=300, height=20, bg='white', highlightthickness=0)
        self.cpu_canvas.pack(pady=10)
        self.cpu_bar = self.cpu_canvas.create_rectangle(0, 0, 0, 20, fill='#3498db')
        
        # Memory Gauge
        mem_frame = tk.LabelFrame(left_frame, text="MEMORY USAGE", font=('Arial', 12, 'bold'),
                                 bg='white', relief=tk.RAISED, borderwidth=2)
        mem_frame.pack(fill='both', expand=True, pady=10)
        
        self.mem_label = tk.Label(mem_frame, text="0%", font=('Arial', 36, 'bold'),
                                 fg='#2c3e50', bg='white')
        self.mem_label.pack(pady=20)
        
        self.mem_canvas = tk.Canvas(mem_frame, width=300, height=20, bg='white', highlightthickness=0)
        self.mem_canvas.pack(pady=10)
        self.mem_bar = self.mem_canvas.create_rectangle(0, 0, 0, 20, fill='#e74c3c')
        
        # Right column - System Information
        right_frame = tk.Frame(container, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True, padx=10)
        
        info_frame = tk.LabelFrame(right_frame, text="SYSTEM INFORMATION", 
                                  font=('Arial', 12, 'bold'), bg='white',
                                  relief=tk.RAISED, borderwidth=2)
        info_frame.pack(fill='both', expand=True)
        
        # System info labels
        info_text = tk.Text(info_frame, height=15, width=40, font=('Arial', 10),
                           bg='white', relief=tk.FLAT)
        info_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.info_text_widget = info_text
        
        # Update system info
        self.update_system_info()
    
    def build_crypto_comparison_tab(self):
        """Build cryptography comparison tab"""
        # Header
        header = tk.Label(self.tab2, text="CRYPTOGRAPHY COMPARISON", 
                         font=('Arial', 18, 'bold'), bg='#34495e', fg='white')
        header.pack(fill='x', padx=5, pady=5)
        
        # Input frame
        input_frame = tk.Frame(self.tab2, bg='#f0f0f0')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(input_frame, text="Enter text to encrypt:", 
                font=('Arial', 11, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.text_input = tk.Text(input_frame, height=4, width=60, font=('Arial', 10))
        self.text_input.pack(fill='x', pady=5)
        self.text_input.insert('1.0', 'Sample text for encryption comparison')
        
        # Settings frame
        settings_frame = tk.Frame(self.tab2, bg='#f0f0f0')
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        # LUC settings
        luc_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        luc_frame.pack(side='left', padx=20)
        
        tk.Label(luc_frame, text="LUC Settings:", 
                font=('Arial', 11, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.luc_var = tk.StringVar(value="1024")
        ttk.Combobox(luc_frame, textvariable=self.luc_var, 
                    values=["512", "1024", "2048", "4096"], width=15).pack(pady=5)
        
        # ECDH settings
        ecdh_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        ecdh_frame.pack(side='left', padx=20)
        
        tk.Label(ecdh_frame, text="ECDH Curve:", 
                font=('Arial', 11, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.ecdh_var = tk.StringVar(value="P-256")
        ttk.Combobox(ecdh_frame, textvariable=self.ecdh_var, 
                    values=["P-256", "P-384", "P-521"], width=15).pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.tab2, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        compare_btn = tk.Button(button_frame, text="RUN COMPARISON", 
                               command=self.run_comparison,
                               font=('Arial', 12, 'bold'),
                               bg='#27ae60', fg='white',
                               padx=20, pady=10, cursor='hand2')
        compare_btn.pack()
        
        # Results frame
        results_frame = tk.Frame(self.tab2, bg='#f0f0f0')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create two columns for results
        self.luc_results_frame = tk.LabelFrame(results_frame, text="AES + LUC Results",
                                              font=('Arial', 11, 'bold'),
                                              bg='white', relief=tk.RAISED)
        self.luc_results_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.ecdh_results_frame = tk.LabelFrame(results_frame, text="AES + ECDH Results",
                                               font=('Arial', 11, 'bold'),
                                               bg='white', relief=tk.RAISED)
        self.ecdh_results_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Initialize empty results
        self.clear_results()
    
    def build_performance_analysis_tab(self):
        """Build performance analysis tab"""
        # Header
        header = tk.Label(self.tab3, text="PERFORMANCE ANALYSIS", 
                         font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        header.pack(fill='x', padx=5, pady=5)
        
        # Analysis frame
        analysis_frame = tk.Frame(self.tab3, bg='#f0f0f0')
        analysis_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Performance metrics
        metrics = [
            ("Encryption Speed", "Measure how fast each algorithm encrypts data"),
            ("Key Generation", "Time taken to generate encryption keys"),
            ("Memory Usage", "RAM consumed during encryption process"),
            ("CPU Usage", "Processor load during cryptographic operations"),
            ("Security Level", "Theoretical security strength in bits"),
            ("Key Size", "Size of encryption keys in bits")
        ]
        
        for i, (metric, desc) in enumerate(metrics):
            metric_frame = tk.Frame(analysis_frame, bg='white', relief=tk.RAISED, borderwidth=1)
            metric_frame.pack(fill='x', pady=5)
            
            tk.Label(metric_frame, text=metric, font=('Arial', 11, 'bold'),
                    bg='white').pack(anchor='w', padx=10, pady=5)
            tk.Label(metric_frame, text=desc, font=('Arial', 9),
                    bg='white', fg='#666').pack(anchor='w', padx=10, pady=(0,5))
        
        # Analysis button
        analyze_btn = tk.Button(analysis_frame, text="ANALYZE PERFORMANCE",
                               command=self.analyze_performance,
                               font=('Arial', 11, 'bold'),
                               bg='#3498db', fg='white',
                               padx=15, pady=8, cursor='hand2')
        analyze_btn.pack(pady=20)
    
    def start_system_monitoring(self):
        """Start the system monitoring thread"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self.update_monitor, daemon=True)
        self.monitoring_thread.start()
    
    def update_monitor(self):
        """Update system monitor displays"""
        while self.monitoring_active:
            try:
                # Get system metrics
                cpu_usage = self.sys_monitor.get_cpu_usage()
                mem_usage = self.sys_monitor.get_memory_usage()
                
                # Update CPU display
                self.cpu_label.config(text=f"{cpu_usage:.1f}%")
                self.cpu_canvas.coords(self.cpu_bar, 0, 0, cpu_usage * 3, 20)
                self.cpu_canvas.itemconfig(self.cpu_bar, 
                                          fill='#2ecc71' if cpu_usage < 50 
                                          else '#f39c12' if cpu_usage < 80 
                                          else '#e74c3c')
                
                # Update memory display
                self.mem_label.config(text=f"{mem_usage:.1f}%")
                self.mem_canvas.coords(self.mem_bar, 0, 0, mem_usage * 3, 20)
                self.mem_canvas.itemconfig(self.mem_bar,
                                          fill='#2ecc71' if mem_usage < 50
                                          else '#f39c12' if mem_usage < 80
                                          else '#e74c3c')
                
                time.sleep(1)
            except:
                break
    
    def update_system_info(self):
        """Update system information display"""
        try:
            sys_info = self.sys_monitor.get_system_info()
            mem_info = self.sys_monitor.get_memory_details()
            
            info_text = f"""System Platform: {sys_info['platform'].upper()}
CPU Cores: {sys_info['cpu_count']}
CPU Frequency: {sys_info['cpu_freq']} MHz
System Boot Time: {sys_info['boot_time']}

Memory Information:
  Total: {mem_info['total'] // (1024**3)} GB
  Available: {mem_info['available'] // (1024**3)} GB
  Used: {mem_info['used'] // (1024**3)} GB
  Free: {mem_info['free'] // (1024**3)} GB

Running Processes: {self.sys_monitor.get_process_count()}
"""
            
            self.info_text_widget.delete('1.0', tk.END)
            self.info_text_widget.insert('1.0', info_text)
        except:
            pass
        
        # Update every 5 seconds
        self.root.after(5000, self.update_system_info)
    
    def run_comparison(self):
        """Run cryptography comparison"""
        # Get input text
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to encrypt!")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Get settings
        luc_bits = int(self.luc_var.get())
        ecdh_curve = self.ecdh_var.get()
        
        try:
            # Run LUC simulation
            luc_encrypted, luc_time = self.crypto.simulate_luc_encryption(text, luc_bits)
            luc_hash = self.crypto.simple_hash(text)
            
            # Run ECDH simulation
            ecdh_encrypted, ecdh_time = self.crypto.simulate_ecdh_encryption(text, ecdh_curve)
            ecdh_hash = self.crypto.simple_hash(text)
            
            # Display LUC results
            self.display_luc_results(text, luc_encrypted, luc_hash, luc_time, luc_bits)
            
            # Display ECDH results
            self.display_ecdh_results(text, ecdh_encrypted, ecdh_hash, ecdh_time, ecdh_curve)
            
            # Show comparison summary
            self.show_comparison_summary(luc_time, ecdh_time, luc_bits, ecdh_curve)
            
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed: {str(e)}")
    
    def display_luc_results(self, original, encrypted, hash_value, time_ms, bits):
        """Display LUC encryption results"""
        # Clear frame
        for widget in self.luc_results_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable text area
        text_frame = tk.Frame(self.luc_results_frame, bg='white')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Original text
        tk.Label(text_frame, text="Original Text:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w')
        original_text = tk.Text(text_frame, height=3, width=40, font=('Arial', 9))
        original_text.pack(fill='x', pady=5)
        original_text.insert('1.0', original[:200] + ('...' if len(original) > 200 else ''))
        original_text.config(state='disabled')
        
        # Encrypted text
        tk.Label(text_frame, text="Encrypted Text:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w', pady=(10,0))
        encrypted_text = tk.Text(text_frame, height=3, width=40, font=('Arial', 9))
        encrypted_text.pack(fill='x', pady=5)
        encrypted_text.insert('1.0', encrypted[:100] + '...')
        encrypted_text.config(state='disabled')
        
        # Hash value
        tk.Label(text_frame, text="Hash:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w', pady=(10,0))
        hash_label = tk.Label(text_frame, text=hash_value[:40] + '...', 
                             font=('Courier', 8), bg='#f8f8f8', anchor='w',
                             relief=tk.SUNKEN, borderwidth=1)
        hash_label.pack(fill='x', pady=5)
        
        # Performance metrics
        metrics_frame = tk.Frame(text_frame, bg='white')
        metrics_frame.pack(fill='x', pady=10)
        
        metrics = [
            ("Encryption Time:", f"{time_ms:.2f} ms"),
            ("Key Size:", f"{bits} bits"),
            ("Security Level:", f"~{int(math.log2(bits))} bits"),
            ("Algorithm:", "LUC + AES Simulation")
        ]
        
        for label, value in metrics:
            frame = tk.Frame(metrics_frame, bg='white')
            frame.pack(fill='x', pady=2)
            tk.Label(frame, text=label, font=('Arial', 9, 'bold'),
                    bg='white', width=15, anchor='w').pack(side='left')
            tk.Label(frame, text=value, font=('Arial', 9),
                    bg='white', anchor='w').pack(side='left')
    
    def display_ecdh_results(self, original, encrypted, hash_value, time_ms, curve):
        """Display ECDH encryption results"""
        # Clear frame
        for widget in self.ecdh_results_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable text area
        text_frame = tk.Frame(self.ecdh_results_frame, bg='white')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Original text
        tk.Label(text_frame, text="Original Text:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w')
        original_text = tk.Text(text_frame, height=3, width=40, font=('Arial', 9))
        original_text.pack(fill='x', pady=5)
        original_text.insert('1.0', original[:200] + ('...' if len(original) > 200 else ''))
        original_text.config(state='disabled')
        
        # Encrypted text
        tk.Label(text_frame, text="Encrypted Text:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w', pady=(10,0))
        encrypted_text = tk.Text(text_frame, height=3, width=40, font=('Arial', 9))
        encrypted_text.pack(fill='x', pady=5)
        encrypted_text.insert('1.0', encrypted[:100] + '...')
        encrypted_text.config(state='disabled')
        
        # Hash value
        tk.Label(text_frame, text="Hash:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w', pady=(10,0))
        hash_label = tk.Label(text_frame, text=hash_value[:40] + '...', 
                             font=('Courier', 8), bg='#f8f8f8', anchor='w',
                             relief=tk.SUNKEN, borderwidth=1)
        hash_label.pack(fill='x', pady=5)
        
        # Performance metrics
        metrics_frame = tk.Frame(text_frame, bg='white')
        metrics_frame.pack(fill='x', pady=10)
        
        curve_bits = {"P-256": 256, "P-384": 384, "P-521": 521}
        
        metrics = [
            ("Encryption Time:", f"{time_ms:.2f} ms"),
            ("Curve:", curve),
            ("Security Level:", f"~{curve_bits.get(curve, 256)//2} bits"),
            ("Algorithm:", "ECDH + AES Simulation")
        ]
        
        for label, value in metrics:
            frame = tk.Frame(metrics_frame, bg='white')
            frame.pack(fill='x', pady=2)
            tk.Label(frame, text=label, font=('Arial', 9, 'bold'),
                    bg='white', width=15, anchor='w').pack(side='left')
            tk.Label(frame, text=value, font=('Arial', 9),
                    bg='white', anchor='w').pack(side='left')
    
    def clear_results(self):
        """Clear comparison results"""
        # Clear LUC results
        for widget in self.luc_results_frame.winfo_children():
            widget.destroy()
        
        # Clear ECDH results
        for widget in self.ecdh_results_frame.winfo_children():
            widget.destroy()
        
        # Add placeholders
        placeholder = tk.Label(self.luc_results_frame, 
                              text="LUC results will appear here\n\nClick 'RUN COMPARISON'",
                              font=('Arial', 11), bg='white', fg='#666')
        placeholder.pack(expand=True)
        
        placeholder2 = tk.Label(self.ecdh_results_frame, 
                               text="ECDH results will appear here\n\nClick 'RUN COMPARISON'",
                               font=('Arial', 11), bg='white', fg='#666')
        placeholder2.pack(expand=True)
    
    def show_comparison_summary(self, luc_time, ecdh_time, luc_bits, ecdh_curve):
        """Show comparison summary in message box"""
        faster = "LUC" if luc_time < ecdh_time else "ECDH"
        time_diff = abs(luc_time - ecdh_time)
        
        summary = f"""COMPARISON SUMMARY:
        
Encryption Performance:
  AES + LUC ({luc_bits} bits): {luc_time:.2f} ms
  AES + ECDH ({ecdh_curve}): {ecdh_time:.2f} ms
  
Result: {faster} is {time_diff:.2f} ms faster

Recommendation:
  • Use AES+ECDH for modern applications
  • Use AES+LUC for compatibility with older systems
  • Both provide adequate security for most use cases
  
Note: This is a simulation. Actual performance may vary."""
        
        messagebox.showinfo("Comparison Complete", summary)
    
    def analyze_performance(self):
        """Analyze performance metrics"""
        # Get current system stats
        cpu_usage = self.sys_monitor.get_cpu_usage()
        mem_usage = self.sys_monitor.get_memory_usage()
        mem_details = self.sys_monitor.get_memory_details()
        
        analysis = f"""PERFORMANCE ANALYSIS:

Current System Status:
  CPU Usage: {cpu_usage:.1f}%
  Memory Usage: {mem_usage:.1f}%
  Available RAM: {mem_details['available'] // (1024**2)} MB
  Process Count: {self.sys_monitor.get_process_count()}

Cryptography Performance Notes:

AES + LUC:
  • Suitable for resource-constrained environments
  • Larger key sizes increase security but reduce speed
  • Good for batch processing where setup time is less critical

AES + ECDH:
  • Better for real-time applications
  • Smaller keys for same security level
  • Lower computational overhead
  • Modern standard for secure communications

Recommendations:
  • For high CPU usage (>80%), consider simpler algorithms
  • Ensure sufficient memory for cryptographic operations
  • Monitor system resources during intensive operations
"""
        
        messagebox.showinfo("Performance Analysis", analysis)
    
    def on_closing(self):
        """Handle application closing"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
        self.root.destroy()

# ==================== MAIN EXECUTION ====================

def main():
    # Check for required packages
    try:
        import psutil
    except ImportError:
        print("Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    
    # Create and run application
    root = tk.Tk()
    app = CryptoComparisonApp(root)
    
    # Set window icon and position
    root.iconbitmap(default='')  # Add icon path if available
    root.update()
    root.minsize(800, 600)
    
    # Center window
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()