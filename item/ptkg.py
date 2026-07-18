# Nusatenggara Timur Development
# Coded By denz!

import os
import time
import requests

try:
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init(autoreset=True)
except Exception:
    class Fore:
        RED = '\033[1;31m'
        GREEN = '\033[1;32m'
        CYAN = '\033[1;36m'
        WHITE = '\033[1;37m'
    class Style:
        RESET_ALL = '\033[0m'

Re = Fore.RED
Gr = Fore.GREEN
Cy = Fore.CYAN
Wh = Fore.WHITE
RST = Style.RESET_ALL


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    clear()
    print(f"""{Gr}
╔══════════════════════════════════════╗
║          CEK PTK GTK TOOL            ║
║        Coded By d3nz            ║
╚══════════════════════════════════════╝
{RST}""")


def cek_ptk():
    banner()

    keyword = input(f"{Wh}[{Gr}+{Wh}] Masukkan Nama / NIK / NUPTK: {Gr}").strip()

    if not keyword:
        print(f"{Re}Input kosong.{RST}")
        return

    print(f"\n{Wh}Menghubungi server GTK...{RST}")
    time.sleep(1)

    url = f"https://gtk.belajar.kemendikdasmen.go.id/akun/ptk-solr?keyword={keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Python PTK Checker)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()

        data = r.json()

        if not data or "data" not in data or not data["data"]:
            print(f"\n{Re}Data PTK tidak ditemukan.{RST}")
            return

        ptk = data["data"][0]
        sekolah = ptk.get("sekolah", {})

        prov = sekolah.get("m_propinsi", {}).get("keterangan", "-")
        kota = sekolah.get("m_kota", {}).get("keterangan", "-")

        print(f"\n{Gr}══════════ HASIL PTK GTK ══════════{RST}")

        print(f"{Cy}Nama{Wh}        : {ptk.get('nama','-')}")
        print(f"{Cy}NUPTK{Wh}       : {ptk.get('nuptk','-')}")
        print(f"{Cy}NIK Masked{Wh}  : {ptk.get('nik_masked','-')}")
        print(f"{Cy}Sekolah{Wh}     : {sekolah.get('nama','-')}")
        print(f"{Cy}NPSN{Wh}        : {sekolah.get('npsn','-')}")
        print(f"{Cy}Provinsi{Wh}    : {prov}")
        print(f"{Cy}Kab/Kota{Wh}    : {kota}")

        status = "Aktif" if ptk.get("status_ptk", {}).get("aktif") else "Tidak Aktif"
        print(f"{Cy}Status PTK{Wh}  : {status}")

        print(f"{Cy}Update{Wh}      : {ptk.get('tanggal_perbaharui','-')}")

    except requests.exceptions.Timeout:
        print(f"\n{Re}Timeout ke server GTK.{RST}")
    except Exception as e:
        print(f"\n{Re}Error: {e}{RST}")


def main():
    while True:
        cek_ptk()
        lagi = input(f"\n{Wh}Cek lagi? (y/n): {Gr}").strip().lower()
        if lagi != "y":
            print(f"\n{Wh}Keluar...{RST}")
            break


def guru():
    main()