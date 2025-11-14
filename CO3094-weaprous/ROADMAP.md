# WeApRous HTTP Server - Development Roadmap

## ✅ Hoàn thành

### Phase 1: Backend Server Setup

- [x] Fix `backend.py` - xóa duplicate `server.accept()`
- [x] Thêm `server.settimeout(1)` để CTRL+C hoạt động
- [x] Fix exception handler cho `socket.timeout`

### Phase 2: HTTP Request Parsing (request.py)

- [x] Extract request line (method, path, version)
- [x] Parse headers
- [x] Parse cookies từ header
- [x] Parse body (với content-length)
- [x] Parse authentication từ Authorization header
- [x] Find hook từ routes

---

## 🚧 Cần làm tiếp theo

### Phase 3: Response Handling (response.py)

**Trạng thái:** ❓ Chưa xem
**Mục đích:** Build HTTP response từ request

**Tasks:**

- [ ] Xem file `response.py` - hiểu structure
- [ ] Implement `build_response()` method
- [ ] Handle status codes (200, 404, 500, etc.)
- [ ] Build response headers
- [ ] Serialize response body

---

### Phase 4: Request-Response Flow (httpadapter.py)

**Trạng thái:** ⚠️ Cần update
**Mục đích:** Liên kết request parsing và response building

**Tasks:**

- [ ] Review `handle_client()` flow
- [ ] Gọi `req.prepare()` ✓ (đã có)
- [ ] Check `req.hook` có tồn tại không
- [ ] Gọi hook handler nếu có
- [ ] Build response
- [ ] Send response back to client
- [ ] Handle errors (404 nếu không có hook)

---

### Phase 5: Sample Application (sampleApp.py)

**Trạng thái:** ⚠️ Cần fix
**Mục đích:** Test backend với real routes

**Tasks:**

- [ ] Fix import (missing `WeApRous` import)
- [ ] Hoàn thành các route handlers
- [ ] Test với Thunder client

---

### Phase 6: Testing & Integration

**Trạng thái:** 🔄 In Progress
**Mục đích:** Integrate tất cả lại và test

**Tests:**

- [ ] Test GET request → `/index.html`
- [ ] Test POST request → `/login` với body
- [ ] Test cookies parsing
- [ ] Test auth header parsing
- [ ] Test 404 response (route không tồn tại)
- [ ] Test error handling

---

## 📊 Architecture Overview

```
Thunder Client
    │
    ↓ POST /login (with headers, body)
Socket Connection (port 9000)
    │
    ↓ server.accept()
backend.py (run_backend)
    │
    ↓ Create thread
handle_client() in httpadapter.py
    │
    ├─ recv() raw HTTP message
    │
    ├─ req.prepare(msg, routes)  ✅
    │   ├─ extract_request_line() ✅
    │   ├─ prepare_headers() ✅
    │   ├─ prepare_cookies() ✅
    │   ├─ prepare_body() ✅
    │   ├─ prepare_auth() ✅
    │   └─ find hook from routes ✅
    │
    ├─ Check req.hook ⚠️ (TODO: implement logic)
    │   ├─ If hook exists → call hook(req)
    │   └─ If no hook → 404
    │
    ├─ resp.build_response(req) ❌ (TODO)
    │
    └─ conn.sendall(response)
        │
        ↓ Response back to Thunder
```

---

## 🔍 Code Issues Found

### request.py

**Issue 1:** prepare_content_length() có thể throw exception

```python
def prepare_content_length(self):
    return int(self.headers["content-length"])  # ← KeyError nếu không có!
```

**Fix:** Thêm error handling

```python
return int(self.headers.get("content-length", "0"))
```

**Issue 2:** prepare_cookies() có thể throw exception

```python
for pair in cookies_str.split(";"):
    key, value = pair.strip().split("=")  # ← ValueError nếu format sai
```

**Fix:** Thêm error handling

**Issue 3:** prepare_body() gọi prepare_content_length() nhưng method có thể return None

```python
if self.method not in ['GET']:
    self.prepare_body(request)  # ← Chỉ POST, PUT, PATCH cần body
```

**Fix:** Thêm các method khác (DELETE, OPTIONS, etc.)

---

## 🎯 Priority Order

**HIGH PRIORITY (Cần làm ngay):**

1. Fix exception handling trong `prepare_content_length()`
2. Fix exception handling trong `prepare_cookies()`
3. Review & implement `response.py`
4. Implement logic trong `handle_client()` để gọi hook

**MEDIUM PRIORITY:** 5. Fix `sampleApp.py` imports 6. Test toàn bộ flow

**LOW PRIORITY:** 7. Optimize performance 8. Add logging

---

## 📝 Next Step

**Hãy bắt đầu với Phase 3:** Review file `response.py` để hiểu cách build response.

**Câu hỏi:** Bạn muốn làm gì tiếp?

- [ ] Fix exception handling trong request.py
- [ ] Review response.py
- [ ] Review httpadapter.py
