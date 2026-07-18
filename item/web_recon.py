#!/usr/bin/env python3
import socket
import requests
import json
import re
import concurrent.futures
import threading
import ssl
import http.client

# ===== DEFINISI WARNA =====
R = "\033[1;41m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
M = "\033[1;35m"
W = "\033[0m"
# =========================

def recon():
    def banner():
        print(f"""{R}
    ╔══════════════════════════════════════════════════════╗
    ║           GHOST-TRACK Ω - REAL RECON v10.0           ║
    ║              ULTRA BRUTAL REAL SHIT!                 ║
    ╚══════════════════════════════════════════════════════╝{W}""")
    
    banner()
    
    target = input(f"{Y}Target (contoh: tesla.com) » {W}").strip().lower()
    domain = target.replace("http://","").replace("https://","").split("/")[0]
    print(f"\n{G}Locking → {domain}{W}")

    # Resolve IP
    try:
        ip = socket.gethostbyname(domain)
        print(f"{G}IP → {ip}{W}")
    except:
        print(f"{R}Domain ga ketemu bro!{W}")
        return

    found = {"subs":[], "leaks":[], "git":[], "env":[], "backup":[], "phpinfo":[], "emails":[], "keys":[], "ports":[], "tech":[], "headers":[]}
    lock = threading.Lock()

    # SUBDOMAIN BRUTEFORCE
    def subdomain_bruteforce():
        print(f"\n{Y}[+] SUBDOMAIN BRUTEFORCE - GAS POL!{W}")
        subs_brute = [
            "admin", "api", "dev", "test", "staging", "beta", "vpn", "mail", "ftp", 
            "cpanel", "git", "jenkins", "kibana", "blog", "shop", "store", "app",
            "dashboard", "portal", "secure", "auth", "login", "adminpanel",
            "backend", "phpmyadmin", "mysql", "db", "database", "old", "new",
            "temp", "tmp", "backup", "archive", "legacy", "classic", "v1", "v2",
            "api1", "api2", "mobile", "m", "wap", "www1", "www2", "cdn", "static",
            "media", "images", "img", "video", "cdn1", "cdn2", "assets", "files",
            "download", "upload", "secure", "ssl", "webmail", "email", "smtp",
            "pop", "imap", "ns1", "ns2", "dns", "ssh", "ftp", "sftp", "crm", "erp"
        ]
        
        apis = [
            f"https://api.hackertarget.com/hostsearch/?q={domain}",
            f"https://crt.sh/?q=%.{domain}&output=json",
        ]
        
        for api in apis:
            try:
                r = requests.get(api, timeout=10)
                if r.status_code == 200:
                    if "hackertarget" in api:
                        for line in r.text.splitlines():
                            sub = line.split(",")[0].strip()
                            if sub and domain in sub:
                                found["subs"].append(sub)
                    elif "crt.sh" in api:
                        try:
                            data = json.loads(r.text)
                            for cert in data:
                                name = cert.get('name_value', '')
                                if domain in name:
                                    found["subs"].extend(name.splitlines())
                        except: pass
            except: pass
        
        def check_subdomain(sub):
            try:
                socket.gethostbyname(sub)
                with lock:
                    if sub not in found["subs"]:
                        found["subs"].append(sub)
                        print(f"{G}[+] Subdomain → {sub}{W}")
            except: pass
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exe:
            for word in subs_brute:
                for prefix in ["", "api-", "dev-", "test-", "staging-", "admin-"]:
                    sub = f"{prefix}{word}.{domain}"
                    exe.submit(check_subdomain, sub)

    # PORT SCANNING
    def port_scan():
        print(f"\n{Y}[+] PORT SCANNING - NYARI BACKDOOR!{W}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 2082, 2083, 2086, 2087, 2095, 2096, 3306, 3389, 5432, 8080, 8443]
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    with lock:
                        found["ports"].append(port)
                        print(f"{G}[+] Port {port} → OPEN{W}")
                sock.close()
            except: pass
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as exe:
            exe.map(scan_port, common_ports)

    # TECHNOLOGY DETECTION
    def tech_detection(host):
        try:
            ctx = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(host, timeout=10, context=ctx)
            conn.request("GET", "/", headers={"User-Agent": "Mozilla/5.0"})
            r = conn.getresponse()
            headers = dict(r.getheaders())
            body = r.read(50000).decode(errors='ignore')
            
            tech_stack = []
            if "server" in headers:
                tech_stack.append(headers["server"])
                print(f"{C}[+] Server → {headers['server']}{W}")
            
            if "x-powered-by" in headers:
                tech_stack.append(headers["x-powered-by"])
                print(f"{C}[+] Powered By → {headers['x-powered-by']}{W}")
            
            if "wp-content" in body or "wordpress" in body:
                tech_stack.append("WordPress")
                print(f"{M}[+] Tech → WordPress{W}")
            elif "laravel" in body.lower():
                tech_stack.append("Laravel") 
                print(f"{M}[+] Tech → Laravel{W}")
            elif "react" in body or "next" in body:
                tech_stack.append("React/Next.js")
                print(f"{M}[+] Tech → React/Next.js{W}")
            
            with lock:
                found["tech"].extend(tech_stack)
                found["headers"].append({host: headers})
                
        except: pass

    # REAL LEAK PATHS
    real_paths = [
        "/.env", "/.env.bak", "/.env.prod", "/.env.local", "/.env.dev",
        "/.git/HEAD", "/.git/config", "/.git/logs/HEAD", "/.git/description",
        "/backup.sql", "/db_backup.sql", "/database.sql", "/dump.sql", "/backup.zip",
        "/phpinfo.php", "/info.php", "/test.php", "/debug.php", "/admin.php",
        "/admin/.env", "/laravel/.env", "/config/.env", "/app/.env",
        "/wp-config.php.bak", "/backup/wp-config.php", "/wp-config.php",
        "/robots.txt", "/sitemap.xml", "/web.config", "/.htaccess",
        "/config.json", "/config.js", "/settings.py", "/.dockerignore",
        "/docker-compose.yml", "/.travis.yml", "/.github/workflows",
        "/.aws/credentials", "/.npmrc", "/.yarnrc", "/composer.json",
        "/package.json", "/.bash_history", "/.ssh/id_rsa", "/.ssh/config"
    ]

    def deep_probe(host, path):
        try:
            ctx = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(host, timeout=10, context=ctx)
            conn.request("GET", path, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            r = conn.getresponse()
            if r.status in [200,301,302,403]:
                data = r.read(1024000).decode(errors="ignore")
                url = f"https://{host}{path}"

                if ".env" in path and any(x in data for x in ["DB_PASSWORD", "APP_KEY", "JWT_SECRET", "API_KEY", "SECRET_KEY"]):
                    with lock:
                        found["env"].append(url)
                        print(f"{R}[!] ENV LEAKED → {url}{W}")
                        for line in data.splitlines()[:20]:
                            if "=" in line and not line.startswith("#"):
                                key, val = line.split("=",1)
                                if any(x in key.upper() for x in ["PASS","KEY","SECRET","TOKEN","API","AUTH"]):
                                    print(f"   {M}{key.strip()} = {val.strip()}{W}")

                elif ".git" in path and ("ref:" in data or "[core]" in data):
                    with lock:
                        found["git"].append(url)
                        print(f"{R}[!] GIT EXPOSED → {url}{W}")
                        if "ref:" in data:
                            print(f"   {Y}Branch → {data.split('ref:')[1].strip()[:60]}{W}")

                elif any(x in path for x in ["sql","dump","backup","zip","tar"]):
                    if "INSERT INTO" in data or "CREATE TABLE" in data or "PK" in data[:100]:
                        with lock:
                            found["backup"].append(url)
                            print(f"{R}[!] DATABASE DUMP → {url}{W}")
                    elif len(data) > 1000:
                        with lock:
                            found["backup"].append(url)
                            print(f"{B}[!] LARGE FILE → {url} ({len(data)} bytes){W}")

                elif "phpinfo" in path or "PHP Version" in data:
                    with lock:
                        found["phpinfo"].append(url)
                        print(f"{R}[!] PHPINFO → {url}{W}")

                elif any(x in path for x in ["config.json","settings.py","wp-config"]):
                    with lock:
                        found["leaks"].append(url)
                        print(f"{R}[!] CONFIG FILE → {url}{W}")

                emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", data)
                keys = re.findall(r"sk_live_[a-zA-Z0-9]{20,50}|[A-Za-z0-9+/]{40,}={0,2}", data)
                
                if emails: 
                    with lock:
                        found["emails"].extend(emails)
                        for email in emails[:3]:
                            print(f"{C}[+] Email → {email}{W}")
                if keys:
                    with lock:
                        found["keys"].extend(keys)
                        for key in keys[:2]:
                            print(f"{M}[!] Potential Key → {key[:50]}...{W}")

        except: pass

    # WAYBACK MACHINE
    def wayback_urls():
        print(f"\n{Y}[+] CHECKING WAYBACK MACHINE - ARCHIVE MODE!{W}")
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                urls = json.loads(r.text)
                for url in urls[1:20]:
                    print(f"{B}[+] Archive → {url[0][:80]}...{W}")
        except: pass

    # ====== EKSEKUSI ======
    print(f"\n{R}REAL RECON DIMULAI - BRUTAL MODE ON!{W}")

    subdomain_bruteforce()
    port_scan()
    tech_detection(domain)
    wayback_urls()

    print(f"\n{R}[+] REAL LEAK HUNTING DIMULAI - BUKAN CUMA 200 DOANG!{W}\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as exe:
        for host in list(set(found["subs"]))[:80]:
            for path in real_paths:
                exe.submit(deep_probe, host, path)
            exe.submit(tech_detection, host)

    # FINAL REPORT
    print(f"\n{R}╔══════════════════════════════════════════════════════╗")
    print(f"║                   REAL RECON SELESAI                 ║")
    print(f"╚══════════════════════════════════════════════════════╝{W}")

    print(f"{G}Subdomains   → {len(set(found['subs']))}{W}")
    print(f"{G}Open Ports   → {len(found['ports'])} → {found['ports']}{W}")
    print(f"{R}ENV Leaked   → {len(found['env'])}{W}")
    print(f"{R}Git Exposed  → {len(found['git'])}{W}")
    print(f"{R}SQL Dump     → {len(found['backup'])}{W}")
    print(f"{R}PHPInfo      → {len(found['phpinfo'])}{W}")
    print(f"{C}Emails Found → {len(set(found['emails']))}{W}")
    print(f"{M}API Keys     → {len(set(found['keys']))}{W}")
    print(f"{Y}Tech Stack   → {list(set(found['tech']))[:5]}{W}")

    if found["env"] or found["git"] or found["backup"]:
        print(f"\n{M}LANGSUNG GAS BRO — INI BENERAN LEAK NYATA!{W}")
        for leak in found["env"][:3]: 
            print(f"   {R}ENV → {leak}{W}")
        for leak in found["git"][:3]: 
            print(f"   {R}GIT → {leak}{W}")
        for leak in found["backup"][:3]: 
            print(f"   {R}SQL → {leak}{W}")
            
        print(f"\n{Y}petrus x d3nz — real recon, real leak, real anjir{W}")
    
    print(f"{R}3113 OUT ☠️ ULTRA BRUTAL MODE!{W}\n")