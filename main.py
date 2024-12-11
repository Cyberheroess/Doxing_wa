import os
import subprocess
import sys
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from flask import Flask, request, jsonify

def install_modules_safely():
    modules = ["requests", "flask", "selenium"]
    print("[*] Memulai proses instalasi modul...")

    for module in modules:
        installed = False
        methods = [
            f"pip install {module}",
            f"python -m pip install {module}",
            f"py -m pip install {module}",
            f"pip3 install {module}",
            f"python3 -m pip install {module}",
        ]
        for method in methods:
            try:
                print(f"[*] Mencoba: {method}")
                result = subprocess.run(
                    method, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if result.returncode == 0:
                    print(f"[+] Modul '{module}' berhasil diinstal.")
                    installed = True
                    break
                else:
                    print(f"[-] Gagal dengan perintah: {method}")
            except Exception as e:
                print(f"[-] Error saat menjalankan: {method}, {str(e)}")

        if not installed:
            print(f"[!] Modul '{module}' gagal diinstal setelah mencoba semua metode.")
        else:
            continue

    print("[*] Instalasi selesai. Memastikan semua modul diimpor...")
    try:
        for module in modules:
            __import__(module)
        print("[+] Semua modul berhasil diimpor tanpa error.")
    except ImportError as e:
        print(f"[-] Modul tidak ditemukan meskipun sudah diinstal: {str(e)}")

def selenium_get_credentials_and_ip():
    print("[*] Menjalankan bot Selenium untuk otomatisasi...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service("chromedriver")  # Pastikan chromedriver ada di direktori yang sama
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Masuk ke Twilio untuk mengambil SID dan Auth Token
        print("[*] Membuka halaman login Twilio...")
        driver.get("https://www.twilio.com/login")
        sleep(5)

        # Isi kredensial (gantikan dengan kredensial Anda)
        email = "YOUR_TWILIO_EMAIL"  # Ganti dengan email Twilio Anda
        password = "YOUR_TWILIO_PASSWORD"  # Ganti dengan password Twilio Anda

        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "password").send_keys("\n")
        sleep(5)

        driver.get("https://console.twilio.com/")
        sleep(5)
        sid = driver.find_element(By.XPATH, "//span[text()='Account SID']").text
        auth_token = driver.find_element(By.XPATH, "//span[text()='Auth Token']").text
        print(f"[+] SID: {sid}")
        print(f"[+] Auth Token: {auth_token}")

        # Dapatkan IP Publik
        driver.get("https://ifconfig.me/")
        public_ip = driver.find_element(By.TAG_NAME, "body").text.strip()
        print(f"[+] IP Publik: {public_ip}")

        return sid, auth_token, public_ip
    except Exception as e:
        print(f"[-] Error pada Selenium: {str(e)}")
    finally:
        driver.quit()

def start_tracking_server():
    app = Flask(__name__)

    @app.route("/track", methods=["GET"])
    def track():
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent")
        print(f"[+] IP: {ip}, User-Agent: {user_agent}")
        return jsonify({"status": "success", "ip": ip, "user_agent": user_agent})

    print("[*] Server berjalan di http://0.0.0.0:5000/track")
    app.run(host="0.0.0.0", port=5000)

def send_tracking_link(sid, auth_token, public_ip, target_number):
    try:
        from twilio.rest import Client
        client = Client(sid, auth_token)
        tracking_link = f"http://{public_ip}:5000/track"
        message = client.messages.create(
            body=f"Halo, kunjungi tautan ini: {tracking_link}",
            from_="whatsapp:+14155238886",  # Ganti dengan nomor WhatsApp Twilio Anda
            to=f"whatsapp:{target_number}"
        )
        print(f"[+] Pesan terkirim ke {target_number}, SID: {message.sid}")
    except Exception as e:
        print(f"[-] Error saat mengirim pesan WhatsApp: {str(e)}")

def banner():
    print("=" * 60)
    print("   OSINT WhatsApp Tracker with Safe Module Installer")
    print("=" * 60)

def main():
    banner()
    install_modules_safely()
    print("[1] Jalankan server pelacakan")
    print("[2] Kirim link pelacakan WhatsApp")
    print("[3] Dapatkan kredensial otomatis dengan Selenium")

    choice = input("[*] Pilih opsi (1/2/3): ")
    if choice == "1":
        start_tracking_server()
    elif choice == "2":
        print("[*] Menggunakan otomatisasi Selenium untuk kredensial...")
        sid, auth_token, public_ip = selenium_get_credentials_and_ip()
        target_number = input("[*] Masukkan nomor WhatsApp target (format internasional): ")
        send_tracking_link(sid, auth_token, public_ip, target_number)
    elif choice == "3":
        sid, auth_token, public_ip = selenium_get_credentials_and_ip()
        print(f"SID: {sid}, Auth Token: {auth_token}, IP Publik: {public_ip}")
    else:
        print("[-] Pilihan tidak valid.")

if __name__ == "__main__":
    main()
