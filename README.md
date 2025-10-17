# 💎 Keyroo v5.1: Elite Evasion & Cryptography Toolkit

![Keyroo Banner](https://img.shields.io/badge/Keyroo-v5.1%20Evasion%20Toolkit-red?style=for-the-badge&logo=github)
![Python Version](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Concise Description:** Keyroo v5.1 is an **Elite Evasion & Cryptography Toolkit**. An advanced Python Dropper Generator with **Multi-Layer AES Encryption**, **Anti-Analysis (VM/Sandbox) checks**, and integrated MSFvenom command generation. Designed for security research and penetration testing. Securely encrypts and hides executables from analysis.

---

## ✨ Full Feature Set

Keyroo is built to provide maximum stealth and flexibility in preparing files for testing and deployment, covering both fully **Implemented** core features and **Advanced Placeholder** concepts.

### 1. Fully Implemented Features (Working Code)

| Menu Option | Feature Name | Description |
| :---: | :--- | :--- |
| **11** | **Multi-Layer AES Encryption (3-Key)** | Utilizes three sequential layers of Fernet encryption (`K2 -> K1 -> K2`) to create a complex decryption stack, significantly hindering static analysis. |
| **13** | **Anti-Analysis Injector** | Injects runtime checks into the loader that analyze the execution environment (e.g., CPU cores, RAM size, suspicious usernames) and terminate silently if a VM or Sandbox is detected. |
| **21** | **MSF Integration Module (Safe)** | A utility for generating the required `msfvenom` payload creation command and a pre-configured `msfconsole` resource file (`.rc`) for fast listener setup. |
| **8** | **Encrypt & Embed (Slim Dropper)** | Encrypts a single file and embeds it into a minimalistic loader (Stub), optimizing for low memory consumption during execution. |
| **9** | **File Binder (Merge & Encrypt)** | Merges two files (e.g., a legitimate PDF and a hidden executable) into one encrypted package. |
| **4** | **Secure Wipe** | Performs secure, multi-pass overwriting of files (using random data) to ensure irreversible deletion of sensitive source files. |
| **7** | **File Padding** | Adds random garbage data to the end of a file to artificially increase its size, bypassing size-based filters. |

### 2. Advanced Evasion Concepts (Placeholders)

These options are included in the menu but currently contain **simulated logic** (`simulated_advanced_option`) that requires massive, specialized external libraries or complex OS-level manipulation to be fully functional.

| Menu Option | Feature Name | Concept |
| :---: | :--- | :--- |
| **10** | **Digital Signature Spoofer** | Simulates attaching a fake digital signature to the executable to appear legitimate. |
| **12** | **Time-Sensitive Loader** | Simulates code that executes only after a certain date/time or after a long delay, evading automated analysis systems. |
| **14** | **Chunked Polymorphic Encryption** | Simulates encrypting the file data in small, different chunks using multiple keys and algorithms to complicate decryption efforts. |
| **15** | **Appender Spoofer** | Simulates methods to append data to a known file type (e.g., JPEG/PDF) while maintaining the original file's validity. |
| **16** | **Anti-Emulation Key Gen** | Simulates generating decryption keys based on unique, hard-to-emulate system hardware identifiers. |
| **17** | **Staged Execution Dropper** | Simulates a tiny initial loader that downloads and decrypts the main payload in multiple stages. |
| **18** | **Encrypted Data Compression** | Simulates compressing the encrypted payload data before embedding it, reducing the final loader size. |

---

## 🚀 Getting Started

### 1. Download the Tool

Use `git clone` to download the entire repository to your local machine:

```bash
# Clone the repository (Replace [YOUR_USERNAME] with your actual GitHub username)
git clone https://github.com/exx888/Keyroo.git

# Navigate into the tool directory
cd Keyroo

#run
python Keyroo.py
