# Task 1A: Authentication Handling - Test Guide

## 🎯 Task Requirements
- [x] Header Parsing
- [x] Session Management (via Set-Cookie)
- [x] Concurrency (threading)
- [x] Error Handling (401 Unauthorized)
- [x] Validate credentials (username=admin, password=password)
- [x] Set-Cookie header on login success
- [ ] Return index page with Set-Cookie on login success

---

## 🚀 How to Run

```bash
# Terminal 1: Start the Task 1A app
python start_app.py

# Terminal 2: Use Thunder Client to test (or curl)
# See test cases below
```

**Expected Server Output:**
```
======================================================================
Starting WeApRous Backend - Task 1A: Authentication Handling
======================================================================
Server listening on: 0.0.0.0:9000

Available Routes:
  • GET  http://localhost:9000/
  • POST http://localhost:9000/login

Credentials for Login:
  • username: admin
  • password: password
======================================================================
```

---

## 🧪 Test Cases

### Test 1: GET / (index page)

**Thunder Client:**
```
Method: GET
URL: http://localhost:9000/
Headers: (none needed)
Body: (empty)
```

**Expected Response:**
```
Status: 200 OK
Headers: Content-Type: application/json
Body:
{
  "page": "index",
  "message": "Welcome to the RESTful TCP WebApp",
  "status": "You are viewing the index page"
}
```

**Expected Console Output:**
```
[Request] GET path / version HTTP/1.1
[Request] prepared headers: {'host': 'localhost:9000'}
[Request] Found hook for GET /
[Response] Calling hook handler for GET /
[Response] JSON response: status=200, content-length=...
[HttpAdapter] Sending response to (...)
```

---

### Test 2: POST /login - Valid Credentials

**Thunder Client:**
```
Method: POST
URL: http://localhost:9000/login
Headers: Content-Type: application/json
Body:
{
  "username": "admin",
  "password": "password"
}
```

**Expected Response:**
```
Status: 200 OK
Headers: 
  - Content-Type: application/json
  - Set-Cookie: auth=true
  - Set-Cookie: sessionid=abc123def456
  - Set-Cookie: username=admin
  - Content-Length: ...

Body:
{
  "status": "logged_in",
  "message": "Authentication successful",
  "username": "admin",
  "auth": true
}
```

**Expected Console Output:**
```
[Request] POST path /login version HTTP/1.1
[Request] prepared headers: {'content-type': 'application/json', 'content-length': '...'}
[Request] prepared body: {"username": "admin", "password": "password"}
[Request] Found hook for POST /login
[App] POST /login - processing authentication request
[App] Login attempt: username='admin'
[App] Login successful - valid credentials
[Response] Calling hook handler for POST /login
[Response] JSON response: status=200, content-length=...
[HttpAdapter] Sending response to (...)
```

---

### Test 3: POST /login - Invalid Credentials

**Thunder Client:**
```
Method: POST
URL: http://localhost:9000/login
Headers: Content-Type: application/json
Body:
{
  "username": "hacker",
  "password": "wrong"
}
```

**Expected Response:**
```
Status: 401 Unauthorized
Headers: 
  - Content-Type: application/json
  - Content-Length: ...

Body:
{
  "status": "unauthorized",
  "message": "Invalid username or password",
  "auth": false
}
```

**Expected Console Output:**
```
[Request] POST path /login version HTTP/1.1
[Request] prepared body: {"username": "hacker", "password": "wrong"}
[Request] Found hook for POST /login
[App] POST /login - processing authentication request
[App] Login attempt: username='hacker'
[App] Login failed - invalid credentials (username=hacker)
[Response] Calling hook handler for POST /login
[Response] JSON response: status=401, content-length=...
[HttpAdapter] Sending response to (...)
```

---

### Test 4: POST /login - Missing Credentials

**Thunder Client:**
```
Method: POST
URL: http://localhost:9000/login
Headers: Content-Type: application/json
Body:
{
  "username": "admin"
}
```

**Expected Response:**
```
Status: 401 Unauthorized
Body:
{
  "status": "unauthorized",
  "message": "Invalid username or password",
  "auth": false
}
```

---

### Test 5: POST /login - Invalid JSON

**Thunder Client:**
```
Method: POST
URL: http://localhost:9000/login
Headers: Content-Type: application/json
Body:
{invalid json}
```

**Expected Response:**
```
Status: 401 Unauthorized
Body:
{
  "status": "unauthorized",
  "message": "Invalid JSON format in request body"
}
```

---

### Test 6: POST /login - Empty Body

**Thunder Client:**
```
Method: POST
URL: http://localhost:9000/login
Headers: Content-Type: application/json
Body: (empty)
```

**Expected Response:**
```
Status: 401 Unauthorized
Body:
{
  "status": "unauthorized",
  "message": "Missing credentials"
}
```

---

## ✅ Validation Checklist

### Response Headers
- [ ] Status line present (HTTP/1.1 200 OK)
- [ ] Content-Type: application/json present
- [ ] Content-Length calculated correctly
- [ ] Set-Cookie headers present on login success (3 cookies)
- [ ] No extra/malformed headers

### Response Body
- [ ] Valid JSON format
- [ ] Correct status codes (200, 401, 500)
- [ ] Correct status text (OK, Unauthorized, etc.)
- [ ] Appropriate error messages

### Request Parsing
- [ ] Method extracted correctly (GET, POST)
- [ ] Path extracted correctly (/, /login)
- [ ] Headers parsed correctly
- [ ] Body extracted correctly
- [ ] Hook found or not found properly

### Error Handling
- [ ] Invalid credentials → 401 ✓
- [ ] Invalid JSON → 401 ✓
- [ ] Empty body → 401 ✓
- [ ] Route not found → 404 (if added)
- [ ] Server error → 500 (if handler crashes)

### Session Management
- [ ] Set-Cookie headers included on success
- [ ] Cookies contain: auth, sessionid, username
- [ ] Cookies properly formatted

### Concurrency
- [ ] Multiple Thunder requests work simultaneously
- [ ] No race conditions
- [ ] CTRL+C stops server gracefully

---

## 📊 Test Results Summary

| Test | Method | URL | Expected Status | ✓/✗ | Notes |
|------|--------|-----|-----------------|-----|-------|
| 1 | GET | / | 200 | | Index page |
| 2 | POST | /login | 200 | | Valid creds + Set-Cookie |
| 3 | POST | /login | 401 | | Invalid creds |
| 4 | POST | /login | 401 | | Missing password |
| 5 | POST | /login | 401 | | Invalid JSON |
| 6 | POST | /login | 401 | | Empty body |

---

## 🔧 Troubleshooting

### Issue: Server doesn't start
**Solution:** Check if port 9000 is in use
```bash
netstat -ano | findstr :9000
taskkill /PID <PID> /F
```

### Issue: Response shows 500 error
**Solution:** Check console for exception details
- Look at `[Response] Error in hook handler: ...`
- Check `[App]` console output

### Issue: Set-Cookie not appearing
**Solution:** Make sure login returns 3-tuple:
```python
return (200, data, cookies_dict)  # ✓ Correct
return (200, data)                # ✗ Wrong - no cookies
```

### Issue: 401 appearing instead of 200
**Solution:** Check credentials in request body
- Should be: `"username": "admin"` (exact match)
- Should be: `"password": "password"` (exact match)

---

## 📝 Implementation Checklist

- [x] Task 1A app.py created with login handler
- [x] response.py updated to support 401 status
- [x] response.py updated to support Set-Cookie headers
- [x] login handler returns (status, data, cookies) tuple
- [x] Error handling for invalid JSON
- [x] Error handling for missing credentials
- [x] Console logging for debugging
- [x] Proper Content-Length calculation
- [ ] Return index page (HTML) with Set-Cookie on login
- [ ] Client-side cookie handling in Thunder Client

---

## 🎓 Learning Outcomes

After completing Task 1A, you should understand:

1. **HTTP Header Parsing**: Extracting headers from raw HTTP requests
2. **Session Management**: Using Set-Cookie headers to maintain sessions
3. **Authentication**: Validating credentials and returning appropriate status codes
4. **Concurrency**: How threading handles multiple simultaneous requests
5. **Error Handling**: Returning 401 for unauthorized, 400 for bad requests, 500 for server errors
6. **HTTP Status Codes**: 200 (OK), 401 (Unauthorized), 500 (Internal Server Error)

---

**Happy Testing! 🎉**
