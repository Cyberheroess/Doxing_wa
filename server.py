import os
import subprocess
import sys
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from flask import Flask, request, jsonify, render_template
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    conn = sqlite3.connect('tracking.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            location TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_visit(ip, user_agent, location):
    conn = sqlite3.connect('tracking.db')
    c = conn.cursor()
    c.execute('INSERT INTO visits (ip, user_agent, location) VALUES (?, ?, ?)', (ip, user_agent, location))
    conn.commit()
    conn.close()

def install_modules_safely():
    modules = ["requests", "flask", "selenium", "twilio", "sqlite3"]
    logging.info("Memulai proses instalasi modul...")

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
                logging.info(f"Mencoba: {method}")
                result = subprocess.run(
                    method, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if result.returncode == 0:
                    logging.info(f"Modul '{module}' berhasil diinstal.")
                    installed = True
                    break
                else:
                    logging.warning(f"Gagal dengan perintah: {method}")
            except Exception as e:
                logging.error(f"Error saat menjalankan: {method}, {str(e)}")

        if not installed:
            logging.error(f"Modul '{module}' gagal diinstal setelah mencoba semua metode.")

    logging.info("Instalasi selesai. Memastikan semua modul diimpor...")
    try:
        for module in modules:
            __import__(module)
        logging.info("Semua modul berhasil diimpor tanpa error.")
    except ImportError as e:
        logging.error(f"Modul tidak ditemukan meskipun sudah diinstal: {str(e)}")

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        location = f"{data.get('city')}, {data.get('region')}, {data.get('country')}"
        return location
    except Exception as e:
        logging.error(f"Error mendapatkan lokasi: {str(e)}")
        return "Unknown"

def selenium_get_credentials_and_ip():
    logging.info("Menjalankan bot Selenium untuk otomatisasi...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service("chromedriver")  # Pastikan chromedriver ada di direktori yang sama
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Masuk ke Twilio untuk mengambil SID dan Auth Token
        logging.info("Membuka halaman login Twilio...")
        driver.get("https://www.twilio.com/login")
        sleep(5)

        # Isi kredensial dari variabel lingkungan
        email = os.getenv("TWILIO_EMAIL")  # Ganti dengan email Twilio Anda
        password = os.getenv("TWILIO _PASSWORD")  # Ganti dengan password Twilio Anda

        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "password").send_keys("\n")
        sleep(5)

        driver.get("https://console.twilio.com/")
        sleep(5)
        sid = driver.find_element(By.XPATH, "//span[text()='Account SID']").text
        auth_token = driver.find_element(By.XPATH, "//span[text()='Auth Token']").text
        logging.info(f"SID: {sid}")
        logging.info(f"Auth Token: {auth_token}")

        # Dapatkan IP Publik
        driver.get("https://ifconfig.me/")
        public_ip = driver.find_element(By.TAG_NAME, "body").text.strip()
        logging.info(f"IP Publik: {public_ip}")

        return sid, auth_token, public_ip
    except Exception as e:
        logging.error(f"Error pada Selenium: {str(e)}")
    finally:
        driver.quit()

def start_tracking_server():
    app = Flask(__name__)

    @app.route("/track", methods=["GET"])
    def track():
        ip = request.remote_addr
        user_agent = request.headers.get('User -Agent')
        location = get_location(ip)  # Dapatkan lokasi berdasarkan IP
        log_visit(ip, user_agent, location)  # Log kunjungan ke database
        logging.info(f"Pelacakan dari IP: {ip}, User-Agent: {user_agent}, Lokasi: {location}")
        return jsonify({"ip": ip, "user_agent": user_agent, "location": location})

    @app.route("/visits", methods=["GET"])
    def visits():
        conn = sqlite3.connect('tracking.db')
        c = conn.cursor()
        c.execute('SELECT * FROM visits ORDER BY timestamp DESC')
        visits_data = c.fetchall()
        conn.close()
        return render_template('visits.html', visits=visits_data)

    @app.route("/stop", methods=["POST"])
    def stop_server():
        logging.info("Menghentikan server...")
        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown is not None:
            shutdown()
            logging.info("Server berhasil dihentikan.")
            return "Server dihentikan", 200
        else:
            logging.error("Tidak dapat menghentikan server.")
            return "Tidak dapat menghentikan server", 500

    init_db()  # Inisialisasi database
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    install_modules_safely()
    sid, auth_token, public_ip = selenium_get_credentials_and_ip()
    logging.info("Memulai server pelacakan...")
    start_tracking_server()
