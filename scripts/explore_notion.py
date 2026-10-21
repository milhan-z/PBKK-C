import os
import sys
import json
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.notion_helper import load_env, NOTION_VERSION

def get_block_children(block_id, headers):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")).get("results", [])
    except Exception as e:
        return []

def query_database(db_id, headers):
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    req = urllib.request.Request(url, data=b"{}", headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8")).get("results", [])
    except Exception as e:
        return []

def explore():
    env = load_env()
    key = env.get("NOTION_API_KEY")
    headers = {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "User-Agent": "AntigravityBot/1.0"
    }
    
    req = urllib.request.Request("https://api.notion.com/v1/search", data=b"{}", headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            print(f"=== TOTAL OBJEK DIAKSES: {len(results)} ===")
            for item in results:
                obj_type = item.get("object")
                item_id = item.get("id")
                
                title = "(Tanpa Judul)"
                if obj_type == "page":
                    props = item.get("properties", {})
                    for p_name, p_val in props.items():
                        if p_val.get("type") == "title":
                            title_parts = p_val.get("title", [])
                            title = "".join([t.get("plain_text", "") for t in title_parts])
                            break
                    print(f"\n[PAGE] {title} (ID: {item_id})")
                    print(f"  URL: {item.get('url')}")
                    
                    # Fetch block children of this page
                    blocks = get_block_children(item_id, headers)
                    print(f"  Jumlah blok konten: {len(blocks)}")
                    for b in blocks[:20]:
                        b_type = b.get("type")
                        content_dict = b.get(b_type, {})
                        rich_texts = content_dict.get("rich_text", [])
                        text = "".join([t.get("plain_text", "") for t in rich_texts])
                        if b_type == "child_database":
                            print(f"    - [Sub-Database]: {content_dict.get('title')}")
                        elif b_type == "child_page":
                            print(f"    - [Sub-Page]: {content_dict.get('title')}")
                        elif text:
                            print(f"    - [{b_type}]: {text}")
                            
                elif obj_type == "database":
                    title_parts = item.get("title", [])
                    title = "".join([t.get("plain_text", "") for t in title_parts])
                    print(f"\n[DATABASE] {title} (ID: {item_id})")
                    print(f"  URL: {item.get('url')}")
                    props = item.get("properties", {})
                    print("  Kolom/Properties:")
                    for p_name, p_val in props.items():
                        print(f"    - {p_name} ({p_val.get('type')})")
                    
                    # Query rows in database
                    rows = query_database(item_id, headers)
                    print(f"  Total entri baris: {len(rows)}")
                    for r in rows:
                        r_props = r.get("properties", {})
                        r_title = ""
                        for p_name, p_val in r_props.items():
                            if p_val.get("type") == "title":
                                r_title = "".join([t.get("plain_text", "") for t in p_val.get("title", [])])
                                break
                        row_details = []
                        for p_name, p_val in r_props.items():
                            p_type = p_val.get("type")
                            if p_type == "status":
                                status_name = (p_val.get("status") or {}).get("name", "")
                                row_details.append(f"Status: {status_name}")
                            elif p_type == "select":
                                sel_name = (p_val.get("select") or {}).get("name", "")
                                row_details.append(f"{p_name}: {sel_name}")
                            elif p_type == "date":
                                d_val = p_val.get("date") or {}
                                row_details.append(f"Date: {d_val.get('start')}")
                        print(f"    * {r_title} [{', '.join(row_details)}]")
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.read().decode("utf-8"))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    explore()
