#!/usr/bin/env python3
"""
Notion Helper Script for PBKK Task Reports
Uses standard Python library (no external pip dependencies needed).
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error

NOTION_VERSION = "2022-06-28"

def load_env(env_path=None):
    """Simple .env parser"""
    if env_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(base_dir, ".env")
    
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip('"').strip("'")
                    env_vars[key.strip()] = val
    return env_vars

def clean_id(raw_id: str) -> str:
    """Extract clean 32-hex character ID or formatted UUID from URL or raw string."""
    raw_id = raw_id.strip()
    if "notion.com" in raw_id or "notion.so" in raw_id:
        path = raw_id.split("?")[0].split("/")[-1]
        if len(path) >= 32:
            raw_id = path[-32:]
    cleaned = raw_id.replace("-", "").strip()
    return cleaned

def make_request(endpoint: str, api_key: str, method: str = "GET", data: dict = None):
    url = f"https://api.notion.com/v1/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "User-Agent": "AntigravityBot/1.0"
    }
    
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data), None
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        try:
            return None, json.loads(error_msg)
        except Exception:
            return None, {"message": error_msg, "status": e.code}
    except Exception as e:
        return None, {"message": str(e)}

def test_connection():
    config = load_env()
    api_key = config.get("NOTION_API_KEY", "").strip()
    target_id = config.get("NOTION_PAGE_OR_DATABASE_ID", "").strip()
    
    if not api_key or api_key == "paste_token_kamu_di_sini":
        print("[ERROR] NOTION_API_KEY belum diisi di file .env!")
        return False
        
    print(f"[*] Menguji token API Notion...")
    user_info, err = make_request("users/me", api_key)
    if err:
        print(f"[FAILED] Gagal terhubung ke Notion:")
        print(json.dumps(err, indent=2))
        return False
        
    bot_name = user_info.get("name", "Unknown Bot")
    print(f"[OK] Berhasil terhubung! Nama Integrasi: {bot_name}")
    
    if target_id and target_id != "paste_id_halaman_atau_database_di_sini":
        cleaned_id = clean_id(target_id)
        print(f"[*] Mengecek target ID: {cleaned_id}...")
        
        # Test as database
        db_info, db_err = make_request(f"databases/{cleaned_id}", api_key)
        if db_info:
            title_list = db_info.get("title", [])
            title = "".join([t.get("plain_text", "") for t in title_list]) or "(Tanpa Judul)"
            print(f"[OK] Ditemukan target tipe: DATABASE ('{title}')")
            return True
            
        # Test as page
        page_info, page_err = make_request(f"pages/{cleaned_id}", api_key)
        if page_info:
            print(f"[OK] Ditemukan target tipe: PAGE")
            return True
            
        print(f"[WARNING] Token valid, tapi ID target ({cleaned_id}) tidak dapat diakses.")
        print("Pastikan kamu sudah klik '...' di halaman Notion -> Connections -> pilih integrasimu!")
        return False
    else:
        print("[INFO] NOTION_PAGE_OR_DATABASE_ID belum diisi atau masih default.")
    return True

def markdown_to_notion_blocks(markdown_text: str):
    """Converts a multi-line markdown string into Notion block objects."""
    blocks = []
    lines = markdown_text.strip().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            i += 1
            continue
            
        # Code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_content = "\n".join(code_lines)
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": code_content[:2000]}}],
                    "language": lang.lower() if lang in ["javascript", "python", "php", "html", "css", "sql", "bash", "json", "typescript"] else "plain text"
                }
            })
            i += 1
            continue

        # Headings
        if stripped.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": stripped[4:][:2000]}}]}
            })
        elif stripped.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": stripped[3:][:2000]}}]}
            })
        elif stripped.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": stripped[2:][:2000]}}]}
            })
        # Checkboxes / To-do
        elif stripped.startswith("- [ ] ") or stripped.startswith("- [x] "):
            checked = stripped.startswith("- [x] ")
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": stripped[6:][:2000]}}],
                    "checked": checked
                }
            })
        # Bullet list
        elif stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": stripped[2:][:2000]}}]}
            })
        # Numbered list
        elif re.match(r"^\d+\.\s+", stripped):
            text_part = re.sub(r"^\d+\.\s+", "", stripped)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": text_part[:2000]}}]}
            })
        # Quote
        elif stripped.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": [{"type": "text", "text": {"content": stripped[2:][:2000]}}]}
            })
        # Regular paragraph
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": stripped[:2000]}}]}
            })
        i += 1
    return blocks

def create_report(title: str, markdown_content: str):
    config = load_env()
    api_key = config.get("NOTION_API_KEY", "").strip()
    target_id = config.get("NOTION_PAGE_OR_DATABASE_ID", "").strip()
    
    if not api_key or api_key == "paste_token_kamu_di_sini":
        print("[ERROR] NOTION_API_KEY belum diisi di .env!")
        return None
    if not target_id or target_id == "paste_id_halaman_atau_database_di_sini":
        print("[ERROR] NOTION_PAGE_OR_DATABASE_ID belum diisi di .env!")
        return None
        
    cleaned_id = clean_id(target_id)
    blocks = markdown_to_notion_blocks(markdown_content)
    
    # Check if target is database or page
    db_info, _ = make_request(f"databases/{cleaned_id}", api_key)
    
    if db_info:
        # It's a database: find title property name
        properties = db_info.get("properties", {})
        title_prop_name = "Name"
        for prop_name, prop_data in properties.items():
            if prop_data.get("type") == "title":
                title_prop_name = prop_name
                break
                
        payload = {
            "parent": {"database_id": cleaned_id},
            "properties": {
                title_prop_name: {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            },
            "children": blocks[:100]  # Notion limit 100 blocks per request
        }
    else:
        # Treat as parent page
        payload = {
            "parent": {"page_id": cleaned_id},
            "properties": {
                "title": [{"type": "text", "text": {"content": title}}]
            },
            "children": blocks[:100]
        }
        
    res, err = make_request("pages", api_key, method="POST", data=payload)
    if err:
        print("[FAILED] Gagal membuat laporan di Notion:")
        print(json.dumps(err, indent=2))
        return None
        
    page_url = res.get("url", "")
    print(f"[SUCCESS] Laporan berhasil dibuat di Notion!\nURL: {page_url}")
    return page_url

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_connection()
    elif len(sys.argv) > 2 and sys.argv[1] == "create":
        title = sys.argv[2]
        content = sys.argv[3] if len(sys.argv) > 3 else "Laporan tugas PBKK."
        create_report(title, content)
    else:
        print("Penggunaan:")
        print("  python scripts/notion_helper.py test")
        print("  python scripts/notion_helper.py create \"Judul Laporan\" \"Konten Markdown...\"")
