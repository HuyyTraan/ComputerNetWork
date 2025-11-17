# 🚀 QUICK TEST GUIDE - P2P Chat UI

## ✅ Status: Đã khởi động thành công!

### 🖥️ Services đang chạy:

1. **WeApRous Server**: http://127.0.0.1:8000 ✅
2. **P2P Client Alice**: WebSocket port **61583** ✅
3. **P2P Client Bob**: WebSocket port **55940** ✅

---

## 📋 Test Steps

### Test 1: Kết nối Alice với UI

1. Mở browser: http://127.0.0.1:8000/p2p_integrated.html
2. Nhập:
   - Username: `alice`
   - WebSocket Port: `61583`
3. Click "Connect to P2P Client"
4. ✅ Nên thấy status: "Connected"

### Test 2: Alice xem danh sách peers

1. Click button "🔄 Refresh" ở sidebar
2. ✅ Nên thấy "bob" trong danh sách Available Peers
3. Thông tin: `bob - 127.0.0.1:55938`

### Test 3: Alice kết nối với Bob (P2P)

1. Tìm peer "bob" trong list
2. Click button "🔗 Connect"
3. ✅ Status của Bob nên đổi thành "🟢 Connected"
4. Kiểm tra terminal của Alice:
   ```
   🔗 Connecting to bob at 127.0.0.1:55938
   ✅ Connected to peer: bob
   🤝 Handshake confirmed with bob
   ```

### Test 4: Alice gửi tin nhắn P2P cho Bob

1. Click button "💬 Chat" trên peer Bob
2. Chat title nên đổi thành "Chat with bob"
3. Gõ tin nhắn: `Hello Bob from Alice via P2P!`
4. Click "Send"
5. ✅ Tin nhắn xuất hiện với badge **🔗 P2P** màu xanh
6. Kiểm tra terminal của Bob:
   ```
   💬 Direct message from alice: Hello Bob from Alice via P2P!
   ```

### Test 5: Bob reply (qua CLI)

1. Trong terminal của Bob, gõ:
   ```
   connect alice
   send alice Hi Alice! This is Bob replying via CLI!
   ```
2. Quay lại browser của Alice
3. ✅ Nên thấy tin nhắn từ Bob với badge **🔗 P2P**

### Test 6: Bob mở UI riêng

1. Mở tab browser mới: http://127.0.0.1:8000/p2p_integrated.html
2. Nhập:
   - Username: `bob`
   - WebSocket Port: `55940`
3. Click "Connect to P2P Client"
4. Refresh peers và connect với Alice
5. Chat 2 chiều giữa 2 browser tabs
6. ✅ Tất cả tin nhắn đều có badge **🔗 P2P**

### Test 7: Verify P2P thật (không qua server)

1. Chat Alice ↔ Bob hoạt động bình thường
2. Stop WeApRous server (Ctrl+C terminal server)
3. Thử gửi tin nhắn giữa Alice và Bob
4. ✅ **Vẫn chat được!** (Vì đã kết nối P2P trực tiếp)
5. Chỉ không refresh được peer list (cần server làm tracker)

---

## 🎯 Expected Results

### ✅ Thành công khi:

- [ ] Kết nối WebSocket thành công
- [ ] Hiển thị danh sách peers
- [ ] Connect peer thành công (terminal show handshake)
- [ ] Gửi tin nhắn có badge "🔗 P2P" màu xanh
- [ ] Tin nhắn xuất hiện ở cả 2 phía
- [ ] Sau khi kết nối P2P, tắt server vẫn chat được

### ❌ Lỗi thường gặp:

1. **"Connection failed"**
   - Kiểm tra WebSocket port đúng chưa
   - P2P client có chạy không
   - Thử auto-detect port

2. **"No peers available"**
   - Server có chạy không
   - Peer khác đã đăng ký chưa (check terminal)
   - Click Refresh

3. **Tin nhắn không gửi**
   - Peer đã connected chưa (màu xanh)
   - Click Connect trước khi chat
   - Check terminal có lỗi

---

## 🖼️ Screenshots Checklist

### UI Alice Browser:
- [ ] Login screen với username + port input
- [ ] Connected status badge (màu xanh)
- [ ] Peer list có Bob (với status)
- [ ] Chat area với tin nhắn có badge P2P
- [ ] Message từ Alice (bên phải)
- [ ] Message từ Bob (bên trái)

### Terminal Alice:
- [ ] P2P Server listening
- [ ] WebSocket server listening
- [ ] Registered with tracker
- [ ] Connecting to bob
- [ ] Handshake confirmed
- [ ] Direct message from bob

### Terminal Bob:
- [ ] Tương tự Alice
- [ ] Incoming P2P connection từ Alice
- [ ] Direct message from alice

---

## 📊 Test Matrix

| Test Case | Alice Action | Bob Sees | Badge | Pass |
|-----------|-------------|----------|-------|------|
| 1 | Connect UI | - | - | ⬜ |
| 2 | Refresh peers | - | - | ⬜ |
| 3 | Connect Bob | Incoming conn | - | ⬜ |
| 4 | Send "Hello" | Terminal msg | 🔗 P2P | ⬜ |
| 5 | - | CLI reply | 🔗 P2P | ⬜ |
| 6 | - | Connect UI | - | ⬜ |
| 7 | Chat via UI | UI shows msg | 🔗 P2P | ⬜ |
| 8 | Stop server | Still works! | 🔗 P2P | ⬜ |

---

## 🎉 Success Criteria

Hệ thống P2P hoàn chỉnh khi:

1. ✅ Browser UI kết nối được với P2P client
2. ✅ Hiển thị danh sách peers từ tracker
3. ✅ Kết nối P2P trực tiếp thành công
4. ✅ Gửi/nhận tin nhắn qua P2P
5. ✅ Tin nhắn có badge "P2P" để phân biệt
6. ✅ Tắt server giữa chừng vẫn chat được
7. ✅ CLI và UI đều hoạt động song song
8. ✅ Real-time message delivery

---

## 🔗 Quick Links

- **P2P UI**: http://127.0.0.1:8000/p2p_integrated.html
- **Server Chat**: http://127.0.0.1:8000/chat.html
- **Compare Options**: http://127.0.0.1:8000/chat_options.html
- **Index**: http://127.0.0.1:8000/

---

## 📝 Notes

- WebSocket ports tự động allocate, mỗi lần chạy có thể khác
- P2P ports cũng tự động allocate
- Tracker chỉ dùng để discovery, không relay messages
- Direct messages KHÔNG đi qua server (P2P thật)
- Broadcast messages vẫn đi qua server (không phải P2P)

---

**Last Updated**: 2025-11-18  
**Status**: Ready for Testing ✅
