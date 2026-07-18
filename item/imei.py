import os
import time
import json
import requests

try:
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init(autoreset=True)
except Exception:
    class Fore:
        BLACK = '\033[30m'; RED = '\033[1;31m'; GREEN = '\033[1;32m'
        YELLOW = '\033[1;33m'; BLUE = '\033[1;34m'; MAGENTA = '\033[1;35m'
        CYAN = '\033[1;36m'; WHITE = '\033[1;37m'
    class Style:
        RESET_ALL = '\033[0m'

Bl = Fore.BLACK
Re = Fore.RED
Gr = Fore.GREEN
Ye = Fore.YELLOW
Blu = Fore.BLUE
Mage = Fore.MAGENTA
Cy = Fore.CYAN
Wh = Fore.WHITE
RST = Style.RESET_ALL

TOOL_NAME = "Ghost-crack Community – CEK IMEI TOOL"
VERSION = "v1.0"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{Gr}

            {TOOL_NAME} {VERSION}
               Coded By d3nz 
{RST}""")

def cek_imei():
    banner()
    imei = input(f"{Wh}[{Gr}+{Wh}] Masukkan IMEI (14–17 digit): {Gr}").strip()

    if not (imei.isdigit() and 14 <= len(imei) <= 17):
        print(f"\n{Re}[!]{Wh} IMEI tidak valid. Harus 14–17 digit angka.{RST}")
        return

    print(f"\n{Wh}[{Gr}*{Wh}] Mengecek IMEI: {Gr}{imei}{RST}")
    time.sleep(1)

    url = "https://www.officialsimunlock.com/Home/GetIMEI"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (compatible; Python IMEI Checker)"
    }
    data = {"imei": imei}

    try:
        r = requests.post(url, data=data, headers=headers, timeout=20)
        r.raise_for_status()

        try:
            resp = r.json()
        except ValueError:
            resp = r.text

        print(f"\n{Gr}═══════════ HASIL CEK IMEI ═══════════{RST}")
        print(f"{Cy}IMEI{Wh} : {imei}")

        if isinstance(resp, dict):
            if "Success" in resp:
                print(f"{Cy}Success{Wh} : {resp['Success']}")
            if "Message" in resp:
                print(f"{Cy}Message{Wh} : {resp['Message']}")

            model = resp.get("Model")
            if model and isinstance(model, dict):
                print(f"\n{Gr}--- DETAIL DEVICE ---{RST}")
                for k, v in model.items():
                    print(f"{Cy}{k}{Wh} : {v}")

            print(f"\n{Gr}--- DATA TAMBAHAN ---{RST}")
            for k, v in resp.items():
                if k in ["Success", "Message", "Model"]:
                    continue
                if isinstance(v, (dict, list)):
                    print(f"{Cy}{k}{Wh} : {json.dumps(v, ensure_ascii=False)}")
                else:
                    print(f"{Cy}{k}{Wh} : {v}")

        elif isinstance(resp, str):
            print(f"\n{Ye}{resp}{RST}")

        else:
            print(f"{Ye}Tidak ada data detail dari server.{RST}")

    except requests.exceptions.Timeout:
        print(f"\n{Re}[!]{Wh} Request timeout saat menghubungi server IMEI.{RST}")
    except requests.exceptions.HTTPError as e:
        print(f"\n{Re}[!]{Wh} Server mengembalikan HTTP {e.response.status_code}{RST}")
    except Exception as e:
        print(f"\n{Re}[!]{Wh} Terjadi kesalahan: {e}{RST}")

def main():
    while True:
        cek_imei()
        lagi = input(f"\n{Wh}[{Gr}?{Wh}] Cek lagi? (y/n): {Gr}").strip().lower()
        if lagi != "y":
            print(f"\n{Wh}[{Gr}+{Wh}] Keluar dari tools...{RST}")
            time.sleep(1)
            break

def imei2():
    main()