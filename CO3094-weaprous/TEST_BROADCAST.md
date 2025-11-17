# 🎯 Test Guide: P2P Broadcast Feature

## ✅ Đã thêm Broadcast vào P2P Chat

### Tính năng mới:

1. **Web UI**: Nút "Broadcast All" màu cam
2. **CLI**: Command `broadcast <message>`
3. **Confirmation**: Xác nhận trước khi broadcast
4. **Feedback**: Hiển thị số peers nhận được

---

## 🧪 Test Cases

### Test 1: Broadcast qua Web UI

#### Setup:
```bash
# Terminal 1: Alice
node p2p_client.js alice

# Terminal 2: Bob
node p2p_client.js bob

# Terminal 3: Charlie
node p2p_client.js charlie
```

#### Steps:
1. Mở browser: http://127.0.0.1:8000/p2p_integrated.html
2. Connect với Alice (port từ terminal 1)
3. Click "🔄 Refresh" → Thấy Bob và Charlie
4. Click "🔗 Connect" cho cả Bob và Charlie
5. Đợi status chuyển thành "🟢 Connected"
6. Gõ tin nhắn: `Hello everyone from Alice!`
7. Click **"Broadcast All"** (nút cam)
8. Confirm popup: "Broadcast to 2 connected peers?"

#### Expected Results:
- ✅ Popup xác nhận hiển thị số peers chính xác
- ✅ System message: `📢 Broadcasting to 2 peers: "Hello everyone from Alice!"`
- ✅ Terminal Bob shows: `💬 Direct message from alice: Hello everyone from Alice!`
- ✅ Terminal Charlie shows: `💬 Direct message from alice: Hello everyone from Alice!`
- ✅ Confirmation message: `✅ Broadcast sent to: bob, charlie`

---

### Test 2: Broadcast qua CLI

#### Steps:
1. Trong terminal Alice, connect tới peers:
   ```
   connect bob
   connect charlie
   ```
2. Chờ handshake confirmations
3. Gõ lệnh broadcast:
   ```
   broadcast Hello from CLI broadcast!
   ```

#### Expected Results:
- ✅ Terminal Alice: `📢 Broadcast message to 2 peers: "Hello from CLI broadcast!"`
- ✅ Terminal Bob: `💬 Direct message from alice: Hello from CLI broadcast!`
- ✅ Terminal Charlie: `💬 Direct message from alice: Hello from CLI broadcast!`

---

### Test 3: Broadcast với 0 connected peers

#### Setup:
- Alice connected to P2P client
- Chưa connect với peer nào

#### Steps:
1. Gõ tin nhắn
2. Click "Broadcast All"

#### Expected Results:
- ✅ Alert: "No peers connected! Connect to peers first using 'Connect' buttons."
- ❌ Không broadcast message nào

---

### Test 4: Broadcast với 1 peer

#### Setup:
- Alice connected với Bob
- Charlie không connected

#### Steps:
1. Gõ tin nhắn: `Hello Bob only`
2. Click "Broadcast All"
3. Confirm: "Broadcast to 1 connected peer?"

#### Expected Results:
- ✅ Popup hiển thị "1 connected peer" (singular)
- ✅ Chỉ Bob nhận được message
- ✅ Charlie KHÔNG nhận được

---

### Test 5: Mix Direct và Broadcast

#### Scenario: Chat history với cả direct và broadcast messages

#### Steps:
1. Alice → Bob (direct): `Hi Bob`
2. Alice → All (broadcast): `Hello everyone`
3. Alice → Charlie (direct): `Hi Charlie`
4. Alice → All (broadcast): `Anyone there?`

#### Expected Results UI:
```
[alice → bob] Hi Bob                    🔗 P2P
[System] 📢 Broadcasting to 2 peers...
[alice] Hello everyone                  (no specific recipient)
[alice → charlie] Hi Charlie            🔗 P2P
[System] 📢 Broadcasting to 2 peers...
[alice] Anyone there?
```

---

### Test 6: Broadcast sau khi peer disconnect

#### Steps:
1. Alice connect Bob và Charlie
2. Tắt terminal Charlie (Ctrl+C)
3. Alice broadcast message

#### Expected Results:
- ✅ Charlie removed from connected peers
- ✅ Broadcast chỉ đến Bob
- ✅ Popup: "Broadcast to 1 connected peer?"
- ✅ Confirmation: "✅ Broadcast sent to: bob"

---

### Test 7: CLI help command

#### Steps:
```
help
```

#### Expected Output:
```
Commands:
  list - Show available P2P peers from server
  peers - Show currently connected peers
  connect <username> - Connect to peer
  send <username> <message> - Send direct message
  broadcast <message> - Broadcast message to all connected peers
  info - Show client information
  history - Show message history
  quit - Exit
```

---

## 🎨 UI Elements

### Broadcast Button Styling:
- Background: Orange gradient (`#f59e0b` to `#d97706`)
- Text: "Broadcast All"
- Position: Below "Send Direct" button

### Message Badges:
- Direct P2P: `🔗 P2P` (green)
- Broadcast: No specific badge (shows as system message context)
- System: `System` (gray)

---

## 📊 Comparison: Direct vs Broadcast

| Feature | Direct Message | Broadcast |
|---------|---------------|-----------|
| **Recipient** | 1 peer | All connected peers |
| **UI Button** | "Send Direct" (blue) | "Broadcast All" (orange) |
| **Confirmation** | No | Yes (shows count) |
| **CLI Command** | `send <user> <msg>` | `broadcast <msg>` |
| **Badge** | 🔗 P2P | System message |
| **Requires selection** | Yes | No |

---

## ✅ Checklist

Broadcast feature hoàn chỉnh khi:

- [ ] Web UI có nút "Broadcast All" màu cam
- [ ] Click broadcast hiển thị confirmation popup
- [ ] Popup hiển thị số peers chính xác
- [ ] Broadcast gửi đến TẤT CẢ connected peers
- [ ] System message xác nhận broadcast
- [ ] CLI command `broadcast` hoạt động
- [ ] Help text có hướng dẫn broadcast
- [ ] Alert khi không có connected peers
- [ ] Singular/plural grammar đúng (1 peer vs 2 peers)
- [ ] Terminal của tất cả peers nhận được message

---

## 🐛 Known Issues / Edge Cases

1. **Empty broadcast**: Nếu gõ tin nhắn trống → Button bị disable
2. **Very long message**: UI vẫn hiển thị đầy đủ
3. **Special characters**: HTML escape hoạt động đúng
4. **Rapid broadcasts**: Mỗi broadcast có system message riêng

---

## 🎉 Success Criteria

Broadcast feature đạt yêu cầu đề bài khi:

1. ✅ **Gửi được broadcast message** đến nhiều peers cùng lúc
2. ✅ **P2P thật**: Messages đi trực tiếp TCP, không qua server
3. ✅ **UI feedback**: User biết được gửi đến bao nhiêu peers
4. ✅ **Error handling**: Báo lỗi khi không có peers
5. ✅ **Documentation**: Có hướng dẫn trong help

---

**Test Status**: ✅ Ready for Testing  
**Last Updated**: 2025-11-18
