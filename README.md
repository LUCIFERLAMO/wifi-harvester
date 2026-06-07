<div align="center">

# 🛜 WiFi Harvester

> A Python-based offensive security tool that extracts saved WiFi passwords from a Windows machine and exfiltrates them via Gmail SMTP.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)
![Category](https://img.shields.io/badge/Category-Offensive%20Security-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational-yellow?style=for-the-badge)

</div>

---

## 📌 About

WiFi Harvester is a Python tool built as part of a **Python for Cybersecurity** learning path.  
It uses Windows native `netsh` commands via subprocess to extract saved WiFi credentials and delivers them to a specified email address over Gmail SMTP — with proper UTF-8 encoding and a clean Rich terminal UI.

---

## ✨ Features

- 🔍 Extracts all saved WiFi profiles from Windows
- 🔑 Retrieves password for a **single profile** or **all profiles at once**
- 📧 Sends results via **Gmail SMTP** with UTF-8 safe encoding
- ✅ **Regex-based** email validation for sender and receiver
- 🎨 Clean terminal UI powered by **Rich**
- 🔒 App password input is **hidden while typing**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `subprocess` | Run Windows `netsh` shell commands |
| `re` | Regex for email validation and password extraction |
| `smtplib` | Send emails over Gmail SMTP |
| `email.mime.text` | UTF-8 safe email formatting |
| `rich` | Beautiful terminal output |

---

## ⚙️ Setup

**1. Clone the repo**
```bash
git clone https://github.com/LUCIFERLAMO/wifi-harvester.git
cd wifi-harvester
```

**2. Install Rich**
```bash
pip install rich
```

**3. Generate a Gmail App Password**
- Go to [myaccount.google.com](https://myaccount.google.com)
- Security → 2-Step Verification → App Passwords
- Generate one and keep it ready

---

## 🚀 Usage

```bash
python windows_gmail.py
```

You will be prompted to:
1. Enter **sender** email address
2. Enter **receiver** email address  
3. Enter your **Gmail App Password** (hidden input)
4. Choose — scan a **single profile** or **all profiles**

---

## 📸 Preview
