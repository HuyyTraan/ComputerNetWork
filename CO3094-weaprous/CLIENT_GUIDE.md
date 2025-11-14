# WeApRous Client Testing Guide

## 📋 Overview

`client.py` là Python client để test WeApRous backend server cho Task 1A & 1B.

**Features:**
- ✅ Auto cookie handling (stores Set-Cookie, sends Cookie headers)
- ✅ Pre-built test cases (5 tests)
- ✅ Interactive menu
- ✅ Custom request support
- ✅ Session persistence across requests

---

## 🚀 Setup

### Requirement
```bash
pip install requests
```

### Start Server (Terminal 1)
```bash
cd d:\fluoxetines\Study_space\hcmut\HK251\MMT\Assignment\Assignment1\CO3094-weaprous\CO3094-weaprous
python start_app.py
```

**Expected Output:**
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

## 🧪 Usage

### Option 1: Run All Tests
```bash
python client.py --test-all
```

**Output:**
```
======================================================================
RUNNING ALL TESTS
======================================================================

Test 1: GET / WITHOUT authentication
Status: 401 Unauthorized
✅ PASS: Got expected status 401

Test 2: POST /login with valid credentials
Status: 200 OK
Cookies received:
  auth = true
  sessionid = abc123def456
  username = admin
✅ PASS: Got expected status 200

Test 3: GET / WITH authentication
Status: 200 OK
Cookies sent: {'auth': 'true', 'sessionid': 'abc123def456', 'username': 'admin'}
✅ PASS: Got expected status 200

Test 4: POST /login with INVALID credentials
Status: 401 Unauthorized
✅ PASS: Got expected status 401

Test 5: GET / with INVALID cookie
Status: 401 Unauthorized
✅ PASS: Got expected status 401

======================================================================
TEST SUMMARY
======================================================================
✅ PASS: Test 1: GET / without auth
✅ PASS: Test 2: POST /login valid
✅ PASS: Test 3: GET / with auth
✅ PASS: Test 4: POST /login invalid
✅ PASS: Test 5: GET / invalid cookie

Total: 5 passed, 0 failed
```

### Option 2: Test Login Flow Only
```bash
python client.py --login
```

**Sequence:**
1. POST /login → Get cookies
2. GET / → Send cookies

### Option 3: Interactive Menu
```bash
python client.py
```

**Menu:**
```
======================================================================
WeApRous Client - Interactive Menu
======================================================================
1. GET / (no auth)
2. POST /login (valid credentials)
3. GET / (with auth)
4. POST /login (invalid credentials)
5. GET / (invalid cookie)
6. Run all tests
7. Custom request
0. Exit
======================================================================
Select option: _
```

### Option 4: Custom Server
```bash
python client.py --server-ip 192.168.1.100 --server-port 8080
```

---

## 📝 Test Cases Explained

### Test 1: GET / WITHOUT authentication

**What it does:**
```
Clear cookies → GET / → Expect 401
```

**Why?**
- No auth cookie provided
- Server should deny access

**Expected:**
```
Status: 401 Unauthorized
Body: {"status": "unauthorized", "message": "Auth cookie required..."}
```

---

### Test 2: POST /login with valid credentials

**What it does:**
```
POST /login with {"username": "admin", "password": "password"}
Store cookies from Set-Cookie headers
```

**Why?**
- Valid credentials should authenticate
- Server returns cookies

**Expected:**
```
Status: 200 OK
Cookies: auth=true, sessionid=abc123def456, username=admin
Body: {"status": "logged_in", "auth": true}
```

---

### Test 3: GET / WITH authentication

**What it does:**
```
Send GET / with cookies from Test 2
```

**Why?**
- Should have valid auth cookie now
- Server should grant access

**Expected:**
```
Status: 200 OK
Body: {"page": "index", "authenticated": true}
```

---

### Test 4: POST /login with INVALID credentials

**What it does:**
```
POST /login with {"username": "hacker", "password": "wrong"}
```

**Why?**
- Invalid credentials should fail
- No cookies should be set

**Expected:**
```
Status: 401 Unauthorized
Body: {"status": "unauthorized", "auth": false}
```

---

### Test 5: GET / with INVALID cookie

**What it does:**
```
Manually set cookies: auth=false, sessionid=invalid123
Send GET /
```

**Why?**
- Invalid cookie value should be rejected
- sessionid not in server's SESSIONS database

**Expected:**
```
Status: 401 Unauthorized
Body: {"status": "unauthorized", "message": "Session invalid or expired"}
```

---

## 🔍 Advanced Usage

### Custom Request (Interactive)
```
Select option: 7

Custom Request
======================================================================
Method (GET/POST): POST
Path (e.g., /login): /login
Body (JSON, leave empty for none): {"username":"admin","password":"password"}

Response:
  Status: 200
  Body: {...}
  Cookies: {'auth': 'true', ...}
```

### Manual Cookie Test
```python
# Terminal, create manual test script:

import requests

session = requests.Session()

# Step 1: Login
login_response = session.post(
    "http://localhost:9000/login",
    json={"username": "admin", "password": "password"}
)
print(f"Login: {login_response.status_code}")
print(f"Cookies: {dict(session.cookies)}")

# Step 2: Access protected resource
protected_response = session.get("http://localhost:9000/")
print(f"Get /: {protected_response.status_code}")
print(f"Body: {protected_response.json()}")
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused"
**Solution:** Make sure server is running
```bash
# Terminal 1
python start_app.py

# Wait for "Server listening on: 0.0.0.0:9000"
```

### Issue: All tests fail
**Solution:** Check server logs
- Look for `[App]` and `[Response]` messages
- Check if routes are registered

### Issue: Cookies not being sent
**Solution:** Check requests library version
```bash
pip install --upgrade requests
```

### Issue: "Invalid sessionid"
**Solution:** Check app.py SESSIONS dict
- Default has `"abc123def456"` key
- Login creates new sessionid
- Make sure login returns valid sessionid

---

## 📊 Cookie Auto-Handling

Python `requests.Session()` auto-handles cookies!

```python
session = requests.Session()  # ← Auto cookie jar

# POST /login
response = session.post(..., json={...})
# Server sends: Set-Cookie: auth=true; sessionid=abc...
# Session AUTOMATICALLY stores these

# GET /
response = session.get(...)
# Request AUTOMATICALLY includes: Cookie: auth=true; sessionid=abc...
```

**You don't need to manually manage cookies!** ✨

---

## 🎓 Learning Points

After using this client, you'll understand:

1. **HTTP Cookie Handling**: How browsers/clients store and send cookies
2. **Session Management**: Maintaining state across HTTP requests
3. **Authentication Flow**: Login → Get cookie → Access protected resource
4. **Status Codes**: 200 (OK), 401 (Unauthorized)
5. **Cookie Validation**: Server validates sessionid against database

---

## 📝 Tips

1. **Run all tests first** to validate server setup
   ```bash
   python client.py --test-all
   ```

2. **Interactive menu is best for learning**
   ```bash
   python client.py
   ```

3. **Compare with Thunder Client** for manual testing
   - Thunder: GUI-based, visual
   - client.py: Script-based, automation

4. **Extend with more tests** in custom_request() or add new methods

---

**Happy Testing! 🚀**
