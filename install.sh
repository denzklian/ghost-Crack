#! /usr/bin/bash
null="> /dev/null 2>&1"
g="\033[1;32m"
r="\033[1;31m"
b="\033[1;34m"
w="\033[0m"
echo -e $b">"$w" Starting Ghost-crack Tool"
echo -e $b">"$w" prepare for installing dependencies ..."
sleep 3
echo -e $b">"$w" installing package: "$g"wget"$w
apt-get install wget -y
clear
echo -e $b">"$w" installing package: "$g"curl"$w
apt-get install curl -y
clear
echo -e $b">"$w" installing package: "$g"apktool"$w
git clone https://github.com/Lexiie/Termux-Apktool
cd Termux-Apktool
dpkg -i apktool_2.3.4_all.deb
cd ..
apt-get install apktool -y
clear
echo -e $b">"$w" installing package: "$g"imagemagick"$w
apt-get install imagemagick -y
clear
echo -e $b">"$w" installing package: "$g"java"$w
wget https://raw.githubusercontent.com/popeye0013/Exploit/main/installjava && bash installjava
clear
echo -e $b">"$w" installing pacakge: "$g"python3"$w
apt-get install python3
clear
echo -e $b">"$w" installing modules: "$g"pillow"$w
pip3 install Pillow
clear
echo -e $b">"$w" installing flask: "$g"flask"$w
pip3 install flask 
clear
echo -e $b">"$w" installing dns: "$g"dns"$w
pip install dnspython
clear
echo -e $b">"$w" installing whois: "$g"whois"$w
pip3 install python-whois
clear
echo -e $b">"$w" installing aiohttp: "$g"aiohttp"$w
pip install aiohttp
clear
echo -e $b">"$w" installing bs4: "$g"bs4"$w
pip install beautifulsoup4
echo -e $b">"$w" installing x11-repo: "$g"x11-repo"$w
pkg install x11-repo
echo -e $b">"$w" installing chromium: "$g"chromium"$w
pkg install chromium
clear   
echo -e $b">"$w" installing nodejs: "$g"nodejs"$w
pip install nodejs
clear   
echo -e $b">"$w" installing crypto: "$g"crypto"$w
pip install cryptography pycryptodome
clear   
echo -e $b">"$w" installing phonenumber: "$g"phonenumber"$w
pip install phonenumbers 
clear   
echo -e $b">"$w" installing colorama: "$g"colorama"$w
pip install colorama 
clear   
echo -e $b">"$w" successfully installing dependencies"
echo -e $b">"$w" use command "$g"python3 ghost-track.py"$w" for start the console"
python3 ghost-track.py
