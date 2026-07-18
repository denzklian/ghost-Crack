import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============ DAFTAR 100+ PLATFORM ============
PLATFORMS = {
    # Sosial Media Utama
    "Instagram": "https://www.instagram.com/{username}",
    "Twitter/X": "https://twitter.com/{username}",
    "Facebook": "https://www.facebook.com/{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "YouTube": "https://www.youtube.com/@{username}",
    "Snapchat": "https://www.snapchat.com/add/{username}",
    "Pinterest": "https://www.pinterest.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "Tumblr": "https://{username}.tumblr.com",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
    "Threads": "https://www.threads.net/@{username}",
    "Bluesky": "https://bsky.app/profile/{username}",
    "Mastodon": "https://mastodon.social/@{username}",
    
    # Messaging & Chat
    "Telegram": "https://t.me/{username}",
    "WhatsApp": "https://wa.me/{username}",
    "Signal": "https://signal.me/#p/{username}",
    "Discord": "https://discord.com/users/{username}",
    "Slack": "https://{username}.slack.com",
    "Line": "https://line.me/ti/p/@{username}",
    "WeChat": "https://www.wechat.com/{username}",
    "KakaoTalk": "https://story.kakao.com/{username}",
    "Viber": "https://chats.viber.com/{username}",
    
    # Gaming
    "Steam": "https://steamcommunity.com/id/{username}",
    "Xbox": "https://xboxgamertag.com/search/{username}",
    "PlayStation": "https://psnprofiles.com/{username}",
    "Nintendo": "https://nintendo.com/@{username}",
    "Epic Games": "https://www.epicgames.com/id/{username}",
    "Battle.net": "https://www.battle.net/{username}",
    "Riot Games": "https://www.riotgames.com/{username}",
    "Roblox": "https://www.roblox.com/user.aspx?username={username}",
    "Minecraft": "https://namemc.com/profile/{username}",
    "Twitch": "https://www.twitch.tv/{username}",
    "Kick": "https://kick.com/{username}",
    "Rumble": "https://rumble.com/user/{username}",
    "DLive": "https://dlive.tv/{username}",
    
    # Music & Audio
    "Spotify": "https://open.spotify.com/user/{username}",
    "SoundCloud": "https://soundcloud.com/{username}",
    "Apple Music": "https://music.apple.com/profile/{username}",
    "Deezer": "https://www.deezer.com/profile/{username}",
    "Tidal": "https://tidal.com/browse/users/{username}",
    "Bandcamp": "https://bandcamp.com/{username}",
    "Mixcloud": "https://www.mixcloud.com/{username}",
    "Audiomack": "https://audiomack.com/{username}",
    "Genius": "https://genius.com/{username}",
    
    # Video & Streaming
    "Vimeo": "https://vimeo.com/{username}",
    "Dailymotion": "https://www.dailymotion.com/{username}",
    "Bilibili": "https://space.bilibili.com/{username}",
    "VK Video": "https://vk.com/video/@{username}",
    "Odysee": "https://odysee.com/@{username}",
    
    # Programming & Tech
    "GitHub": "https://github.com/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Bitbucket": "https://bitbucket.org/{username}",
    "Stack Overflow": "https://stackoverflow.com/users/{username}",
    "HackerRank": "https://www.hackerrank.com/{username}",
    "LeetCode": "https://leetcode.com/{username}",
    "Codeforces": "https://codeforces.com/profile/{username}",
    "Dev.to": "https://dev.to/{username}",
    "Medium": "https://medium.com/@{username}",
    "Hashnode": "https://hashnode.com/@{username}",
    "Kaggle": "https://www.kaggle.com/{username}",
    
    # Blog & Writing
    "WordPress": "https://{username}.wordpress.com",
    "Blogger": "https://www.blogger.com/profile/{username}",
    "Ghost": "https://{username}.ghost.io",
    "Substack": "https://{username}.substack.com",
    "Wattpad": "https://www.wattpad.com/user/{username}",
    "Quotev": "https://www.quotev.com/{username}",
    "FanFiction": "https://www.fanfiction.net/u/{username}",
    "Archive of Our Own": "https://archiveofourown.org/users/{username}",
    
    # Photography & Art
    "Flickr": "https://www.flickr.com/people/{username}",
    "500px": "https://500px.com/p/{username}",
    "DeviantArt": "https://www.deviantart.com/{username}",
    "ArtStation": "https://www.artstation.com/{username}",
    "Behance": "https://www.behance.net/{username}",
    "Dribbble": "https://dribbble.com/{username}",
    "Unsplash": "https://unsplash.com/@{username}",
    "Pexels": "https://www.pexels.com/@{username}",
    
    # Dating & Social
    "Tinder": "https://www.tinder.com/@{username}",
    "Bumble": "https://bumble.com/@{username}",
    "OKCupid": "https://www.okcupid.com/profile/{username}",
    "Hinge": "https://hinge.com/@{username}",
    "Plenty of Fish": "https://www.pof.com/{username}",
    
    # Professional & Business
    "AngelList": "https://angel.co/u/{username}",
    "Crunchbase": "https://www.crunchbase.com/person/{username}",
    "Product Hunt": "https://www.producthunt.com/@{username}",
    "Fiverr": "https://www.fiverr.com/{username}",
    "Upwork": "https://www.upwork.com/freelancers/{username}",
    "Freelancer": "https://www.freelancer.com/u/{username}",
    
    # Forum & Community
    "Quora": "https://www.quora.com/profile/{username}",
    "StackExchange": "https://stackexchange.com/users/{username}",
    "ResearchGate": "https://www.researchgate.net/profile/{username}",
    "Academia.edu": "https://independent.academia.edu/{username}",
    "Couchsurfing": "https://www.couchsurfing.com/people/{username}",
    "Meetup": "https://www.meetup.com/members/{username}",
    
    # News & Bookmark
    "Pocket": "https://getpocket.com/@{username}",
    "Instapaper": "https://www.instapaper.com/p/{username}",
    "Digg": "https://digg.com/@{username}",
    "News.yc": "https://news.ycombinator.com/user?id={username}",
    
    # Lainnya
    "Patreon": "https://www.patreon.com/{username}",
    "OnlyFans": "https://onlyfans.com/{username}",
    "Linktree": "https://linktr.ee/{username}",
    "Beacons": "https://beacons.ai/{username}",
    "Carrd": "https://{username}.carrd.co",
    "About.me": "https://about.me/{username}",
    "Keybase": "https://keybase.io/{username}",
    "Gravatar": "https://en.gravatar.com/{username}",
    "Disqus": "https://disqus.com/by/{username}",
    
    # Regional (Asia)
    "Weibo": "https://weibo.com/u/{username}",
    "Douyin": "https://www.douyin.com/user/{username}",
    "Kuaishou": "https://www.kuaishou.com/profile/{username}",
    "Xiaohongshu": "https://www.xiaohongshu.com/user/profile/{username}",
    "Zhihu": "https://www.zhihu.com/people/{username}",
    "Naver": "https://blog.naver.com/{username}",
    "Daum": "https://blog.daum.net/{username}",
    
    # Dark Web (Public onion sites - hanya contoh)
    # "Facebook Onion": "https://www.facebookcorewwwi.onion/{username}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ============ FUNGSI UTAMA ============

def check_platform(platform, url_template, username):
    """Cek apakah username ada di platform tertentu"""
    url = url_template.format(username=username)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=False)
        
        if response.status_code == 200:
            return (platform, url, "✅", "Ditemukan")
        elif response.status_code == 404:
            return (platform, url, "❌", "Tidak ditemukan")
        elif response.status_code in [301, 302, 303, 307, 308]:
            # Cek redirect ke halaman profile
            if "profile" in response.headers.get("Location", "").lower() or "user" in response.headers.get("Location", "").lower():
                return (platform, url, "✅", "Ditemukan (redirect)")
            return (platform, url, "↗️", f"Redirect {response.status_code}")
        elif response.status_code == 403:
            return (platform, url, "🚫", "Diblokir/Private")
        elif response.status_code == 429:
            return (platform, url, "⏳", "Rate limited")
        else:
            return (platform, url, "⚠️", f"Status {response.status_code}")
            
    except requests.exceptions.Timeout:
        return (platform, url, "⏰", "Timeout")
    except requests.exceptions.ConnectionError:
        return (platform, url, "🔌", "Gagal konek")
    except requests.exceptions.SSLError:
        return (platform, url, "🔒", "SSL Error")
    except Exception as e:
        return (platform, url, "❌", f"Error: {str(e)[:35]}")

def search_all_platforms(username, max_workers=20):
    """Cari username di semua platform secara paralel"""
    print(f"\n🔍 Mencari username: {username}")
    print(f"📊 Total platform: {len(PLATFORMS)}")
    print("="*70)
    
    results = []
    found_count = 0
    total_checked = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(check_platform, platform, url, username): platform 
            for platform, url in PLATFORMS.items()
        }
        
        for future in as_completed(futures):
            platform, url, icon, status = future.result()
            results.append((platform, url, icon, status))
            total_checked += 1
            
            if icon == "✅":
                found_count += 1
            
            print(f"{icon} [{found_count}] {platform:20} | {status:15} → {url}")
    
    return results, found_count

def search_by_email(email):
    """Cari berdasarkan email"""
    print(f"\n📧 Mencari berdasarkan email: {email}")
    username = email.split('@')[0]
    print(f"🔑 Username yang dicoba: {username}")
    print("-"*70)
    return search_all_platforms(username)

def save_results(username, results, found_count):
    """Simpan hasil ke file"""
    filename = f"osint_result_{username}_{int(time.time())}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"HASIL OSINT - {username}\n")
        f.write(f"Total platform: {len(results)}\n")
        f.write(f"Username ditemukan di: {found_count} platform\n")
        f.write("="*70 + "\n\n")
        
        for platform, url, icon, status in sorted(results, key=lambda x: x[2], reverse=True):
            if icon == "✅":
                f.write(f"[✓] {platform:25} → {url}\n")
            elif icon in ["❌", "🚫", "⏰", "🔌"]:
                f.write(f"[ ] {platform:25} → {status}\n")
            else:
                f.write(f"[?] {platform:25} → {status}\n")
    
    print(f"\n💾 Hasil disimpan ke: {filename}")
    return filename

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                GHOST OSINT USERNAME TOOL                  ║
    ║                       CRRATE BY D3NZ                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n" + "─"*70)
        print("📋 MENU UTAMA:")
        print("  1. Cari berdasarkan Username")
        print("  2. Cari berdasarkan Email")
        print("  3. Cari Username dari List (Bulk)")
        print("  4. Lihat daftar platform")
        print("  5. Keluar")
        
        choice = input("\n👉 Pilihan (1-5): ").strip()
        
        if choice == "1":
            username = input("Masukkan username: ").strip()
            if username:
                start = time.time()
                results, found_count = search_all_platforms(username)
                elapsed = time.time() - start
                
                print("\n" + "="*70)
                print(f"📊 RINGKASAN:")
                print(f"  ✅ Ditemukan di: {found_count} platform")
                print(f"  ❌ Tidak ditemukan: {len(results) - found_count} platform")
                print(f"  ⏱️ Waktu: {elapsed:.2f} detik")
                
                save = input("\n💾 Simpan hasil ke file? (y/n): ").lower()
                if save == 'y':
                    save_results(username, results, found_count)
        
        elif choice == "2":
            email = input("Masukkan email: ").strip()
            if email and '@' in email:
                start = time.time()
                results, found_count = search_by_email(email)
                elapsed = time.time() - start
                
                print("\n" + "="*70)
                print(f"📊 RINGKASAN:")
                print(f"  ✅ Ditemukan di: {found_count} platform")
                print(f"  ❌ Tidak ditemukan: {len(results) - found_count} platform")
                print(f"  ⏱️ Waktu: {elapsed:.2f} detik")
                
                save = input("\n💾 Simpan hasil ke file? (y/n): ").lower()
                if save == 'y':
                    save_results(email.split('@')[0], results, found_count)
        
        elif choice == "3":
            print("📝 Masukkan username satu per satu (kosongkan untuk selesai):")
            usernames = []
            while True:
                u = input("  Username: ").strip()
                if not u:
                    break
                usernames.append(u)
            
            if usernames:
                print(f"\n🔍 Mencari {len(usernames)} username...")
                all_results = {}
                for username in usernames:
                    print(f"\n{'─'*70}")
                    results, found_count = search_all_platforms(username)
                    all_results[username] = (results, found_count)
                
                # Tampilkan ringkasan
                print("\n" + "="*70)
                print("📊 RINGKASAN BULK SEARCH:")
                for username, (_, found_count) in all_results.items():
                    print(f"  {username}: ditemukan di {found_count} platform")
        
        elif choice == "4":
            print("\n📋 DAFTAR PLATFORM:")
            print("="*70)
            for i, platform in enumerate(sorted(PLATFORMS.keys()), 1):
                print(f"{i:3}. {platform}")
            print(f"\nTotal: {len(PLATFORMS)} platform")
        
        elif choice == "5":
            print("\n👋 Sampai jumpa! Tetap gunakan untuk tujuan etis ya! 😊")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan coba lagi.")

def osint():
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proses dihentikan oleh user. Sampai jumpa!")
    except Exception as e:
        print(f"\n❌ Terjadi error: {e}")
