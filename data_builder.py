import os
import json
import base64
import glob

def build_data():
    base_path = "D:/OpenCoPow/copow-data/cryptoverse-intel"
    data = {
        "transcripts": [],
        "reports": [],
        "knowledge": [],
        "last_updated": ""
    }
    
    # helper to read file content
    def read_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""

    # Transcripts
    for ext in ["*.txt", "*.md"]:
        for f in glob.glob(os.path.join(base_path, "transcripts", ext)):
            data["transcripts"].append({
                "name": os.path.basename(f),
                "content": read_file(f)
            })
        
    # Reports
    for f in glob.glob(os.path.join(base_path, "reports", "*.md")):
        data["reports"].append({
            "name": os.path.basename(f),
            "content": read_file(f)
        })
        
    # Knowledge Vault
    for f in glob.glob(os.path.join(base_path, "knowledge_vault", "*.md")):
        data["knowledge"].append({
            "name": os.path.basename(f),
            "content": read_file(f)
        })
        
    from datetime import datetime
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write to data.js
    js_content = f"const CRYPTOVERSE_DATA = {json.dumps(data, indent=2)};"
    
    # Write to both root and docs
    with open(os.path.join(base_path, "data.js"), 'w', encoding='utf-8') as f:
        f.write(js_content)
    with open(os.path.join(base_path, "docs", "data.js"), 'w', encoding='utf-8') as f:
        f.write(js_content)

    print("Data manifest rebuilt successfully.")

if __name__ == "__main__":
    build_data()
