import requests
from bs4 import BeautifulSoup
import sys
import time
import threading
import re
import os
import random
    
a = "\033[1;30m"
m = "\033[1;31m"
h = "\033[1;32m"
k = "\033[1;33m"
c = "\033[1;36m"
p = "\033[1;37m"
r = "\033[0m"

class SfileSearcher:
    def __init__(self):
        self.base_url = 'https://sfile.mobi'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.loading = False
        self.loading_complete = False
        self.current_page = 0
        self.total_pages = 0

    def sfile_search_request(self, query, page=1):
        search_url = f'{self.base_url}/search.php'
        params = {
            'q': query,
            'search': 'Search',
            'page': page
        }
        
        try:
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            return self.sfile_search_parse(response.text, query)
        except Exception as e:
            return None

    def sfile_search_parse(self, html, query):
        soup = BeautifulSoup(html, 'html.parser')
        
        results = {
            'query': query,
            'total_results': 0,
            'current_page': 1,
            'total_pages': 0,
            'files': []
        }

        search_header = soup.find('div', {'class': 'w3-container w3-blue'})
        
        if search_header:
            h3_text = search_header.find('h3')
            if h3_text:
                text = h3_text.get_text()
                result_match = re.search(r'([\d,]+)\s+results?\s+for\s+"([^"]+)"', text)
                if result_match:
                    results['total_results'] = int(result_match.group(1).replace(',', ''))
                    results['query'] = result_match.group(2)
            
            p_text = search_header.find('p')
            if p_text:
                text = p_text.get_text()
                page_match = re.search(r'Page\s+(\d+)\s+of\s+(\d+)', text)
                if page_match:
                    results['current_page'] = int(page_match.group(1))
                    results['total_pages'] = int(page_match.group(2))

        lists = soup.find_all('div', {'class': 'list'})
        
        for element in lists:
            if element.find('form'):
                continue
            
            file_info = {}
            
            img = element.find('img')
            if img and img.get('alt'):
                file_info['type'] = img.get('alt')
            
            link = element.find('a')
            if link:
                file_info['name'] = link.get_text().strip()
                href = link.get('href')
                if href:
                    if not href.startswith('http'):
                        href = self.base_url + href
                    file_info['url'] = href
                    file_id = href.split('/')[-1]
                    file_info['file_id'] = file_id
            
            span = element.find('span', {'class': 'file-info'})
            if span:
                span_text = span.get_text()
                
                size_match = re.search(r'\(([\d.]+\s*(?:bytes|KB|MB|GB))\)', span_text)
                if size_match:
                    file_info['size'] = size_match.group(1)
                
                download_match = re.search(r'(\d+)\s+downloads?', span_text)
                if download_match:
                    file_info['downloads'] = int(download_match.group(1))
                else:
                    file_info['downloads'] = 0
            
            if 'name' in file_info and file_info['name']:
                results['files'].append(file_info)
        
        return results

    def sfile_search_loading_animation(self):
        speed = 0.1
        length = 20
        COLORS = [m, k, c, h]
        color_index = 0
        
        while self.loading:
            if self.total_pages > 0:
                progress = (self.current_page / self.total_pages)
                filled_length = int(length * progress)
                
                filled_color = COLORS[color_index % len(COLORS)] + "━" * filled_length + r
                empty = a + "━" * (length - filled_length) + r
                
                percentage = int(progress * 100)
                bar = f"{a}[{m}i{a}]{p} Proses Pencarian {r}{filled_color}{empty} {p}{percentage}%{r}"
                sys.stdout.write("\r" + bar)
                sys.stdout.flush()
                
                color_index += 1
            time.sleep(speed)
        
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        sys.stdout.flush()

    def sfile_search_all_pages(self, query, max_pages=None):
        all_files = []
        
        first_result = self.sfile_search_request(query, 1)
        
        if not first_result or not first_result['files']:
            return None
        
        total_pages = first_result['total_pages']
        if max_pages:
            total_pages = min(total_pages, max_pages)
        
        self.total_pages = total_pages
        self.current_page = 1
        all_files.extend(first_result['files'])
        
        print()
        self.loading = True
        loading_thread = threading.Thread(target=lambda: self.sfile_search_loading_animation())
        loading_thread.start()
        
        if total_pages > 1:
            for page in range(2, total_pages + 1):
                result = self.sfile_search_request(query, page)
                self.current_page = page
                
                if result and result['files']:
                    all_files.extend(result['files'])
                
                time.sleep(0.2)
        
        self.loading = False
        loading_thread.join()
        
        os.system("clear")
        self.sfile_search_banner()
        print(f"""
{a}[{m}⌬{a}]{p} Ditemukan {m}: {a}{first_result['total_results']} Data File
{a}[{m}⌬{a}]{p} Total Halaman {m}:{a} {total_pages}""")
        print()
        
        return {
            'query': query,
            'total_results': first_result['total_results'],
            'files': all_files
        }

    def sfile_search_display_chunk(self, files, start_idx):
        end_idx = min(start_idx + 15, len(files))
        for i in range(start_idx, end_idx):
            idx = i + 1
            file = files[i]
            name = file.get('name', 'N/A')
            url = file.get('url', 'N/A')
            size = file.get('size', 'N/A')
            file_type = file.get('type', 'N/A')
            downloads = file.get('downloads', 0)
            
            print(f"{a}┌─[ {p}PENCARIAN {idx}{a} ]")
            print(f"{a}│")
            print(f"{a}├─{m}➤ {p}Nama        {m}: {a}{name}")
            print(f"{a}├─{m}➤ {p}Url         {m}: {a}{url}")
            print(f"{a}├─{m}➤ {p}Ukuran      {m}: {a}{size}")
            print(f"{a}├─{m}➤ {p}Tipe        {m}: {a}{file_type}")
            print(f"{a}└─{m}➤ {p}Download    {m}: {a}{downloads}")
            if i < end_idx - 1:
                print()

    def sfile_search_show_menu(self, files, query):
        total = len(files)
        total_pages = (total + 14) // 15
        
        while True:
            os.system("clear")
            self.sfile_search_banner()
            print(f"{a}┌─[ {p}HASIL PENCARIAN {a}]{r}")
            print(f"{a}│{r}")
            
            for page in range(1, total_pages + 1):
                start = (page - 1) * 15 + 1
                end = min(page * 15, total)
                print(f"{a}├─{m}➤ {p}Pencarian Ke {m}- {p}{page:02d}")
            
            print(f"{a}└─{m}➤ {p}{total_pages + 1:02d} {m}- {p}Cari File Lain{r}")
            
            choice = input(f"\n{a}[{m}?{a}]{p} Pilih Hasil Pencarian {m}:{a} {r}")
            
            try:
                choice_num = int(choice)
                if choice_num == total_pages + 1:
                    break
                elif 1 <= choice_num <= total_pages:
                    os.system('clear')
                    self.sfile_search_banner()
                    print()
                    start_idx = (choice_num - 1) * 15
                    self.sfile_search_display_chunk(files, start_idx)
                    input(f"\n{a}[{m}!{a}]{p} Kembali Ke Menu Bagian Data {a}| \033[101m\033[1;32m ENTER \033[0m")
                    os.system('clear')
                    print()
                else:
                    input(f"{a}[{m}!{a}]{p} Pilihan Tidak Valid{m}!{a} | \033[101m\033[1;32m ENTER \033[0m")
                    os.system('clear')
                    print()
            except ValueError:
                input(f"{a}[{m}!{a}]{p} Pilihan Tidak Valid{m}!{a} | \033[101m\033[1;32m ENTER \033[0m")
                os.system('clear')
                print()

    def sfile_search_banner(self):
        print(f"""{m}
╭────────────────────────────────────────────────────────╮
{m}│⠀⠀{a}  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│
{m}│⠀⠀{a} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {m}│⠀⠀
{m}│⠀⠀{a} ⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a} ⠀⠀⣿⣿⣿⣿⣿⣿⠟⠿⠿⠿⠿⠿⠿⠿⠷⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠴⠿⠿⠿⠿⠿⠿⠿⠟⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a} ⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a}⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│⠀
{m}│⠀⠀{a}⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│⠀⠀⠀
{m}│⠀⠀{a}   ⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿   {m}│
{m}│⠀⠀{a}⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a} ⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│⠀⠀
{m}│⠀⠀{a} ⠀⠀⣿⣿⣿⣿⣿⣿⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⠀⠀⠀{m}│
{m}│⠀⠀{a} ⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀{m}│
{m}│⠀⠀{a}⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀{m}│
{m}│⠀⠀{a}                                                      {m}│
{m}│⠀⠀{a}               {a}[{m} >{p} MENCARI SFILE!{m} < {a}] ⠀               {m}│
╰────────────────────────────────────────────────────────╯
""")

    def sfile_search_main(self):
        while True:
            os.system("clear")
            self.sfile_search_banner()
            
            print(f"{a}[\033[101m{h} INFO {r}{a}]{p} Ketik \033[101m{h} ENTER {r} Untuk Keluar\n")
            query = input(f"{a}[{m}?{a}]{p} Masukkan 1 Kata Pencarian {m}:{a} ")
            
            if query.lower() == 'exit':
                break
            
            if not query.strip():
                input(f"\n{a}[{m}!{a}]{p} Kata kunci tidak boleh kosong{m}!{a} | \033[101m\033[1;32m ENTER \033[0m")
                continue
            
            
            result = self.sfile_search_all_pages(query)
            
            if not result or not result['files']:
                input(f"\n{a}[{m}!{a}]{p} Tidak ada hasil ditemukan untuk '{query}'{m}!{a} | \033[101m\033[1;32m ENTER \033[0m")
                continue
            
            self.sfile_search_show_menu(result['files'], query)

if __name__ == '__main__':
    searcher = SfileSearcher()
    searcher.sfile_search_main()
