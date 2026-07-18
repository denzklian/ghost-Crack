import requests
import json

def search_nik_by_phone(phone_number):
    """
    Mencari NIK berdasarkan nomor telepon menggunakan API leak-x68k
    
    Args:
        phone_number (str): Nomor telepon yang akan dicari (dengan atau tanpa 62)
    
    Returns:
        dict: Hasil pencarian atau pesan error
    """
    # Bersihkan nomor telepon
    phone = str(phone_number).strip()
    # Hapus '+' jika ada
    if phone.startswith('+'):
        phone = phone[1:]
    # Pastikan menggunakan kode negara 62
    if not phone.startswith('62'):
        phone = '62' + phone
    
    # URL API dengan parameter q
    url = f"https://api-leak-x68k.vercel.app/search?q={phone}"
    
    try:
        # Kirim request GET
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception untuk status HTTP error
        
        # Parse JSON response
        data = response.json()
        
        # Cek status response
        if data.get('status') == True:
            return {
                'success': True,
                'data': data.get('data', {}),
                'message': 'Data ditemukan'
            }
        else:
            return {
                'success': False,
                'message': data.get('message', 'Data tidak ditemukan'),
                'data': None
            }
            
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'message': 'Timeout: Server tidak merespons',
            'data': None
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'message': 'Gagal terhubung ke server',
            'data': None
        }
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'message': f'HTTP Error: {e}',
            'data': None
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'message': 'Respons tidak valid dari server',
            'data': None
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}',
            'data': None
        }

def main():
    """
    Fungsi utama untuk menjalankan script
    """
    print("="*50)
    print("PENCARIAN NIK BERDASARKAN NOMOR TELEPON")
    print("="*50)
    print("Catatan: Gunakan dengan bijak dan patuhi aturan privasi")
    print("-"*50)
    
    while True:
        # Input nomor telepon
        phone = input("\nMasukkan nomor telepon (atau 'quit' untuk keluar): ").strip()
        
        if phone.lower() == 'quit':
            print("Terima kasih telah menggunakan script ini.")
            break
        
        if not phone:
            print("❌ Nomor telepon tidak boleh kosong!")
            continue
        
        # Panggil fungsi pencarian
        print(f"\n🔍 Mencari data untuk nomor: {phone}...")
        result = search_nik_by_phone(phone)
        
        # Tampilkan hasil
        if result['success']:
            print("\n✅ DATA DITEMUKAN!")
            print("-"*50)
            data = result['data']
            # Tampilkan data dengan format rapi
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"{key}: {value}")
            else:
                print(data)
            print("-"*50)
        else:
            print(f"\n❌ {result['message']}")
        
        # Tanya apakah mau lanjut
        again = input("\nCari lagi? (y/n): ").strip().lower()
        if again != 'y':
            print("Terima kasih telah menggunakan script ini.")
            break
def leaktol():
        main()