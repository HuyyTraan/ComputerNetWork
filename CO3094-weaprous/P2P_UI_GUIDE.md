# WeApRous P2P Chat - Quick Start Guide

## 🚀 Cách sử dụng P2P Chat trên Web UI

### Phương pháp 1: Sử dụng script tự động (KHUYẾN NGHỊ)

```bash
# Chạy script khởi động
start_p2p_ui.bat

# Script sẽ tự động:
# 1. Kiểm tra và cài đặt dependencies
# 2. Khởi động WeApRous server (nếu chưa chạy)
# 3. Khởi động P2P client với username bạn nhập
# 4. Mở browser tự động
```

### Phương pháp 2: Chạy thủ công (chi tiết)

#### Bước 1: Khởi động WeApRous Server
```bash
python start_app.py
```

#### Bước 2: Khởi động P2P Client
```bash
# Terminal 1 - User Alice
node p2p_client.js alice

# Terminal 2 - User Bob (terminal khác)
node p2p_client.js bob
```

**Lưu ý WebSocket Port:**
Khi P2P client khởi động, sẽ hiển thị:
```
============================================================
✅ P2P Client ready!
============================================================
   👤 User: alice
   🔗 P2P Server: localhost:xxxxx
   🌐 WebSocket: ws://localhost:62420    <-- PORT NÀY QUAN TRỌNG
============================================================
```

#### Bước 3: Mở Browser UI

1. Mở trình duyệt: http://127.0.0.1:8000/p2p_integrated.html
2. Nhập username: `alice` (phải giống với P2P client)
3. Nhập WebSocket port: `62420` (lấy từ terminal)
4. Click "Connect to P2P Client"

#### Bước 4: Kết nối với Peer

1. Sau khi connect, click "🔄 Refresh" để xem danh sách peers
2. Click "🔗 Connect" để kết nối với peer
3. Click "💬 Chat" để bắt đầu chat
4. Gõ tin nhắn và click "Send"

## 📋 Các tính năng chính

### ✅ Đã hoàn thành:

1. **True P2P Connection**
   - Kết nối trực tiếp TCP giữa các peer
   - Không qua server khi gửi direct message

2. **WebSocket Bridge**
   - Browser UI kết nối với Node.js P2P client qua WebSocket
   - Real-time message delivery

3. **Peer Discovery**
   - Tự động lấy danh sách peers từ tracker server
   - Hiển thị status connected/available

4. **Auto-Connect Feature**
   - Tự động kết nối với tất cả peers available
   - Button "Auto-Connect All Peers"

5. **Beautiful UI**
   - Modern design với gradient và animations
   - Real-time status updates
   - Message badges (P2P/Server/System)

### 🔧 Cách test P2P thực sự:

```bash
# 1. Start 2 P2P clients
Terminal 1: node p2p_client.js alice
Terminal 2: node p2p_client.js bob

# 2. Trong terminal Alice:
connect bob
send bob Hello from Alice via P2P!

# 3. Bob sẽ nhận được tin nhắn TRỰC TIẾP qua TCP
# 4. Mở browser UI để xem tin nhắn với badge "🔗 P2P"

# 5. Test: TẮT server giữa chừng
# Alice và Bob vẫn chat được vì đã kết nối P2P!
```

## 🎯 So sánh các chế độ Chat

### Server-Based Chat (`/chat.html`)
- ✅ Browser only, không cần setup
- ✅ Dễ sử dụng
- ❌ Tin nhắn đi qua server (không phải P2P thật)
- ❌ Server bottleneck

### True P2P Chat (`/p2p_integrated.html`)
- ✅ Kết nối trực tiếp TCP giữa peers
- ✅ Không qua server (P2P thật)
- ✅ Scalable, không bottleneck
- ❌ Cần Node.js client chạy local
- ❌ Setup phức tạp hơn

## 🐛 Troubleshooting

### Lỗi: "Connection failed"
- Kiểm tra P2P client đã chạy chưa
- Kiểm tra WebSocket port đúng chưa
- Thử auto-detect port

### Lỗi: "No peers available"
- Kiểm tra WeApRous server đã chạy chưa
- Khởi động thêm P2P client khác
- Click "Refresh" để cập nhật danh sách

### Tin nhắn không gửi được
- Kiểm tra peer đã "Connected" (màu xanh) chưa
- Click "Connect" trước khi chat
- Kiểm tra terminal P2P client có lỗi không

## 📱 UI Screenshots Flow

```
1. Login Screen
   ├─ Enter username
   ├─ Enter/Auto-detect WebSocket port
   └─ Connect button

2. Main UI (After Connect)
   ├─ Sidebar
   │  ├─ Connection status badge
   │  ├─ Available peers list
   │  └─ Auto-connect button
   │
   └─ Chat Area
      ├─ Message history
      ├─ Message badges (P2P/Server/System)
      └─ Composer
```

## 🚀 Advanced Usage

### Multi-peer Testing
```bash
# Terminal 1
node p2p_client.js alice

# Terminal 2  
node p2p_client.js bob

# Terminal 3
node p2p_client.js charlie

# Mở 3 browser tabs:
# Tab 1: alice kết nối với bob và charlie
# Tab 2: bob kết nối với alice và charlie
# Tab 3: charlie kết nối với alice và bob

# Test group chat thông qua multiple P2P connections
```

### CLI + UI Hybrid
```bash
# Có thể dùng CLI và UI cùng lúc:
# - Terminal: Dùng CLI commands (connect, send, etc.)
# - Browser: Dùng GUI để xem messages đẹp hơn
# Cả 2 đều real-time sync qua WebSocket
```

## 📝 Implementation Details

### Architecture
```
Browser UI ←[WebSocket]→ Node.js P2P Client ←[TCP P2P]→ Other Peers
                              ↓
                         [HTTP Tracker]
                              ↓
                      WeApRous Server
```

### Message Flow
```
1. Direct P2P Message:
   Browser → WebSocket → P2P Client → TCP → Target Peer
   
2. Peer Discovery:
   P2P Client → HTTP → WeApRous Server → Returns peer list
```

### Why Browser Cannot Do P2P Directly?
- Browser security model không cho phép tạo TCP server
- Browser không thể listen trên arbitrary ports
- WebRTC là giải pháp cho browser P2P, nhưng phức tạp hơn
- Node.js client đóng vai trò "bridge" giữa browser và P2P network

## 🌟 Future Enhancements

1. **WebRTC Integration**: Browser-native P2P
2. **File Transfer**: P2P file sharing
3. **Voice/Video**: Real-time communication
4. **Encryption**: Secure P2P messages
5. **NAT Traversal**: STUN/TURN support

---

**Tác giả:** WeApRous Team  
**Course:** CO3094 - Computer Networks  
**University:** HCMUT - Ho Chi Minh University of Technology
