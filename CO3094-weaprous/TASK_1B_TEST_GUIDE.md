# Task 1B: Cookie-based Access Control - Test Guide

## 🎯 Task Requirements

**Task 1B: Implement cookie-based access control**

- When a client sends a GET request to `/`, the server must check for the presence of the `auth=true` cookie.
- If the cookie is present, the server serves the index page (200 OK).
- If the cookie is missing or incorrect, the server responds with 401 Unauthorized.

---

## 🚀 How to Run

```bash
# Terminal 1: Start the Task 1B app
python start_app.py

# Terminal 2: Use Thunder Client to test
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

Press CTRL+C to stop the server
======================================================================
```

---

## 🧪 Test Cases

### Test 1: GET / WITHOUT cookie (should fail)

**Thunder Client:**
```
Method: GET
URL: http://localhost:9000/
Headers: (none - make sure Cookie header is NOT set)
Body: (empty)
```

**Expected Response:**
```
Status: 401 Unauthorized
Headers: Content-Type: application/json
Body:
{
  "status": "unauthorized",
  "message": "Auth cookie required. Please login first.",
  "authenticated": false
}
```

**Expected Console Output:**
```
[Request] GET path / version HTTP/1.1
[Request] prepared headers: {'host': 'localhost:9000'}
[Request] prepared cookies: {}                          ← No cookies
[Request] Found hook for GET /
[App] GET / - checking authentication via cookie
[App] No auth cookie found
[Response] Calling hook handler for GET /
[Response] status code : 401, data: ...
```

---

### Test 2: POST /login (get auth cookie)

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
[Request] prepared cookies: {}                          ← No cookies yet
[Request] Found hook for POST /login
[App] POST /login - processing authentication request
[App] Login attempt: username='admin'
[App] Login successful - valid credentials
[Response] Calling hook handler for POST /login
[Response] cookies: {...}, status code : 200, data: ...
```

---

### Test 3: GET / WITH auth=true cookie (should succeed)

**Thunder Client:**
```
Method: GET
URL: http://localhost:9000/
Headers: Cookie: auth=true
Body: (empty)
```

**OR (Thunder auto-sends cookies if you already did Test 2 in same session):**
```
Method: GET
URL: http://localhost:9000/
Headers: (empty - Thunder auto-sends Set-Cookie from previous response)
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
  "status": "You are viewing the index page",
  "authenticated": true
}
```

**Expected Console Output:**
```
[Request] GET path / version HTTP/1.1
[Request] prepared headers: {'host': 'localhost:9000', 'cookie': 'auth=true; sessionid=abc123def456; username=admin'}
[Request] prepared cookies: {'auth': 'true', 'sessionid': 'abc123def456', 'username': 'admin'}    ← Cookies parsed!
[Request] Found hook for GET /
[App] GET / - checking authentication via cookie
[App] Cookies found: {'auth': 'true', 'sessionid': 'abc123def456', 'username': 'admin'}
[App] Valid auth cookie found - serving index page
[Response] Calling hook handler for GET /
[Response] status code : 200, data: ...
```

---

### Test 4: GET / WITH invalid cookie

**Thunder Client:**
```
Method: GET
URL: http://localhost:9000/
Headers: Cookie: auth=false
Body: (empty)
```

**Expected Response:**
```
Status: 401 Unauthorized
Headers: Content-Type: application/json
Body:
{
  "status": "unauthorized",
  "message": "Invalid or missing auth cookie",
  "authenticated": false
}
```

**Expected Console Output:**
```
[Request] GET path / version HTTP/1.1
[Request] prepared cookies: {'auth': 'false'}
[App] GET / - checking authentication via cookie
[App] Cookies found: {'auth': 'false'}
[App] Invalid auth cookie: false
[Response] Calling hook handler for GET /
[Response] status code : 401, data: ...
```

---

### Test 5: GET / WITH wrong auth cookie value

**Thunder Client:**
```
Method: GET
URL: http://localhost:9000/
Headers: Cookie: auth=123
Body: (empty)
```

**Expected Response:**
```
Status: 401 Unauthorized
Body:
{
  "status": "unauthorized",
  "message": "Invalid or missing auth cookie",
  "authenticated": false
}
```

---

## ✅ Validation Checklist

### Access Control Logic
- [ ] GET / without cookie → 401 ✓
- [ ] GET / with auth=true → 200 ✓
- [ ] GET / with auth=false → 401 ✓
- [ ] GET / with auth=xyz → 401 ✓

### Cookie Handling
- [ ] POST /login returns Set-Cookie headers ✓
- [ ] Thunder auto-stores cookies from Set-Cookie
- [ ] Next GET request includes Cookie header
- [ ] Server parses cookies correctly

### Response Format
- [ ] Status codes correct (200, 401)
- [ ] Status text correct (OK, Unauthorized)
- [ ] Content-Type: application/json ✓
- [ ] Response body is valid JSON ✓
- [ ] "authenticated" field in response ✓

### Request Parsing
- [ ] Cookies extracted from Cookie header
- [ ] Cookies stored in request.cookies dict ✓
- [ ] Multiple cookies separated by ";" ✓
- [ ] Cookie values with "=" handled correctly

---

## 📊 Test Flow

1. **Verify no access without login:**
   - Test 1: GET / without cookie → 401
   
2. **Login to get cookie:**
   - Test 2: POST /login (admin/password) → 200 + Set-Cookie
   
3. **Verify access with cookie:**
   - Test 3: GET / with auth=true → 200 (index page)
   - Test 4: GET / with auth=false → 401
   - Test 5: GET / with wrong cookie → 401

---

## 🔍 What Changed from Task 1A

### handlers parameter
```python
# Task 1A: Only received body
def login(body=""):
    pass

# Task 1B: Receive request object
def login(request=None, body=""):
    cookies = request.cookies  # ← Can access cookies!
    pass
```

### response.py hook call
```python
# Task 1A: Pass only body
result = request.hook(body=request.body)

# Task 1B: Pass request object
result = request.hook(request=request)
```

### Access control logic
```python
# Task 1B: Check cookie before serving content
if request and request.cookies.get('auth') == 'true':
    return (200, {...})  # Authorized
else:
    return (401, {...})  # Unauthorized
```

---

## 🎓 Learning Outcomes

After completing Task 1B, you should understand:

1. **Cookie-based Authentication**: Using cookies to maintain session state
2. **Access Control**: Checking authentication before serving protected resources
3. **HTTP Status Codes**: Using 401 Unauthorized for access denied
4. **Request Object Passing**: Handlers receiving full request context
5. **Cookie Parsing**: Extracting and validating cookies from requests

---

## 🐛 Troubleshooting

### Issue: GET / still returns index page without cookie
**Solution:** Make sure app.py has the cookie check implemented
- Check that `index()` function checks `request.cookies.get('auth')`
- Make sure response.py passes `request=request` to hook

### Issue: Cookies not being sent to server
**Solution:** 
- Option 1: Manually add `Cookie: auth=true` header in Thunder
- Option 2: Login first (Test 2), then Thunder auto-sends cookies
- Option 3: Check Thunder's cookie jar to verify cookies are stored

### Issue: "Invalid or missing auth cookie" even with valid cookie
**Solution:** Check console output
- Look for: `[App] Cookies found: {...}`
- Make sure `auth` value is exactly `'true'` (case-sensitive)
- Not `'True'` or `true` without quotes

### Issue: Handler receiving None for request
**Solution:** Update response.py to pass request object
```python
# Must be:
result = request.hook(request=request)
# NOT:
result = request.hook(body=request.body)
```

---

## 📝 Implementation Checklist

- [x] response.py passes `request=request` to hook
- [x] index() handler accepts `request` parameter
- [x] index() checks `request.cookies.get('auth')`
- [x] index() returns 401 if auth != 'true'
- [x] index() returns 200 with index page if auth == 'true'
- [x] login() handler accepts `request` parameter
- [x] login() returns Set-Cookie headers on success
- [x] Console logging shows cookie extraction
- [x] Error handling for missing/invalid cookies

---

**Ready to Test Task 1B! 🚀**
