# 🌐 WeApRous

**Một HTTP Server & Hệ thống Chat Hybrid được xây dựng từ đầu (from scratch) bằng Python.**

_Dự án cho môn học CO3094 - Mạng Máy Tính tại Trường Đại học Bách khoa (HCMUT)._

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Protocol](https://img.shields.io/badge/Protocol-HTTP/1.1-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

---

**WeApRous** không chỉ là một dự án bình thường. Đây là một hành trình đi sâu vào "bên dưới" của web, nơi chúng tôi tự tay xây dựng mọi thứ từ tầng socket TCP, phân tích các gói tin HTTP, cho đến việc tạo ra một ứng dụng chat P2P thời gian thực.

## 🚀 Tính năng nổi bật

### 🔐 Task 1A: HTTP Server & Authentication

- **Web Server đa luồng** xây dựng thuần túy bằng socket và threading của Python
- **Bộ phân tích HTTP (Parser)**: Tự phân tích Request (method, path, headers, cookies, body) và xây dựng Response
- **Hệ thống Routing**: Một hệ thống decorator gọn nhẹ để ánh xạ URL đến các hàm xử lý
- **Xác thực Session/Cookie**: Triển khai cơ chế đăng nhập, bảo vệ route, và quản lý session
- **Phục vụ tệp tĩnh**: Có khả năng phục vụ các tệp HTML, CSS, JS

### 💬 Task 2: Hybrid P2P Chat

- **Tracker & Peer Discovery**: Server trung tâm (Tracker) quản lý danh sách các peer và kênh chat
- **Giao diện Hiện đại**: UI chat responsive, thân thiện, giống các ứng dụng nhắn tin hiện đại
- **Cập nhật Polling**: Tự động làm mới tin nhắn mỗi 2 giây
- **Hai chế độ Chat**:
  - 🌍 **Broadcast Mode**: Gửi tin nhắn cho tất cả mọi người trong kênh
  - 🔒 **Direct Mode**: Nhắn tin riêng tư, trực tiếp (P2P) giữa hai peer

## 🛠️ Công nghệ sử dụng

| Component         | Technology / Library              |
| ----------------- | --------------------------------- |
| Backend           | Python (Sockets, Threading)       |
| Giao thức         | HTTP 1.1 (Cài đặt tùy chỉnh)      |
| Xác thực          | Cookie + Session (Tự quản lý)     |
| Frontend          | HTML5, CSS3, JavaScript (Vanilla) |
| Giao tiếp Dữ liệu | JSON qua HTTP                     |
| Kiến trúc         | Client–Server + Hybrid Peer Logic |

## ⚙️ Cài đặt & Khởi chạy

### 🌐 Bước 1: Cấu hình Network cho truy cập từ mạng LAN

#### Tìm địa chỉ IP của máy bạn:

```bash
# Windows
ipconfig | findstr "IPv4"

# Kết quả ví dụ: 172.16.0.117 (Wi-Fi adapter)
```

#### Cấu hình Proxy cho network access:

1. **Mở file `config/proxy.conf`**
2. **Sửa địa chỉ IP** trong các dòng sau:

```properties
# Thay YOUR_IP bằng IP thật của máy (ví dụ: 172.16.0.117)
host "YOUR_IP:8080" {
    proxy_pass http://127.0.0.1:8000;
}

host "YOUR_IP:8081" {
    proxy_pass http://127.0.0.1:8000;
}
```

#### Mở Windows Firewall (chạy với quyền Administrator):

```bash
# Mở port cho server
netsh advfirewall firewall add rule name="WeApRous Server Port 8000" dir=in action=allow protocol=TCP localport=8000

# Mở port cho proxy
netsh advfirewall firewall add rule name="WeApRous Proxy Port 8080" dir=in action=allow protocol=TCP localport=8080
```

### 🚀 Bước 2: Khởi chạy Services

#### Khởi chạy theo thứ tự:

1. **Khởi động Proxy Server:**

```bash
cd CO3094-weaprous
python start_proxy.py --server-ip 0.0.0.0 --server-port 8080
```

2. **Khởi động Main Application (Terminal mới):**

```bash
cd CO3094-weaprous
python start_app.py --server-ip 127.0.0.1 --server-port 8000
```

### 🌍 Bước 3: Truy cập ứng dụng

#### Truy cập từ máy local:

- **Task 1A (Authentication):** `http://localhost:8080/`
- **Task 2 (Chat):** `http://localhost:8080/chat.html`

#### Truy cập từ máy khác trong mạng LAN:

- **Task 1A:** `http://YOUR_IP:8080/` (ví dụ: http://172.16.0.117:8080/)
- **Task 2:** `http://YOUR_IP:8080/chat.html`

#### 💡 Mẹo:

- Mở nhiều tab/máy khác nhau để test chat P2P
- Sử dụng Thunder Client để test API endpoints
- Kiểm tra console để debug connection issues

## 🔄 Luồng hoạt động

### Luồng đi của một peer khi tham gia hệ thống:

**[1] 🚀 Khởi tạo**

- Peer đăng nhập (`/login`) để lấy cookie
- Peer đăng ký thông tin (`/submit-info`) với Tracker
- Peer tham gia kênh (`/add-list`)

**[2] 🤝 Kết nối**

- Peer lấy danh sách tất cả peer khác (`/get-list`)
- Khi muốn chat riêng, Peer A yêu cầu thông tin Peer B (`/connect-peer`)

**[3] ⌨️ Chat**

- **Broadcast**: Gửi tin nhắn lên server (`/broadcast-peer`)
- **Direct**: Gửi tin nhắn thẳng đến IP/Port của peer kia (`/send-peer`)
- **Polling**: Tự động gọi `/channel/messages` mỗi 2s để lấy tin nhắn mới

## 🧩 Kiến trúc

### Sơ đồ hệ thống

```
📡 Client (Web Browser)
│
├── 🎨 Chat UI (HTML + CSS + JS)
│    ├── Đăng nhập
│    ├── Chọn kênh
│    ├── Danh sách Peer
│    └── Khung chat
│
└── 🐍 Server (Python)
     ├── 📜 HTTP Parser (Request + Response)
     ├── 🗺️ Routing System (Task 1A)
     ├── 💬 Chat APIs (Task 2.2)
     ├── 🧭 Tracker + Quản lý Kênh
     └── 🔌 Socket Layer (Multi-threaded)
```

### Cấu trúc thư mục

```
CO3094-weaprous/
│
├── daemon/               # Lõi của server
│   ├── backend.py        # Logic TCP server
│   ├── httpadapter.py    # Adapter xử lý HTTP
│   ├── request.py        # Phân tích Request
│   ├── response.py       # Xây dựng Response
│   ├── proxy.py          # Proxy server implementation
│   └── weaprous.py       # Framework routing
│
├── apps/
│   └── app.py            # Logic của ứng dụng (API)
│
├── config/
│   └── proxy.conf        # Proxy configuration
│
├── www/                  # Các file HTML cho client
│   ├── index.html
│   ├── login.html
│   └── chat.html
│
├── static/               # CSS, JS, Images
│   ├── css/
│   │   └── styles.css
│   └── images/
│
├── start_app.py          # Điểm khởi chạy chính
├── start_proxy.py        # Khởi chạy proxy server
├── start_backend.py      # Khởi chạy backend
└── README.md
```

## 📚 Tài liệu API

### 🔐 API Xác thực (Task 1A)

#### POST /login

Xác thực người dùng và cấp cookie.

**Request Body:**

```json
{
  "username": "admin",
  "password": "password"
}
```

**Response (Success 200):**

- Thiết lập `Set-Cookie: auth=true; sessionid=...`

```json
{
  "status": "authorized",
  "message": "Login successful"
}
```

**Response (Failure 401):**

```json
{
  "status": "unauthorized",
  "message": "Invalid credentials"
}
```

### 💬 API Chat & Quản lý Peer (Task 2)

#### 🧭 Quản lý Peer & Kênh

| Endpoint        | Method | Description                                          |
| --------------- | ------ | ---------------------------------------------------- |
| `/submit-info`  | POST   | Đăng ký thông tin peer (username, IP, port)          |
| `/add-list`     | POST   | Tham gia vào một kênh chat                           |
| `/get-list`     | GET    | Lấy danh sách tất cả peer và kênh hiện có            |
| `/connect-peer` | POST   | Lấy IP/port của một peer cụ thể để kết nối trực tiếp |

#### 💭 Gửi & Nhận tin nhắn

| Endpoint            | Method | Description                                          |
| ------------------- | ------ | ---------------------------------------------------- |
| `/broadcast-peer`   | POST   | Gửi tin nhắn broadcast đến tất cả peer trong kênh    |
| `/send-peer`        | POST   | Gửi tin nhắn riêng tư (direct) đến một peer          |
| `/channel/messages` | POST   | Lấy lịch sử tin nhắn của một kênh (dùng cho polling) |

## 💡 Tóm tắt

Dự án này là minh chứng cho việc triển khai end-to-end một hệ thống giao tiếp HTTP - từ việc phân tích giao thức ở tầng socket đến tương tác peer-to-peer trên nền tảng web. Nó kết nối lập trình mạng cấp thấp với thiết kế ứng dụng, cho thấy cách các hệ thống truyền thông thực tế được xây dựng từ những nguyên tắc cơ bản.

## 👨‍💻 Tác giả

**Trần Vũ Đình Huy**

- Khoa Khoa học và Kỹ thuật Máy tính
- Trường Đại học Bách khoa (HCMUT)

---

_Được xây dựng với ❤️ và rất nhiều ☕ từ sinh viên HCMUT_
