import sys
sys.dont_write_bytecode = True

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import requests
import json
import os
import sys
import time
import random
import ipaddress
import socket
import ssl
import http.client
import hashlib
import re
import threading
import concurrent.futures
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from item.sfilemobi import SfileSearcher
from item.ip import ip
from item.ngl import ngl_run
from item.exploit import memek
from item.web_recon import recon
from item.server import server 
from item.osintusr import osint 
from item.gosin import imei
from item.leak import leaktol
from item.phone import phone
from item.imei import imei2
from item.ewalet import ewalet
from item.ptkg import guru
from item.cell import cell
a = "\033[1;30m"
m = "\033[1;31m"
h = "\033[1;32m"
k = "\033[1;33m"
c = "\033[1;36m"
p = "\033[1;37m"
r = "\033[0m"

init(autoreset=True)

binid = "6a325d0ada38895dfecee184"
apikeybin = "$2a$10$AK24OjaA6gI.jt9Q1cVufeL2peBFlGkpSS9wGI.Pcybk.nG.fWO7a"
accesskey = "DENZ"

yellow = Fore.YELLOW
white = Fore.WHITE
red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
magenta = Fore.MAGENTA
blue = Fore.BLUE
hitam = Fore.BLACK
    
ipaddress = ""
ip_tersensor = True
    
USER_UID = "-"
USER_NAMA = "-"
USER_STATUS = "-"

BOT_REGISTER = "8833715654:AAFThpTzx7BVzRHka6gFKC65PZSmQX5oxHE"
ID_TELE_ADMIN = "8844146703"

def gtc():
    folder = "gtc"
    
    if not os.path.exists(folder):
        print(f"{yellow}[{red}!{yellow}] {white}Module {folder} tidak ditemukan")
        return
    
    try:
        subprocess.run(
            [sys.executable, "run.py"],
            cwd=folder,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"{red}Error menjalankan run.py: {e}{white}")
    except KeyboardInterrupt:
        print(f"\n{yellow}Dihentikan oleh pengguna.{white}")
    except FileNotFoundError:
        print(f"{red}File run.py tidak ditemukan di dalam folder {folder}{white}")

    
def get_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json()["ip"]
    except:
        return "N/A"

def toggle_sensor_ip():
    global ip_tersensor
    ip_tersensor = not ip_tersensor
    
def sensor_ip(ip):
    try:
        hasil = ""
        for char in str(ip):
            if char == ".":
                hasil += "."
            elif char.isdigit():
                hasil += "×"
            else:
                hasil += char
        return hasil
    except:
        return ip
    
def kirim_registrasi_telegram(device_id, username):
    pesan = f"""
📨 Data Registrasi Masuk

ID PENGGUNA
`{device_id}`

NAMA AKUN PENGGUNA
`{username}`
"""
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_REGISTER}/sendMessage",
            json={
                "chat_id": ID_TELE_ADMIN,
                "text": pesan,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        return True
    except:
        return False
    
def get_devid():
    try:
        import hashlib
        whoami = os.popen('whoami').read().strip()
        id_output = os.popen('id').read().strip()
        uid_match = re.search(r'uid=(\d+)', id_output)
        uid = uid_match.group(1) if uid_match else "0"
        ctx_match = re.search(r'context=([^\s]+)', id_output)
        ctx = ctx_match.group(1) if ctx_match else ""
        c_vals = re.findall(r'c(\d+)', ctx)
        c_str = ''.join(c_vals[:2]) if c_vals else ""
        mac = os.popen("ip link show 2>/dev/null | grep 'link/ether' | awk '{print $2}' | head -1").read().strip().replace(":", "")
        serial = os.popen("getprop ro.serialno 2>/dev/null").read().strip()
        android_id = os.popen("settings get secure android_id 2>/dev/null").read().strip()
        build_id = os.popen("getprop ro.build.id 2>/dev/null").read().strip()
        fingerprint = os.popen("getprop ro.build.fingerprint 2>/dev/null").read().strip()
        termux_home = os.path.expanduser("~")
        inode = str(os.stat(termux_home).st_ino) if os.path.exists(termux_home) else ""
        raw = f"{whoami}{uid}{c_str}{mac}{serial}{android_id}{build_id}{fingerprint}{inode}"
        raw = re.sub(r'[^a-zA-Z0-9]', '', raw)
        hashed = hashlib.sha256(raw.encode()).hexdigest()[:20]
        return hashed
    except:
        try:
            import hashlib
            fallback = os.popen('whoami').read().strip() + str(os.getuid())
            return hashlib.md5(fallback.encode()).hexdigest()[:20]
        except:
            return "unknown"

def loading_bar(duration=2, text="Memproses"):
    bar_length = 30
    for i in range(bar_length + 1):
        percent = i / bar_length
        bar = "█" * int(bar_length * percent) + "░" * (bar_length - int(bar_length * percent))
        sys.stdout.write(f"\r{cyan}{text} [{bar}] {int(percent*100)}%{white}")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    print()

def loading_spinner(duration=1.5, text="Loading"):
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{cyan}{spinner[i % len(spinner)]} {text}{white}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 30 + "\r", end="")

def typing_animation(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_banner():
    now = datetime.now()
    tanggal = now.strftime('%d-%m-%Y')
    jumlah_user = jumlah_uid_terdaftar()
    user_text = f"{jumlah_user} User"
    ip_sensor = sensor_ip(ipaddress) if ip_tersensor else ipaddress
    uid_text = USER_UID
    nama_text = USER_NAMA
    status_text = USER_STATUS
    jarak_users = " " * (16 - len(str(user_text)))
    jarak_tanggal = " " * (16 - len(str(tanggal)))
    jarak_ip = " " * (23 - len(str(ip_sensor)))
    jarak_id = " " * (24 - len(str(uid_text)))
    jarak_nama = " " * (19 - len(str(nama_text)))
    jarak_status = " " * (19 - len(str(status_text)))

    print(f"""{a}
╭─────────────────────────────────────────────────────────────╮
│{k} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                               {a}│
│{k}⠀⠀⠀⠀⠀⠀⠀⢶⠦⣄⡀⠀⢸⣿⣦⡀⠀⠀⠀⠀⠀⠀{h}⠀ ┌─┐┬ ┬┌─┐┌─┐┌┬┐   ┌┬┐┬─┐┌─┐┌─┐┬┌─.   {a}│
│{k}⠀⠀⠀⠀⠀⠀⠀⠘⡄⣠⣿⣦⣈⡙⠛⠳⠀⠀⠀⠀⠀⠀{h}⠀⠀│ ┬├─┤│ │└─┐ │{a} ───{h} │ ├┬┘├─┤│  ├┴┐    {a}│
│{k}⠀⠀⠀⠀⠀⠀⠀⠀⢻⣽⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀{h}⠀⠀└─┘┴ ┴└─┘└─┘ ┴     ┴ ┴└─┴ ┴└─┘┴ ┴    {a}│
│{k}⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀{a} ───────────────────────────────────.  {a}│
│{k}⠀⠀⠀⠀⠀⣺⣿⣿⣿⣿⠿⠒⠈⠉⠛⠿⣷⣦⡙⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀                               {a}│
│{k}⠀⠀⠀⠀⣰⣿⣿⣿⣟⡅⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣷⣤⣀⡀⠀⠀⠀⠀⠀ {h}ꫝ{p} Author    {m}:{h} Denz×Kevin      {a}│
│{k}⠀⠀⠀⢰⣿⣿⣿⠿⠿⠀⠀⠀⠀⠀⠀⡠⠖⠲⠤⠄⠀⠉⠉⠜⢁⣷⡀⠀⠀⠀ {h}ꫝ{p} Designer  {m}:{h} Byexe           {a}│
│{k}⠀⠀⠀⠟⠋⣁⣤⡴⠶⠶⠶⢿⣷⢶⣤⣁⡀⠀⠀⠀⠀⣀⣀⣴⣾⣿⣿⡄⠀⠀ {h}ꫝ{p} Version   {m}:{h} 4.5.0           {a}│
│{k}⠀⠀⢀⣴⣛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⣙⡻⣿⣶⣦⣤⣴⣶⣿⣿⣿⣿⡇⠀⠀ {h}ꫝ{p} Users     {m}:{h} {user_text}{jarak_users}{a}│
│{k}⠀⠀⢈⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀ {h}ꫝ{p} Tanggal   {m}:{h} {tanggal}{jarak_tanggal}{a}│
│{k}⠀⢠⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀                               {a}│
│{k}⠀⢸⡇⠀⠀⢀⣀⣀⣀⣀⠀⠀⠀⠀⢤⣤⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀                               {a}│
│{k}⠀⢸⣧⡶⠟⠋⠉⢩⣿⣿⣉⣀⣀⣀⣀⣩⣽⣿⣿⣿⣿⢿⣿⡿⠟⠁⠀⠀⠀⠀                               {a}│
│{k}⠀⠘⠋⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠛⠛⠛⠉⠉⠉⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀                               {a}│
╰─────────────────────────────────────────────────────────────╯
╭──────────────────────────────╮╭─────────────────────────────╮{a}
│{k} IP{m} : {p}{ip_sensor}{jarak_ip}{a} ││{k} NAME{m}   :{p} {nama_text}{jarak_nama}{a}│
│{k} ID{m} :{p} {uid_text}{jarak_id}{a}││{k} STATUS{m} : {p}{status_text}{jarak_status}{a}│
╰──────────────────────────────╯╰─────────────────────────────╯""")

def load_uid_database():
    url = f"https://api.jsonbin.io/v3/b/{binid}/latest"
    headers = {
        "X-Master-Key": apikeybin,
        "X-Access-Key": accesskey
    }
    try:
        res = requests.get(url, headers=headers, timeout=30)
        if res.status_code == 401:
            return None
        res.raise_for_status()
        data = res.json()
        if "record" in data:
            return data["record"]
        return data
    except:
        return None

def cek_uid_device(device_id):
    db = load_uid_database()
    if db is None:
        return None, None
    users = db.get("users", [])
    for user in users:
        if user.get("device_id") == device_id:
            return True, user
    return False, None

def jumlah_uid_terdaftar():
    db = load_uid_database()
    if not db:
        return 0
    return len(db.get("users", []))
    
def save_users(users):
    url = f"https://api.jsonbin.io/v3/b/{binid}"
    headers = {
        "X-Master-Key": apikeybin,
        "X-Access-Key": accesskey,
        "Content-Type": "application/json"
    }
    data = {"users": users}
    try:
        res = requests.put(url, json=data, headers=headers, timeout=30)
        return res.status_code == 200
    except:
        return False

def get_remaining_days(expiry_str):
    if not expiry_str:
        return "∞ (Admin)"
    try:
        expiry = datetime.fromisoformat(expiry_str)
        remaining = (expiry - datetime.now()).days
        if remaining < 0:
            return "Expired"
        return f"{remaining} hari"
    except:
        return "Tidak diketahui"

def check_nik(nik_user):
    url = "https://indonesia-ktp-parser-validator.p.rapidapi.com/ktp_validator"
    payload = {"nik": nik_user}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "f11650a45amsh3e76202887793b1p186972jsn95b1a9eb9539",
        "X-RapidAPI-Host": "indonesia-ktp-parser-validator.p.rapidapi.com"
    }
    try:
        respon = requests.post(url, json=payload, headers=headers)
        respons = respon.json()
        if respons['result']['status'] == "success":
            data = respons['result']['data']
            print(f"\n{green}Jenis Kelamin : {white}" + data['kelamin'])
            print(f"{green}Tanggal Lahir : {white}" + data['lahir'])
            print(f"{green}Provinsi :{white} " + data['provinsi'])
            print(f"{green}Kota/Kabupaten : {white}" + data['kotakab'])
            print(f"{green}Kecamatan :{white} " + data['kecamatan'])
            print(f"{green}Uniqcode :{white} " + data['uniqcode'])
            return True
        else:
            print(f"{red}Gagal mendapatkan data. Status: " + respons['result']['status'])
            return False
    except Exception as e:
        print(f"{red}Error: {e}{white}")
        return False

def telegram_spam():
    print(f"{yellow}1. Spam Teks{white}".center(os.get_terminal_size().columns))
    print(f"{yellow}2. Spam Gambar{white}".center(os.get_terminal_size().columns))
    print(f"{yellow}3. Spam Teks + Gambar{white}".center(os.get_terminal_size().columns))
    sp = input(f"\n{green}Pilih Menu -> {white}")
    if sp in ['01','1']:
        token = input(f"{yellow}Masukkan Token : {white}")
        chat_id = input(f"{yellow}Masukkan Chat Id : {white}")
        text = input(f"{yellow}Text : {white}")
        jumlah = int(input(f"{yellow}Jumlah : {white}"))
        print(f"{cyan}Processing...{white}".center(os.get_terminal_size().columns))
        for i in range(jumlah):
            send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}'
            requests.get(send_text)
            print(f"{green}Succes : {blue}{i}{white}".center(os.get_terminal_size().columns))
        print(f"{green}Berhasil spam dengan teks : {yellow}{text}{green} Dengan Jumlah {yellow}{jumlah}{white}".center(os.get_terminal_size().columns))
    if sp in ['02','2']:
        token = input(f"{yellow}Masukkan Token : {white}")
        chat_id = input(f"{yellow}Masukkan Chat Id : {white}")
        photo_url = input(f"{yellow}Image Url : {white}")
        jumlah = int(input(f"{yellow}Jumlah : {white}"))
        print(f"{cyan}Processing...{white}".center(os.get_terminal_size().columns))
        for i in range(jumlah):
            send_photo = f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&photo={photo_url}'
            requests.get(send_photo)
            print(f"{green}Succes : {blue}{i}{white}".center(os.get_terminal_size().columns))
        print(f"{green}Berhasil spam dengan gambar, Dengan Jumlah {yellow}{jumlah}{white}".center(os.get_terminal_size().columns))
    if sp in ['03','3']:
        token = input(f"{yellow}Masukkan Token : {white}")
        chat_id = input(f"{yellow}Masukkan Chat Id : {white}")
        text = input(f"{yellow}Text : {white}")
        photo_url = input(f"{yellow}Image Url : {white}")
        jumlah = int(input(f"{yellow}Jumlah : {white}"))
        print(f"{cyan}Processing...{white}".center(os.get_terminal_size().columns))
        for i in range(jumlah):
            send_photo = f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&photo={photo_url}'
            send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}'
            requests.get(send_photo)
            requests.get(send_text)
            print(f"{green}Succes : {blue}{i}{white}".center(os.get_terminal_size().columns))
        print(f"{green}Berhasil spam dengan teks : {yellow}{text}{green} dan Gambar, Dengan Jumlah {yellow}{jumlah}{white}".center(os.get_terminal_size().columns))
def main():
    global USER_UID, USER_NAMA, USER_STATUS, ipaddress

    
    DEVICE_ID = get_devid()
    status, user_data = cek_uid_device(DEVICE_ID)

    if status is None:
        print(f"{red}Gagal terhubung ke database!{white}")
        sys.exit(1)

    if status is False:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{a}
╭─────────────────────────────────────────────────────────────╮
│{p} Silakan {h}buat {h}username{p} untuk akun ghost-crack Anda. {h}Username {a}│
│{p} {h}digunakan sebagai identitas akun saat login{p} dan{h} menggunakan {a}│
│{p} {h}fitur yang tersedia{p}. Gunakan nama yang singkat, mudah       {a}│
│{p} diingat, tanpa spasi, dengan panjang 2 hingga 7 karakter.   {a}│
│{p} Contoh username: {h}Daemon{p}, {h}User01{p}, atau {h}King77{p}. Jika sudah    {a}│
│{p} sesuai syarat, Anda dapat langsung melanjutkan.             {a}│
╰── {a}╭─ {m}[{p} U S E R N A M E {m}]{a} ───────────────────────────────────╯""")

        while True:
            c_namabaru = input(f"    {a}╰──{h}➤{p} ").strip()
            if (
                len(c_namabaru) < 2 or
                len(c_namabaru) > 7 or
                " " in c_namabaru or
                not re.match(r'^[a-zA-Z0-9_]+$', c_namabaru)
            ):
                input(f"\n  [!] Username Tidak Sesuai Aturan | ENTER")
                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"""{a}
╭─────────────────────────────────────────────────────────────╮
│{p} Silakan {h}buat {h}username{p} untuk akun ghost-crack Anda. {h}Username  {a}││{p} {h}digunakan sebagai identitas akun saat login{p} dan{h} menggunakan {a}│
│{p} {h}fitur yang tersedia{p}. Gunakan nama yang singkat, mudah       {a}│
│{p} diingat, tanpa spasi, dengan panjang 2 hingga 7 karakter.   {a}│
│{p} Contoh username: {h}Daemon{p}, {h}User01{p}, atau {h}King77{p}. Jika sudah    {a}│
│{p} sesuai syarat, Anda dapat langsung melanjutkan.             {a}│
╰── {a}╭─ {m}[{p} U S E R N A M E {m}]{a} ───────────────────────────────────╯""")
                continue
            break

        os.system('clear' if os.name == 'posix' else 'cls')
        loading_spinner(1.5, "Mengirim Data Registrasi")
        kirim_registrasi_telegram(DEVICE_ID, c_namabaru)
        time.sleep(1)
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{a}
╭───────────────────────────────────────────────╮
│                                               │
│  ⠀{p}╔═╗╔═╗╔╗╔╔═╗╔═╗╔═╗╔═╗╦╔═╔═╗╔╗╔    {m}╦ ╦{h}╦{k}╔╦╗   {a}│
│   {p}╠═╝║╣ ║║║║ ╦║╣ ║  ║╣ ╠╩╗╠═╣║║║    {m}║ ║{h}║ {k}║║   {a}│
│   {p}╩  ╚═╝╝╚╝╚═╝╚═╝╚═╝╚═╝╩ ╩╩ ╩╝╚╝    {m}╚═╝{h}╩{k}═╩╝⠀  {a}│
│  {m}───────────────────────────────────────────  {a}│
│   {p}Sistem Validasi UID Untuk Mengakses Tools   {a}│
│                                               {a}│
╰───────────────────────────────────────────────╯
╭───────────────────────────────────────────────╮
│ {h}Tunggu Sampai UID Kamu Didaftarkan Oleh Admin {a}│
╰───────────────────────────────────────────────╯""")
        sys.exit(0)

    username = user_data.get("nama", DEVICE_ID)
    USER_UID = user_data.get("device_id", DEVICE_ID)
    USER_NAMA = user_data.get("nama", "Unknown")
    USER_STATUS = user_data.get("status", "Unknown")
    ipaddress = get_ip()
    
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        status, user_data = cek_uid_device(DEVICE_ID)
        USER_STATUS = user_data.get("status", "Unknown")
        nama_fitur_ip = f"{'Tampilkan' if ip_tersensor else 'Sembunyikan'} IP Saya"
        show_banner()

        print(f"""{a}╭──────────────────────── {m}[{p} M E N U {m}]{a} ────────────────────────╮
│                                                             │
│ {p}[{k}01{p}] Gosin menu                                             {a}│
│ {p}[{k}02{p}] Cek NIK dari Nomor Telepon                             {a}│
│ {p}[{k}03{p}] Osint username                                         {a}│
│ {p}[{k}04{p}] Phone Number Osint Tool                                {a}│
│ {p}[{k}05{p}] NIK Checker                                            {a}│
│ {p}[{k}06{p}] Telegram Spam Bot                                      {a}│
│ {p}[{k}07{p}] Sfile.mobi Searcher                                    {a}│
│ {p}[{k}08{p}] Web Recon {m}({p}Ultra Brutal{m})                               {a}│
│ {p}[{k}09{p}] RAT Control {m}({p}Remote Ransomware {m})                       {a}│
│ {p}[{k}10{p}] Crack IP Address                                       {a}│
│ {p}[{k}11{p}] Spam NGL                                               {a}│
│ {p}[{k}12{p}] Create APK Ransomware                                  {a}│
│ {p}[{k}13{p}] {nama_fitur_ip}{' ' * (55 - len(nama_fitur_ip))}{a}│
│ {p}[{k}14{p}] Crack imei                                             {a}│
│ {p}[{k}15{p}] Cek data guru                                          {a}│
│ {p}[{k}16{p}] Cellmapper loakup                                      {a}│
│ {p}[{k}17{p}] Ewallet Checker                                        {a}│
│ {p}[{k}18{p}] gtc Checker                                            {a}│
│ {p}[{k}00{p}] Keluar                                                 {a}│
│                                                             │
╰── ╭─ {m}[{p} P I L I H {m}]{a} ─────────────────────────────────────────╯""")

        pilihan = input(f"    {a}╰──{h}➤{p} ").strip().lower()

        if pilihan in ["1", "01"]:
            imei()
            
        elif pilihan in ["2", "02"]:
            leaktol()

        elif pilihan in ["3", "03"]:
            osint()

        elif pilihan in ["4", "04"]:
            phone()

        elif pilihan in ["5", "05"]:
            os.system('clear' if os.name == 'posix' else 'cls')
            show_banner()
            nik = input(f"{yellow}NIK (16 digit): {white}")
            if len(nik) == 16:
                check_nik(nik)
            else:
                print(f"{red}NIK harus 16 digit!{white}".center(os.get_terminal_size().columns))
            input(f"\n{cyan}Tekan Enter...{white}".center(os.get_terminal_size().columns))

        elif pilihan in ["6", "06"]:
            telegram_spam()
            input(f"\n{cyan}Tekan Enter...{white}".center(os.get_terminal_size().columns))

        elif pilihan in ["7", "07"]:
            searcher = SfileSearcher()
            searcher.sfile_search_main()

        elif pilihan in ["8", "08"]:
            recon()

        elif pilihan in ["9", "09"]:
            server()
            
        elif pilihan in ["10"]:
            ip()
            
        elif pilihan in ["11"]:
            ngl_run("NEXUS_NGL_462_X7K2P9A4M8D1Q6W3E5R7T9Y2U4I6O8P1A3S5D7F9G2H4J6K8L1Z3X5KANBI972MNBAVHM6Q8W1E3R5T7Y9U2I4O6P8A1S3D5F7G9H2J4K6L8Z1X3C5V7B9N2M4Q6W8E1R3T5Y7U9I2O4P6A8S1D3F5G7H9J2K4L6Z8X1C3V5B7N9")
            
        elif pilihan in ["12"]:
            memek()
            
        elif pilihan in ["13"]:
            toggle_sensor_ip()
            
        elif pilihan in ["14"]:
            imei2()
            
        elif pilihan in ["15"]:
            guru()
            
        elif pilihan in ["16"]:
            cell()
            
        elif pilihan in ["17"]:
             ewalet()

        elif pilihan in ["18"]:
            gtc()
                    
        elif pilihan in ["0", "00"]:
            os.system("clear")
            break

        else:
            print(f"{red}❌ Pilihan tidak valid!{white}".center(os.get_terminal_size().columns))
            time.sleep(1)

if __name__ == "__main__":
    main()
