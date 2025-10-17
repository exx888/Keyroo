# Keyroo
Keyroo v5.1: Elite Evasion &amp; Cryptography Toolkit. Advanced Python Dropper Generator with Multi-Layer AES Encryption, Anti-Analysis (VM/Sandbox) checks, and integrated MSFvenom command generation. Designed for security research and penetration testing. Securely encrypts and hides executables from analysis.
# 💎 Keyroo v5.1: Elite Evasion & Cryptography Toolkit

![Keyroo Banner](https://img.shields.io/badge/Keyroo-v5.1%20Evasion%20Toolkit-red?style=for-the-badge&logo=github)
![Python Version](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Concise Description:** Keyroo v5.1 is an **Elite Evasion & Cryptography Toolkit**. An advanced Python Dropper Generator with **Multi-Layer AES Encryption**, **Anti-Analysis (VM/Sandbox) checks**, and integrated MSFvenom command generation. Designed for security research and penetration testing. Securely encrypts and hides executables from analysis.

## ✨ Key Features

Keyroo is built to provide maximum stealth and flexibility in preparing files for testing and deployment.

| Feature | Description | Status |
| :--- | :--- | :--- |
| **Multi-Layer AES Encryption (3-Key)** | Utilizes three layers of Fernet encryption for extreme complexity in reverse engineering. | **✅ Implemented** |
| **Anti-Analysis Injector** | Injects runtime checks to detect and terminate execution in Sandboxes or Virtual Machines. | **✅ Implemented** |
| **MSF Integration Module (Safe)** | Generates `msfvenom` commands and pre-configured `msfconsole` resource files for rapid listener setup. | **✅ Implemented** |
| **Slim Dropper & Binder** | Options for simple embedding or binding multiple files into one encrypted package. | **✅ Implemented** |
| **Secure Wipe (Standalone & Post-Encryption)** | Performs secure, multi-pass overwriting of files to ensure no data recovery is possible. | **✅ Implemented** |

---

## 🚀 Getting Started

### 1. Prerequisites (Setup)

Ensure you have **Python 3.x** and the required dependencies installed.

```bash
# Install the core dependencies: cryptography, psutil, and pyinstaller
pip install pyinstaller cryptography psutil
