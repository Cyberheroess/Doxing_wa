# <span style="color:#ff6347;">🚀 **Doxing WA**</span> - **OSINT WhatsApp Tracker** <span style="color:#ff6347;">🔍</span>

![17338966752836731961566911678352](https://github.com/user-attachments/assets/36237702-05b3-4fcd-9489-1dbb24cf21ce)


**Doxing WA** adalah alat **OSINT (Open-Source Intelligence)** yang memungkinkan Anda untuk melacak nomor WhatsApp target dan mengumpulkan berbagai informasi terkait secara otomatis. Script ini juga terintegrasi dengan **Twilio** untuk pengiriman link pelacakan dan penggunaan **Flask server** untuk menerima data IP dan User-Agent dari target.

---

## ✨ **Fitur Utama** <span style="color:#32cd32;">🌟</span>

<table border="1" cellpadding="10" cellspacing="0">
  <thead>
    <tr style="background-color:#ffebcd;">
      <th style="color:#ff6347;">Fitur</th>
      <th style="color:#32cd32;">Deskripsi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>🛠️ Kredensial Twilio Otomatis</strong></td>
      <td>Pengambilan SID dan Auth Token Twilio tanpa perlu input manual.</td>
    </tr>
    <tr>
      <td><strong>📲 Pengiriman Link Pelacakan</strong></td>
      <td>Link pelacakan WhatsApp akan dikirimkan ke target untuk melacak informasi.</td>
    </tr>
    <tr>
      <td><strong>🌍 IP Publik Otomatis</strong></td>
      <td>Menemukan IP publik target secara otomatis dan menampilkannya.</td>
    </tr>
    <tr>
      <td><strong>🖥️ Flask Server</strong></td>
      <td>Server untuk menerima dan memproses data seperti IP, User-Agent, dan lainnya.</td>
    </tr>
  </tbody>
</table>

---

## 🔧 **Persyaratan** <span style="color:#ffa500;">⚙️</span>
Sebelum memulai, pastikan Anda sudah memiliki perangkat dan pengaturan berikut:
- **Google Chrome** (pastikan versi terbaru).
- **ChromeDriver** sesuai dengan versi Google Chrome.
- **Python 3.x**.

---

## 📥 **Instalasi** <span style="color:#8a2be2;">🛠️</span>
1. **Clone repositori**:
   ```bash
   git clone https://github.com/Cyberheroess/Doxing_wa.git
   cd Doxing_wa
   ```
   # 💻versi server flask
```bash
python server.py
```
Script ini dirancang untuk mengumpulkan informasi tentang pengunjung situs web, termasuk alamat IP, user agent, dan lokasi geolokasi. Data yang dikumpulkan disimpan dalam database SQLite dan dapat diakses melalui antarmuka web.

## Daftar Isi

1. [Prasyarat](#prasyarat)
2. [Instalasi](#instalasi)
3. [Konfigurasi](#konfigurasi)
   - [Setel Variabel Lingkungan](#setel-variabel-lingkungan)
   - [Konfigurasi Database](#konfigurasi-database)
4. [Menjalankan Script](#menjalankan-script)
5. [Mengakses Antarmuka Web](#mengakses-antarmuka-web)
6. [Contoh Output](#contoh-output)
7. [Menghentikan Server](#menghentikan-server)
8. [Catatan Penting](#catatan-penting)

## Prasyarat

Sebelum memulai, pastikan Anda memiliki:

- **Python 3.x**: Pastikan Python terinstal di sistem Anda. Anda dapat mengunduhnya dari [python.org](https://www.python.org/downloads/).
- **Pip**: Pip biasanya sudah terinstal bersama Python. Anda dapat memeriksa dengan menjalankan `pip --version`.
- **Google Chrome**: Pastikan Anda memiliki browser Google Chrome yang terinstal.
- **ChromeDriver**: Unduh ChromeDriver yang sesuai dengan versi Chrome Anda dari [sini](https://sites.google.com/chromium.org/driver/).

## Instalasi

Ikuti langkah-langkah berikut untuk menginstal script:

1. **Unduh Script**:
   Unduh file script dari sumber yang Anda miliki dan simpan di direktori pilihan Anda.

2. **Instal Dependensi**:
   Buka terminal dan navigasikan ke direktori tempat Anda menyimpan script. Instal semua dependensi yang diperlukan dengan perintah:
   ```bash
   pip install requests flask selenium twilio
