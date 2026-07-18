# scrapingbyrolandino
import json
import time
import os
import subprocess
from datetime import datetime

API = "https://api.cellmapper.net/v6/getTowerInformation"

# =========================
# FUNGSI BANTUAN
# =========================

def garis(panjang=78):
    print("=" * panjang)

def garis_kecil(panjang=78):
    print("-" * panjang)

def aman(v, default="-"):
    return v if v not in [None, "", [], {}] else default

def format_timestamp(ts):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime("%d-%m-%Y %H:%M:%S UTC")
    except:
        return "Tidak diketahui"

def format_list(data):
    if isinstance(data, list) and data:
        return ", ".join(str(x) for x in data)
    return "-"

def status_visible(v):
    if v is True:
        return "Ya"
    elif v is False:
        return "Tidak"
    return "-"

def status_bool(v):
    if v is True:
        return "Tersedia"
    elif v is False:
        return "Tidak"
    return "-"

def buat_link_maps(lat, lon):
    if lat in [None, "-", ""] or lon in [None, "-", ""]:
        return "Tidak tersedia"
    return f"https://www.google.com/maps?q={lat},{lon}"

def simpan_json(site_id, region_id, data):
    folder = "hasil_bts"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"site_{site_id}_region_{region_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return file_path

# =========================
# AMBIL DATA VIA CURL
# =========================

def ambil_data_api(mcc, mnc, offset):
    url = f"{API}?MCC={mcc}&MNC={mnc}&offset={offset}"

    cmd = [
        "curl",
        "-s",
        "--max-time", "35",
        "-H", "Accept: application/json",
        url
    ]

    try:
        hasil = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        text = hasil.decode("utf-8", errors="ignore").strip()

        if not text:
            print("[!] Response kosong dari API.")
            return None

        try:
            data = json.loads(text)
            return data
        except Exception:
            print("[!] Gagal parse JSON dari API.")
            print("\n[DEBUG RAW RESPONSE]")
            print(text[:1500])
            return None

    except subprocess.CalledProcessError as e:
        print("[!] Curl error:")
        try:
            print(e.output.decode("utf-8", errors="ignore"))
        except:
            print(str(e))
        return None

    except Exception as e:
        print(f"[!] Gagal ambil data API: {e}")
        return None

# =========================
# TAMPILKAN HASIL
# =========================

def tampilkan_hasil(tower, mcc, mnc):
    lat = tower.get("latitude")
    lon = tower.get("longitude")
    maps = buat_link_maps(lat, lon)

    garis()
    print("                    HASIL INFORMASI BTS / TOWER")
    garis()

    print(" [ INFORMASI DASAR ]")
    garis_kecil()
    print(f"  Site ID                 : {aman(tower.get('siteID'))}")
    print(f"  Region ID               : {aman(tower.get('regionID'))}")
    print(f"  MCC                     : {mcc}")
    print(f"  MNC                     : {mnc}")
    print(f"  Jenis Jaringan (RAT)    : {aman(tower.get('RAT'))}")
    print(f"  Sub Jenis Jaringan      : {aman(tower.get('RATSubType'))}")
    print(f"  Tower Terlihat          : {status_visible(tower.get('visible'))}")
    print(f"  Tower Mover ID          : {aman(tower.get('towerMover'))}")

    print()
    print(" [ KOORDINAT & LOKASI ]")
    garis_kecil()
    print(f"  Latitude                : {aman(lat)}")
    print(f"  Longitude               : {aman(lon)}")
    print(f"  Link Google Maps        : {maps}")

    print()
    print(" [ INFORMASI FREKUENSI & JARINGAN ]")
    garis_kecil()
    print(f"  Channel / EARFCN        : {format_list(tower.get('channels'))}")
    print(f"  Bandwidth               : {format_list(tower.get('bandwidths'))}")
    print(f"  Nomor Band              : {format_list(tower.get('bandNumbers'))}")
    print(f"  Estimasi Data Band      : {format_list(tower.get('estimatedBandData'))}")
    print(f"  Data Bandwidth          : {status_bool(tower.get('bandwidthData'))}")
    print(f"  Data Frekuensi          : {status_bool(tower.get('frequencyData'))}")

    print()
    print(" [ WAKTU TERDETEKSI ]")
    garis_kecil()
    print(f"  Pertama Kali Terdeteksi : {format_timestamp(tower.get('firstseendate'))}")
    print(f"  Terakhir Kali Terdeteksi: {format_timestamp(tower.get('lastseendate'))}")

    print()
    print(" [ DATA TAMBAHAN ]")
    garis_kecil()
    print(f"  Data Cells              : {json.dumps(tower.get('cells', {}), ensure_ascii=False)}")
    print(f"  Atribut Tower           : {json.dumps(tower.get('towerAttributes', {}), ensure_ascii=False)}")

    print()
    print(" [ JSON MENTAH / RAW DATA ]")
    garis_kecil()
    print(json.dumps(tower, indent=2, ensure_ascii=False))

    garis()

# =========================
# PROSES PENCARIAN
# =========================

def cari_tower(site_id, region_id, mcc, mnc):
    offset = 0
    total_dicek = 0

    garis()
    print("                   CELLMAPPER LIVE BTS LOOKUP")
    garis()
    print(f" Target Site ID   : {site_id}")
    print(f" Target Region ID : {region_id}")
    print(f" MCC              : {mcc}")
    print(f" MNC              : {mnc}")
    garis()

    while True:
        print(f"[+] Memindai offset {offset}...")

        data = ambil_data_api(mcc, mnc, offset)

        if not data:
            print("[!] Gagal mendapatkan data dari API.")
            return

        if offset == 0:
            print(f"[i] Status API        : {data.get('statusCode', '-')}")
            print(f"[i] hasMore           : {data.get('hasMore', '-')}")
            print(f"[i] Tipe responseData : {type(data.get('responseData')).__name__}")

        towers = data.get("responseData", [])

        if not isinstance(towers, list):
            print("[!] Format data dari API tidak valid.")
            return

        if not towers:
            print("[!] Batch ini kosong / tidak berisi data tower.")

        for tower in towers:
            if not isinstance(tower, dict):
                continue

            total_dicek += 1

            tower_site = str(tower.get("siteID", "")).strip()
            tower_region = str(tower.get("regionID", "")).strip()

            if tower_site == str(site_id).strip() and tower_region == str(region_id).strip():
                print(f"\n[✓] Tower ditemukan setelah memeriksa {total_dicek} data.\n")

                tampilkan_hasil(tower, mcc, mnc)

                file_hasil = simpan_json(site_id, region_id, tower)
                print(f"[✓] Data berhasil disimpan ke: {file_hasil}")
                return

        if not data.get("hasMore", False):
            break

        offset += 100
        time.sleep(0.5)

    print("\n[!] Tower tidak ditemukan.")
    print(f"[i] Pencarian berdasarkan:")
    print(f"    - Site ID   : {site_id}")
    print(f"    - Region ID : {region_id}")
    print(f"    - MCC       : {mcc}")
    print(f"    - MNC       : {mnc}")
    print(f"[i] Total data yang telah diperiksa: {total_dicek}")

# =========================
# MAIN
# =========================

def cell():
    garis()
    print("                    INFORMASI BTS / TOWER")
    garis()

    site_id   = input(" Masukkan Site ID   : ").strip()
    region_id = input(" Masukkan Region ID : ").strip()
    mcc       = input(" Masukkan MCC       : ").strip()
    mnc       = input(" Masukkan MNC       : ").strip()

    print()
    cari_tower(site_id, region_id, mcc, mnc)