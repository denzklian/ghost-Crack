import hmac
import hashlib
import time
import base64
import json
import requests
import sys
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Konfigurasi
HMAC_SECRET = "8d3f2f7f5a7e4c9f2e1d8b6c4a9f7e5d3c2b1a8f6e4d9c7b5a3f1e8d6c4b2a9"
AES_KEY = "7f4c9a2d8e1b6f3a5c7d9e0f2a4b6c8d1e3f5a7b9c0d2e4f6a8b1c3d5e7f9a2".encode()[:32].ljust(32, b'\0')

# Warna ANSI untuk terminal
class Colors:
    PURPLE = '\033[95m'
    PURPLE_BRIGHT = '\033[94m'
    GREEN = '\033[92m'
    GREEN_BRIGHT = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class EWalletCheckerCLI:
    def __init__(self):
        self.clear_screen()
        self.show_banner()
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        banner = f"""
{Colors.PURPLE_BRIGHT}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║               🔐  {Colors.WHITE}E-WALLET CHECKER {Colors.PURPLE_BRIGHT}v2.0                  ║
║               {Colors.GREEN}🟢  Auto Request & Enkripsi {Colors.PURPLE_BRIGHT}               ║
║               {Colors.CYAN}  Report bug: t.me/denzkucai{Colors.PURPLE_BRIGHT}               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
    
    def show_loading_bar(self, progress, total=100, width=50):
        """Menampilkan loading bar dengan warna ungu dan hijau"""
        percent = int((progress / total) * 100)
        filled = int(width * progress / total)
        bar = f"{Colors.PURPLE_BRIGHT}{'█' * filled}{Colors.GREEN}{'░' * (width - filled)}{Colors.END}"
        
        # Warna progress berubah sesuai persentase
        if percent < 30:
            color = Colors.RED
        elif percent < 70:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN_BRIGHT
            
        sys.stdout.write(f'\r{Colors.BOLD}Progress:{Colors.END} {bar} {color}{percent}%{Colors.END}')
        sys.stdout.flush()
    
    def aes_encrypt(self, plaintext: str) -> str:
        iv = get_random_bytes(16)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ct).decode()
    
    def make_signed_request(self, phone_number: str):
        try:
            # Step 1: Enkripsi
            print(f"\n{Colors.PURPLE}🔒 Mengenkripsi nomor...{Colors.END}")
            self.show_loading_bar(20)
            encrypted_phone = self.aes_encrypt(phone_number)
            
            # Step 2: Prepare body
            body = {"phone_number": encrypted_phone}
            raw_body = json.dumps(body, separators=(",", ":"))
            timestamp = str(int(time.time()))
            message = timestamp + raw_body
            
            # Step 3: Generate signature
            print(f"\n{Colors.PURPLE}🔑 Generate signature...{Colors.END}")
            self.show_loading_bar(40)
            signature = hmac.new(
                HMAC_SECRET.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Step 4: Send request
            print(f"\n{Colors.PURPLE}📡 Mengirim request ke server...{Colors.END}")
            self.show_loading_bar(60)
            
            response = requests.post(
                "https://topupelitt.ddns.net/api/check-ewallet2",
                data=raw_body,
                headers={
                    "Content-Type": "application/json",
                    "X-Signature": signature,
                    "X-Timestamp": timestamp,
                },
                timeout=30
            )
            
            # Step 5: Process response
            print(f"\n{Colors.PURPLE}📊 Memproses response...{Colors.END}")
            self.show_loading_bar(80)
            
            result = response.json()
            
            # Step 6: Complete
            self.show_loading_bar(100)
            print(f"\n{Colors.GREEN_BRIGHT}✅ Selesai!{Colors.END}\n")
            
            return result
            
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "⏱️ Timeout - Server tidak merespons"}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": "🔌 Gagal terhubung ke server"}
        except Exception as e:
            return {"status": "error", "message": f"❌ {str(e)}"}
    
    def format_result(self, data):
        """Format hasil dengan warna-warna menarik"""
        print(f"\n{Colors.BOLD}{Colors.GREEN_BRIGHT}╔══════════════════════════════════════════════════════════╗")
        print(f"║                     📋 HASIL RESPONSE                    ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        if isinstance(data, dict):
            status = data.get('status', 'unknown')
            
            # Status dengan warna
            if status == 'success':
                status_color = Colors.GREEN_BRIGHT
                status_icon = '✅'
            elif status == 'error':
                status_color = Colors.RED
                status_icon = '❌'
            else:
                status_color = Colors.YELLOW
                status_icon = '⚠️'
            
            print(f"{Colors.BOLD}Status:{Colors.END} {status_color}{status_icon} {status.upper()}{Colors.END}")
            
            # Tampilkan message
            if 'message' in data:
                print(f"{Colors.BOLD}Message:{Colors.END} {Colors.CYAN}{data['message']}{Colors.END}")
            
            # Tampilkan data jika ada
            if 'data' in data and data['data']:
                print(f"\n{Colors.BOLD}{Colors.PURPLE_BRIGHT}📱 DATA DETAIL:{Colors.END}")
                print(f"{Colors.BOLD}{'─' * 50}{Colors.END}")
                
                phone_data = data['data']
                
                # Phone number - tampilkan dalam format 08
                if 'phone_number' in phone_data:
                    phone_display = phone_data['phone_number']
                    # Jika response masih 62, konversi ke 08 untuk tampilan
                    if phone_display.startswith('62'):
                        phone_display = '0' + phone_display[2:]
                    print(f"{Colors.GREEN}📞 Nomor:{Colors.END} {Colors.WHITE}{phone_display}{Colors.END}")
                
                # Provider
                if 'provider' in phone_data:
                    print(f"{Colors.GREEN}📡 Provider:{Colors.END} {Colors.WHITE}{phone_data['provider']}{Colors.END}")
                
                # E-wallet details
                if 'ewallet' in phone_data:
                    print(f"\n{Colors.BOLD}{Colors.PURPLE_BRIGHT}💳 E-WALLET:{Colors.END}")
                    
                    for wallet_name, wallet_data in phone_data['ewallet'].items():
                        registered = wallet_data.get('registered', False)
                        status_wallet = wallet_data.get('status', 'inactive')
                        balance = wallet_data.get('balance', 0)
                        
                        # Warna berdasarkan status
                        if registered and status_wallet == 'active':
                            icon = '🟢'
                            color = Colors.GREEN_BRIGHT
                        elif registered and status_wallet == 'inactive':
                            icon = '🟡'
                            color = Colors.YELLOW
                        else:
                            icon = '🔴'
                            color = Colors.RED
                        
                        print(f"  {icon} {Colors.BOLD}{wallet_name.upper()}{Colors.END}:")
                        print(f"    {Colors.GREEN}Registered:{Colors.END} {color}{registered}{Colors.END}")
                        if registered:
                            print(f"    {Colors.GREEN}Status:{Colors.END} {color}{status_wallet}{Colors.END}")
                            print(f"    {Colors.GREEN}Balance:{Colors.END} {Colors.WHITE}Rp {balance:,.0f}{Colors.END}")
                
                # Last check
                if 'last_check' in phone_data:
                    print(f"\n{Colors.GREEN}🕐 Last Check:{Colors.END} {Colors.WHITE}{phone_data['last_check']}{Colors.END}")
                
                # Request ID
                if 'request_id' in phone_data:
                    print(f"{Colors.GREEN}🆔 Request ID:{Colors.END} {Colors.WHITE}{phone_data['request_id']}{Colors.END}")
            
            # Tampilkan error code jika ada
            if 'error_code' in data:
                print(f"\n{Colors.RED}⚠️ Error Code:{Colors.END} {Colors.WHITE}{data['error_code']}{Colors.END}")
            
            # Tampilkan full JSON
            print(f"\n{Colors.BOLD}{Colors.PURPLE_BRIGHT}📄 FULL RESPONSE JSON:{Colors.END}")
            print(f"{Colors.BOLD}{'─' * 50}{Colors.END}")
            print(f"{Colors.CYAN}{json.dumps(data, indent=2, ensure_ascii=False)}{Colors.END}")
            
        else:
            print(f"{Colors.RED}❌ Format response tidak valid{Colors.END}")
    
    def run(self):
        while True:
            print(f"\n{Colors.BOLD}{Colors.PURPLE_BRIGHT}╔══════════════════════════════════════════════════════════╗")
            print(f"║           MASUKKAN NOMOR TELEPON YG MAU DI CEK           ║")
            print(f"║                   {Colors.GREEN}Contoh: 0853******* {Colors.PURPLE_BRIGHT}                   ║")
            print(f"║                     {Colors.CYAN}create by @d3nz{Colors.PURPLE_BRIGHT}                      ║")
            print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}")
            
            phone_input = input(f"\n{Colors.BOLD}{Colors.GREEN}➜{Colors.END} Nomor (08xxx): ").strip()
            
            # Validasi input
            if phone_input.lower() in ['exit', 'quit', 'q']:
                print(f"\n{Colors.PURPLE_BRIGHT}👋 Terima kasih! Sampai jumpa.{Colors.END}")
                break
            
            if not phone_input:
                print(f"{Colors.RED}⚠️ Nomor tidak boleh kosong!{Colors.END}")
                continue
            
            # Bersihkan nomor (hapus karakter non-digit)
            phone = ''.join(filter(str.isdigit, phone_input))
            
            if not phone:
                print(f"{Colors.RED}⚠️ Nomor harus berupa angka!{Colors.END}")
                continue
            
            # Validasi format 08
            if not phone.startswith('08'):
                print(f"{Colors.RED}⚠️ Nomor harus dimulai dengan 08!{Colors.END}")
                print(f"{Colors.YELLOW}💡 Contoh: 085389400823{Colors.END}")
                continue
            
            if len(phone) < 10 or len(phone) > 13:
                print(f"{Colors.RED}⚠️ Panjang nomor tidak valid (10-13 digit)!{Colors.END}")
                continue
            
            # Gunakan format 08 langsung (TIDAK dikonversi ke 62)
            phone_display = phone
            
            print(f"\n{Colors.GREEN}📱 Memproses nomor: {Colors.WHITE}{phone_display}{Colors.END}")
            print(f"{Colors.CYAN}📡 Format API: {Colors.WHITE}{phone_display}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.PURPLE_BRIGHT}{'═' * 60}{Colors.END}\n")
            
            # Proses request dengan format 08 (LANGSUNG)
            result = self.make_signed_request(phone_display)
            
            # Tampilkan hasil
            self.format_result(result)
            
            # Tanya apakah mau lanjut
            print(f"\n{Colors.BOLD}{Colors.PURPLE_BRIGHT}─{'─' * 58}{Colors.END}")
            again = input(f"\n{Colors.GREEN}🔄 Request lagi? (y/n): {Colors.END}").strip().lower()
            if again not in ['y', 'yes', '']:
                print(f"\n{Colors.PURPLE_BRIGHT}👋 Terima kasih! Sampai jumpa.{Colors.END}")
                break
            
            self.clear_screen()
            self.show_banner()

def ewalet():
    try:
        app = EWalletCheckerCLI()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.PURPLE_BRIGHT}👋 Program dihentikan. Sampai jumpa!{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        sys.exit(1)
