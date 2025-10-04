import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog
import shutil

BANNER = r'''
     █████╗ ███╗   ██╗████████╗██╗    ██████╗ ██╗   ██╗ ██████╗ 
    ██╔══██╗████╗  ██║╚══██╔══╝██║    ██╔══██╗╚██╗ ██╔╝██╔═══██╗
    ███████║██╔██╗ ██║   ██║   ██║    ██████╔╝ ╚████╔╝ ██║   ██║
    ██╔══██║██║╚██╗██║   ██║   ██║    ██╔═══╝   ╚██╔╝  ██║   ██║
    ██║  ██║██║ ╚████║   ██║   ██║    ██║        ██║   ╚██████╔╝
    ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝    ╚═╝        ╚═╝    ╚═════╝ 
               Version 1.1 - Anti.exe by slayer
'''

def print_colored(msg, color='default'):
    colors = {
        "blue": "\033[94m",
        "green": "\033[92m",
        "cyan": "\033[96m",
        "red": "\033[91m",
        "default": "\033[0m"
    }
    print(f"{colors.get(color, colors['default'])}{msg}\033[0m")

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a Python-compiled .exe",
        filetypes=[("Executable files", "*.exe")]
    )
    return file_path

def extract_exe(exe_path):
    print_colored(f"[+] Extracting: {exe_path}", "cyan")
    time.sleep(0.4)
    subprocess.call(['python', 'pyinstxtractor.py', exe_path])
    extracted_dir = exe_path + "_extracted"
    return extracted_dir

def find_main_pyc(folder):
    best_guess = None
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower() == "main.pyc":
                return os.path.join(root, file)
            elif file.endswith(".pyc") and not best_guess:
                best_guess = os.path.join(root, file)
    return best_guess

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    print_colored("[?] Click to select a Python-compiled .exe file...", "blue")
    
    exe_path = select_file()
    if not exe_path or not exe_path.endswith(".exe"):
        print_colored("[!] No file selected or invalid file. Exiting.", "red")
        return

    folder = extract_exe(exe_path)

    print_colored("[+] Looking for main.pyc...", "cyan")
    main_pyc_path = find_main_pyc(folder)

    if main_pyc_path:
        shutil.copy(main_pyc_path, "main.pyc")
        print_colored(f"[✓] Found and copied: {main_pyc_path} → main.pyc", "green")
    else:
        print_colored("[!] Could not find main.pyc or any .pyc file.", "red")

if __name__ == "__main__":
    main()
