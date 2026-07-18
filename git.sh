#!/bin/bash

# Warna biar keren
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Config (user di-set via env atau input)
REPO_URL="${REPO_URL:-}"
USERNAME="${GITHUB_USER:-}"
TOKEN="${GITHUB_TOKEN:-}"
TARGET_DIR="${TARGET_DIR:-.}"
COMMIT_MSG="${COMMIT_MSG:-"Auto upload $(date '+%Y-%m-%d %H:%M:%S')"}"

# Fungsi minta input
ask_config() {
    echo -e "${YELLOW}📦 GitHub Auto Uploader${NC}"
    
    if [ -z "$REPO_URL" ]; then
        read -p "🔗 Repository URL (https://github.com/user/repo.git): " REPO_URL
    fi
    
    if [ -z "$USERNAME" ]; then
        read -p "👤 GitHub Username: " USERNAME
    fi
    
    if [ -z "$TOKEN" ]; then
        read -sp "🔑 GitHub Token (classic): " TOKEN
        echo
    fi
    
    if [ -z "$TARGET_DIR" ]; then
        read -p "📁 Folder target (default .): " input_dir
        TARGET_DIR="${input_dir:-.}"
    fi
}

# Validasi
validate_config() {
    if [ -z "$REPO_URL" ] || [ -z "$USERNAME" ] || [ -z "$TOKEN" ]; then
        echo -e "${RED}❌ Error: REPO_URL, USERNAME, dan TOKEN wajib diisi${NC}"
        exit 1
    fi
    
    if [ ! -d "$TARGET_DIR" ]; then
        echo -e "${RED}❌ Folder '$TARGET_DIR' ga ada!${NC}"
        exit 1
    fi
}

# Proses upload
upload_to_github() {
    cd "$TARGET_DIR" || exit 1
    
    echo -e "${GREEN}📂 Masuk ke folder: $(pwd)${NC}"
    
    # Init git kalo belum
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}⚙️ Init git repo...${NC}"
        git init
        git branch -M main
    fi
    
    # Set remote pake token
    AUTH_URL=$(echo "$REPO_URL" | sed "s|https://|https://${USERNAME}:${TOKEN}@|")
    git remote remove origin 2>/dev/null
    git remote add origin "$AUTH_URL"
    
    # Add & commit
    echo -e "${YELLOW}📝 Adding files...${NC}"
    git add .
    
    if git diff --staged --quiet; then
        echo -e "${YELLOW}⚠️ Ga ada perubahan, skip commit${NC}"
    else
        git commit -m "$COMMIT_MSG"
        echo -e "${GREEN}✅ Commit berhasil${NC}"
    fi
    
    # Push
    echo -e "${YELLOW}🚀 Uploading ke GitHub...${NC}"
    if git push -u origin main --force; then
        echo -e "${GREEN}✅ Upload sukses!${NC}"
    else
        echo -e "${RED}❌ Gagal push. Cek token/repo.${NC}"
        exit 1
    fi
}

# Main
main() {
    ask_config
    validate_config
    upload_to_github
}

main
