import sys
sys.dont_write_bytecode = True
import os
import re
import time
import random
import string
import threading
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

a = "\033[1;30m"
m = "\033[1;31m"
h = "\033[1;32m"
k = "\033[1;33m"
p = "\033[1;37m"
r = "\033[0m"

_INTERNAL_TOKEN = "NEXUS_NGL_462_X7K2P9A4M8D1Q6W3E5R7T9Y2U4I6O8P1A3S5D7F9G2H4J6K8L1Z3X5KANBI972MNBAVHM6Q8W1E3R5T7Y9U2I4O6P8A1S3D5F7G9H2J4K6L8Z1X3C5V7B9N2M4Q6W8E1R3T5Y7U9I2O4P6A8S1D3F5G7H9J2K4L6Z8X1C3V5B7N9"

def h_cursor():
    print("\033[?25l", end="")

def s_cursor():
    print("\033[?25h", end="")

def ngl_run(token):
    if token != _INTERNAL_TOKEN:
        time.sleep(999999)
        return
    ngl_spam_main()

def ngl_spam_pesan_acak():
    return [
        "Lagi ngapain sekarang?",
        "Kamu lagi dimana?",
        "Aku kangen deh sama kamu",
        "Umur kamu berapa sih kalau boleh tau?",
        "Lagi sibuk gak?",
        "Kok jarang online akhir-akhir ini?",
        "Aku mau confess tapi takut ditolak",
        "Sebenernya aku suka sama kamu",
        "Kamu udah makan belum?",
        "Hari ini capek gak?",
        "Kamu tipe orang yang setia gak sih?",
        "Kalau lagi sedih biasanya ngapain?",
        "Pengen deket tapi gengsi",
        "Kamu masih single kan?",
        "Aku kepikiran kamu terus",
        "Kamu orangnya humoris ya",
        "Kalau weekend biasanya ngapain?",
        "Aku penasaran sama kehidupan kamu",
        "Boleh kenalan lebih dekat gak?",
        "Kamu punya pacar gak sekarang?",
        "Kamu cakep/cantik banget sih",
        "Aku nyaman ngobrol sama kamu",
        "Kamu lagi bad mood ya?",
        "Jangan lupa jaga kesehatan ya",
        "Aku seneng liat story kamu",
        "Kok kamu jarang update sih?",
        "Aku pengen chat kamu tapi malu",
        "Kamu suka dengerin lagu apa?",
        "Kalau lagi galau biasanya ngapain?",
        "Aku pengen jadi orang spesial buat kamu",
        "Kamu lagi mikirin apa sekarang?",
        "Aku iri sama orang yang deket sama kamu",
        "Kamu gampang baper gak?",
        "Aku pengen jujur tapi takut kamu ilfeel",
        "Kamu percaya cinta online gak?",
        "Aku selalu nunggu balasan kamu",
        "Kamu pernah suka diam-diam gak?",
        "Aku pengen ngajak kamu jalan",
        "Kamu lagi overthinking ya?",
        "Aku nyaman sama kamu tanpa alasan",
        "Kamu orangnya perhatian banget",
        "Aku suka cara kamu ngomong",
        "Kalau aku bilang aku suka, kamu gimana?",
        "Kamu bikin hari aku lebih baik",
        "Aku takut kehilangan kamu",
        "Kamu masih inget aku gak?",
        "Aku pengen lebih sering ngobrol sama kamu",
        "Kamu itu bikin penasaran",
        "Aku pengen jadi tempat cerita kamu",
        "Kamu lagi bahagia gak sekarang?"
    ]

def ngl_spam_ua():
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.1; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; Nokia G20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    ]

def ngl_spam_sec_ch_ua(user_agent):
    if "Chrome/120" in user_agent:
        return '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
    elif "Chrome/119" in user_agent:
        return '"Not_A Brand";v="8", "Chromium";v="119", "Google Chrome";v="119"'
    elif "Chrome/118" in user_agent:
        return '"Not_A Brand";v="8", "Chromium";v="118", "Google Chrome";v="118"'
    elif "Edge" in user_agent:
        return '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"'
    else:
        return '"Not_A Brand";v="99", "Chromium";v="120"'

def ngl_spam_proxy():
    try:
        url = "https://www.sslproxies.org/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        proxy_list = []
        table = soup.find('table', {'class': 'table table-striped table-bordered'})
        
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows[:50]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxy = f"http://{ip}:{port}"
                    proxy_list.append(proxy)
        
        if not proxy_list:
            proxy_list = [
                "http://103.152.112.162:80",
                "http://47.251.43.115:33333",
                "http://20.206.106.192:8123",
                "http://185.217.143.96:9090",
                "http://103.152.112.145:80"
            ]
        
        return proxy_list
    except:
        return [
            "http://103.152.112.162:80",
            "http://47.251.43.115:33333",
            "http://20.206.106.192:8123",
            "http://185.217.143.96:9090",
            "http://103.152.112.145:80"
        ]

def ngl_spam_devid():
    device_types = [
        f"{''.join(random.choices(string.hexdigits.lower(), k=16))}",
        f"web-{random.randint(100000000, 999999999)}",
        f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=32))}",
        f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
    ]
    return random.choice(device_types)

def ngl_spam_pesan_random(message):
    variations = [
        message,
        message + " ",
        " " + message,
        message + "  ",
        message.replace(" ", "  "),
    ]
    return random.choice(variations)

def ngl_spam_header(user_agent, username):
    is_mobile = "Mobile" in user_agent or "iPhone" in user_agent or "Android" in user_agent
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.9", "en-US,en;q=0.8"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://ngl.link",
        "Referer": f"https://ngl.link/{username}",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
    
    if "Chrome" in user_agent or "Edge" in user_agent:
        headers["sec-ch-ua"] = ngl_spam_sec_ch_ua(user_agent)
        headers["sec-ch-ua-mobile"] = "?1" if is_mobile else "?0"
        headers["sec-ch-ua-platform"] = random.choice(['"Windows"', '"macOS"', '"Linux"', '"Android"'])
    
    header_order = list(headers.items())
    random.shuffle(header_order)
    
    return dict(header_order)

def ngl_spam_loading(stop_event, completed_ref, total):

    WARNA = [
        "\033[1;91m",
        "\033[1;93m",
        "\033[1;92m",
        "\033[1;94m",
    ]

    RESET = "\033[0m"

    length = 10
    color_index = 0

    while not stop_event.is_set():

        for i in range(length + 1):

            if stop_event.is_set():
                break

            filled_color = (
                WARNA[color_index % len(WARNA)]
                + "■" * i
                + RESET
            )

            empty = "□" * (length - i)

            sys.stdout.write(
                f"\r {h}# {p}Sedang Menyerang Username NGL [[{filled_color}{empty}{p}]]"
            )

            sys.stdout.flush()

            time.sleep(0.05)

            color_index += 1

    sys.stdout.write("\r" + " " * 120 + "\r")
    sys.stdout.flush()

def ngl_spam_send_pesan(username, message, proxy_list, session, task_number):
    url = "https://ngl.link/api/submit"
    
    user_agents = ngl_spam_ua()
    user_agent = random.choice(user_agents)
    
    headers = ngl_spam_header(user_agent, username)
    
    randomized_message = ngl_spam_pesan_random(message)
    
    payload_fields = [
        ("username", username),
        ("question", randomized_message),
        ("deviceId", ngl_spam_devid()),
        ("gameSlug", ""),
        ("referrer", ""),
    ]
    
    random.shuffle(payload_fields)
    payload = dict(payload_fields)
    
    proxy = random.choice(proxy_list)
    proxies = {
        "http": proxy,
        "https": proxy
    }
    
    try:
        response = session.post(
            url, 
            headers=headers, 
            json=payload, 
            proxies=proxies,
            timeout=10
        )
        
        if response.status_code == 200:
            return (task_number, True)
            
    except:
        try:
            response = session.post(
                url, 
                headers=headers, 
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return (task_number, True)
        except:
            pass
    
    return (task_number, False)

def ngl_spam_main():
    print(f"""
{a}╭─────────────────────────────────────────────────────────────╮
│ {p}Masukkan Username NGL Target Tanpa "{h}@{p}". Contoh{m}:{h} MyTarget123 {a}│
╰── ╭─ {m}[{p} N G L {m}]{a} ─────────────────────────────────────────────╯""")
    
    username = input(f"    {a}╰──{h}➤{p} ").strip()
    
    if not username:
        input(f"\n{p} [{m}!{p}]{p} Username Ga Boleh Kosong{m} | {h} ENTER {r}")
        return
    
    jumlah = 30
    threads = 10
    
    confirm = input(f"\n {p}[{h}+{p}]{p} Silahkan {h}ENTER{r} {p}Atau Ketik {h}N{r} {p}Untuk Membatalkan{m} :{p} ").strip().lower()
    
    if confirm == 'n':
        return
    
    proxy_list = ngl_spam_proxy()
    
    sukses = 0
    gagal = 0
    lock = threading.Lock()
    completed = 0
    completed_ref = [0]
    stop_loading = threading.Event()
    
    def ngl_spam_worker(task_num):
        nonlocal sukses, gagal, completed
        
        random_messages = ngl_spam_pesan_acak()
        current_message = random.choice(random_messages)
        
        session = requests.Session()
        task_number, result = ngl_spam_send_pesan(
            username, current_message, proxy_list, session, task_num
        )
        
        with lock:
            completed += 1
            completed_ref[0] = completed
            if result:
                sukses += 1
            else:
                gagal += 1
    
    print()
   
    loading_thread = threading.Thread(target=ngl_spam_loading, args=(stop_loading, completed_ref, jumlah))
    loading_thread.daemon = True
    loading_thread.start()
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(ngl_spam_worker, i) for i in range(1, jumlah + 1)]
        
        for future in as_completed(futures):
            future.result()
    
    end_time = time.time()
    elapsed = end_time - start_time

    stop_loading.set()
    loading_thread.join()

    jarak_sukses = " " * (7 - len(str(sukses)))
    jarak_gagal = " " * (7 - len(str(gagal)))

    h_cursor()
    print(f"""{a}╭─────────────────────────────────────────────────────────────╮
│{p} Proses Pengiriman Selesai {m}|{p} Sukses{m}:{h} {sukses}{jarak_sukses} {m}|{p} Gagal{m}:{h} {gagal}{jarak_gagal}{a}│
╰─────────────────────────────────────────────────────────────╯""")
    input(
        f"{a}\n╭─────────────────────────────────────────────────────────────╮\n"
        f"│ \033[101m     {r}{h}          >> {p}ENTER FOR BACK TO MENU{h} <<           \033[101m     {r} {a}│\n"
        f"╰─────────────────────────────────────────────────────────────╯\n"
    )
    s_cursor()