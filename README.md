<h1 align="center">
  🌐 WeApRous 🌐
</h1>

<p align="center">
  <b>Một HTTP Server & Hệ thống Chat Hybrid được xây dựng từ đầu (from scratch) bằng Python.</b>
</p>

<p align="center">
  <i>Dự án cho môn học CO3094 - Mạng Máy Tính tại Trường Đại học Bách khoa (HCMUT).</i>
</p>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Protocol-HTTP/1.1-brightgreen?style=for-the-badge" alt="Protocol">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge" alt="Status">
  </a>
</p>

---

**WeApRous** không chỉ là một dự án bình thường. Đây là một hành trình đi sâu vào "bên dưới" của web, nơi chúng tôi tự tay xây dựng mọi thứ từ tầng socket TCP, phân tích các gói tin HTTP, cho đến việc tạo ra một ứng dụng chat P2P thời gian thực.

## ✨ Giao diện ứng dụng

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/434435ad-b42d-4dfd-8bec-56e99156d0a4" />

```markdown
![WeApRous Chat UI](link_den_anh_cua_ban.png)

🚀 Tính năng nổi bật
Dự án được chia làm hai phần chính với các tính năng chuyên biệt:

🔐 Task 1A: HTTP Server & Authentication
Web Server đa luồng xây dựng thuần túy bằng socket và threading của Python.

Bộ phân tích HTTP (Parser): Tự phân tích Request (method, path, headers, cookies, body) và xây dựng Response.

Hệ thống Routing: Một hệ thống decorator gọn nhẹ để ánh xạ URL đến các hàm xử lý.

Xác thực Session/Cookie: Triển khai cơ chế đăng nhập, bảo vệ route, và quản lý session (auth=true, sessionid).

Phục vụ tệp tĩnh: Có khả năng phục vụ các tệp HTML, CSS, JS.

💬 Task 2.2: Hybrid P2P Chat
Tracker & Peer Discovery: Server trung tâm (Tracker) quản lý danh sách các peer và kênh chat.

Giao diện Hiện đại: UI chat responsive, thân thiện, giống các ứng dụng nhắn tin hiện đại.

Cập nhật Polling: Tự động làm mới tin nhắn mỗi 2 giây.

Hai chế độ Chat:

🌍 Broadcast Mode: Gửi tin nhắn cho tất cả mọi người trong kênh.

🔒 Direct Mode: Nhắn tin riêng tư, trực tiếp (P2P) giữa hai peer.

🛠️ Công nghệ sử dụng
Component,Technology / Library
Backend,"Python (Sockets, Threading)"
Giao thức,HTTP 1.1 (Cài đặt tùy chỉnh)
Xác thực,Cookie + Session (Tự quản lý)
Frontend,"HTML5, CSS3, JavaScript (Vanilla)"
Giao tiếp Dữ liệu,JSON qua HTTP
Kiến trúc,Client–Server + Hybrid Peer Logic



⚙️ Cài đặt & Khởi chạy
Chỉ cần 2 bước đơn giản để khởi chạy server:

1. Mở Terminal và cd vào thư mục dự án:
cd CO3094-weaprous/CO3094-weaprous

2. Khởi chạy Server bằng Python:
python start_app.py --server-ip 0.0.0.0 --server-port 8000

3. Truy cập ứng dụng:
Mở trình duyệt của bạn và truy cập:

http://127.0.0.1:8000/chat.html
Mẹo: Mở nhiều tab/cửa sổ trình duyệt để giả lập nhiều peer tham gia chat!



🧭 Quản lý Peer & Kênh

Endpoint,Method,Description
/submit-info,POST,"Đăng ký thông tin peer (username, IP, port)."
/add-list,POST,Tham gia vào một kênh chat.
/get-list,GET,Lấy danh sách tất cả peer và kênh hiện có.
/connect-peer,POST,Lấy IP/port của một peer cụ thể để kết nối trực tiếp.

💭 Gửi & Nhận tin nhắn
| Endpoint | Method | Description | | :--- | :--- | :--- | | /broadcast-peer | POST | Gửi tin nhắn broadcast đến tất cả peer trong kênh. | | /send-peer | POST | Gửi tin nhắn riêng tư (direct) đến một peer. | | /channel/messages| POST | Lấy lịch sử tin nhắn của một kênh (dùng cho polling). |
</details>

💡 Tóm tắt
Dự án này là minh chứng cho việc triển khai end-to-end một hệ thống giao tiếp HTTP - từ việc phân tích giao thức ở tầng socket đến tương tác peer-to-peer trên nền tảng web.
Nó kết nối lập trình mạng cấp thấp với thiết kế ứng dụng, cho thấy cách các hệ thống truyền thông thực tế được xây dựng từ những nguyên tắc cơ bản.

👨‍💻 Tác giả
Trần Vũ Đình Huy
Nguyễn Tấn Đạt
Khoa Khoa học và Kỹ thuật Máy tính

Trường Đại học Bách khoa (HCMUT)

