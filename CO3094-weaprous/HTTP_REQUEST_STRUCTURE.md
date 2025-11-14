# HTTP Request Structure - Lý Thuyết

## Cấu trúc của một HTTP Request:

```
┌─────────────────────────────────┐
│   REQUEST LINE (Dòng 1)         │  ← Method, Path, Version
│   GET /index.html HTTP/1.1      │
├─────────────────────────────────┤
│   HEADERS (Dòng 2-N)            │  ← Key: Value pairs
│   Host: localhost:8080          │
│   User-Agent: Mozilla/5.0       │
│   Content-Length: 50            │
│   Cookie: sessionId=abc123      │
│   (dòng trống)                  │
├─────────────────────────────────┤
│   BODY (Nếu có)                 │  ← POST/PUT data
│   name=John&age=30              │
└─────────────────────────────────┘
```

## Thứ tự xử lý HTTP Request:

### 1️⃣ **REQUEST LINE** (PHẢI PARSE TRƯỚC)

```
GET /index.html HTTP/1.1
```

**Tại sao trước?**

- Nó ở dòng 1, chứa thông tin cơ bản (method, path, version)
- **Phải biết method để quyết định có body hay không**
  - GET, HEAD, DELETE: KHÔNG có body
  - POST, PUT, PATCH: CÓ body
- Phải biết path để **tìm hook (route handler)**

### 2️⃣ **HEADERS** (PARSE THỨ HAI)

```
Host: localhost
Content-Length: 50
Content-Type: application/x-www-form-urlencoded
Cookie: sessionId=abc123
```

**Tại sao thứ 2?**

- Headers chứa **metadata quan trọng** cho body:
  - `Content-Length`: độ dài body
  - `Content-Type`: kiểu dữ liệu body
  - `Cookie`: thông tin cookies
- Phải parse headers **trước khi parse body**

### 3️⃣ **COOKIES** (EXTRACT TỪ HEADERS)

```python
# Cookie header có dạng:
Cookie: sessionId=abc123; userId=456; token=xyz
```

**Đặc điểm:**

- Là một phần của headers
- Parse **sau khi có headers**
- Có thể extract/parse nó **cùng lúc với headers**

### 4️⃣ **CONTENT-LENGTH** (EXTRACT TỪ HEADERS)

```python
# Headers có:
Content-Length: 50
```

**Đặc điểm:**

- Cũng là một phần của headers
- Extract **sau khi có headers**
- **PHẢI có nó để parse body chính xác**

### 5️⃣ **BODY** (PARSE CUỐI CÙNG)

```
name=John&age=30
```

**Tại sao cuối?**

- **Phải biết Content-Length trước** để biết lấy bao nhiêu bytes
- **Phải biết Content-Type** để parse đúng format (JSON, form-data, etc.)
- **Nằm sau headers, được phân tách bởi `\r\n\r\n`**

### 6️⃣ **AUTHENTICATION** (TUỲ CHỌN)

```python
# Từ header:
Authorization: Bearer eyJhbGc...
# Hoặc:
Authorization: Basic dXNlcjpwYXNz
```

**Đặc điểm:**

- Extract từ headers
- Parse **sau khi có headers**

---

## ✅ THỨ TỰ CHÍNH XÁC để parse HTTP Request:

```
1. REQUEST LINE (method, path, version)
   ↓
2. HEADERS (toàn bộ headers)
   ↓
3. COOKIES (extract từ headers)
   ↓
4. CONTENT-LENGTH (extract từ headers)
   ↓
5. BODY (parse dựa trên content-length + content-type)
   ↓
6. AUTHENTICATION (extract từ headers)
   ↓
7. FIND HOOK/ROUTE (dựa trên method + path)
```

---

## ❓ Câu hỏi: Thứ tự có cần tuần tự không?

### **CÓ! Vì những lý do sau:**

| Step           | Phụ thuộc vào                 | Lý do                          |
| -------------- | ----------------------------- | ------------------------------ |
| Request Line   | ❌ Không                      | Parse trước, độc lập           |
| Headers        | Request Line                  | Cần biết request line đã parse |
| Cookies        | Headers                       | Nằm trong headers              |
| Content-Length | Headers                       | Nằm trong headers              |
| Body           | Content-Length + Content-Type | Cần biết lấy bao nhiêu bytes   |
| Auth           | Headers                       | Nằm trong headers              |
| Hook/Route     | Request Line + Routes dict    | Cần method + path              |

### **Kết luận:**

- ✅ Phải **tuần tự**
- ✅ **CÓ thể tối ưu**: Parse cookies, content-length, auth cùng lúc với headers (chúng đều từ headers)
- ❌ **KHÔNG thể**: Parse body trước headers (body phụ thuộc headers)

---

## 📊 So sánh code hiện tại vs lý thuyết:

```python
# HIỆN TẠI (request.py):
def prepare(self, request, routes=None):
    # 1. ✅ Extract request line
    self.method, self.path, self.version = self.extract_request_line(request)

    # 2. ✅ Find hook TRƯỚC headers (LỖI LOGIC!)
    self.hook = routes.get((self.method, self.path))

    # 3. ✅ Parse headers
    self.headers = self.prepare_headers(request)

    # 4. ❌ THIẾU: Extract cookies từ headers
    # 5. ❌ THIẾU: Extract content-length từ headers
    # 6. ❌ THIẾU: Parse body
    # 7. ❌ THIẾU: Extract auth từ headers
```

**VẤN ĐỀ:**

- Find hook ở vị trí #2 là **CÓ THỂ** nhưng nên ở cuối (sau khi parse hết)
- Thiếu parse body, auth, content-length

```

---

## 🎯 Kết luận:

**Thứ tự PHẢI tuần tự:**
```

Request Line → Headers → (Cookies + Content-Length + Auth từ headers) → Body → Find Hook

```

**CÓ thể linh động:**
- Extract cookies, content-length, auth cùng lúc với parse headers
- Find hook có thể ở đầu hoặc cuối (nhưng lý thuyết nên ở cuối)
```
