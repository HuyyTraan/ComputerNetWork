# WeApRous - Testing Guide

## ✅ IMPLEMENTATION STATUS

### Phase 1: Backend Server ✅
- [x] Fixed `backend.py` - removed duplicate accept()
- [x] Added `server.settimeout(1)` for CTRL+C support
- [x] Fixed exception handler for socket.timeout

### Phase 2: HTTP Request Parsing ✅
- [x] Extract request line (method, path, version)
- [x] Parse headers
- [x] Parse cookies from header
- [x] Parse body (with content-length)
- [x] Parse authentication from Authorization header
- [x] Find hook from routes

### Phase 3: Response Building ✅
- [x] Refactored `build_response()` to handle 3 cases:
  - JSON response (with hook)
  - Static file response
  - 404 error response
- [x] Implemented `build_json_response()` with status code support
- [x] Implemented `build_file_response()` for static files
- [x] Implemented `build_error_response()` for errors
- [x] Fixed all hardcoded values

### Phase 4: Request-Response Flow ✅
- [x] Refactored `handle_client()` in httpadapter.py
- [x] Proper error handling with try-except-finally
- [x] Logging for debugging
- [x] No double-calling of hooks

### Phase 5: Sample Application ✅
- [x] Fixed imports in sampleApp.py
- [x] Fixed indentation
- [x] Proper entry point with `app.run()`

---

## 🚀 HOW TO TEST

### Step 1: Start Backend with Sample App

```bash
cd d:\fluoxetines\Study_space\hcmut\HK251\MMT\Assignment\Assignment1\CO3094-weaprous\CO3094-weaprous
python start_sampleapp.py
```

**Expected Output:**
```
[Backend] Listening on port 9000
[Backend] route settings {('GET', '/'): <function home>, ('GET', '/user'): <function get_user>, ('POST', '/echo'): <function echo>}
```

---

### Step 2: Test with Thunder Client

#### **Test 1: GET / (home endpoint)**
```
Method: GET
URL: http://localhost:9000/

Expected Response:
Status: 200 OK
Body: {"message": "Welcome to the RESTful TCP WebApp"}

Expected Console Output:
[Request] GET path / version HTTP/1.1
[Request] prepared headers: {...}
[Request] Found hook for GET /index.html
[Response] Calling hook handler for GET /index.html
[HttpAdapter] Sending response to (...)
```

---

#### **Test 2: GET /user**
```
Method: GET
URL: http://localhost:9000/user

Expected Response:
Status: 200 OK
Body: {"id": 1, "name": "Alice", "email": "alice@example.com"}

Expected Console Output:
[Request] GET path /user version HTTP/1.1
[Request] Found hook for GET /user
[Response] Calling hook handler for GET /user
[Response] JSON response: {"id": 1, "name": "Alice", "email": "alice@example.com"}
```

---

#### **Test 3: POST /echo (valid JSON)**
```
Method: POST
URL: http://localhost:9000/echo

Headers:
Content-Type: application/json
Content-Length: 35

Body:
{"user":"admin","password":"test"}

Expected Response:
Status: 200 OK
Body: {"received": {"user":"admin","password":"test"}}

Expected Console Output:
[Request] POST path /echo version HTTP/1.1
[Request] prepared headers: {'content-type': 'application/json', 'content-length': '35'}
[Request] prepared body: {"user":"admin","password":"test"}
[Request] Found hook for POST /echo
[Response] Calling hook handler for POST /echo
[Response] JSON response: {"received": {"user":"admin","password":"test"}}
```

---

#### **Test 4: POST /echo (invalid JSON)**
```
Method: POST
URL: http://localhost:9000/echo

Headers:
Content-Type: application/json
Content-Length: 11

Body:
invalid json

Expected Response:
Status: 200 OK
Body: {"error": "Invalid JSON"}

Expected Console Output:
[Request] POST path /echo version HTTP/1.1
[Request] prepared body: invalid json
[Response] Calling hook handler for POST /echo
[Response] JSON response: {"error": "Invalid JSON"}
```

---

#### **Test 5: GET /nonexistent (route not found)**
```
Method: GET
URL: http://localhost:9000/nonexistent

Expected Response:
Status: 404 Not Found
Body: {"error": "Route not found"}

Expected Console Output:
[Request] GET path /nonexistent version HTTP/1.1
[Request] No route handler for GET /nonexistent
[Response] No hook found
[HttpAdapter] Sending response to (...)
```

---

## 🔍 WHAT TO CHECK

### ✅ Request Parsing
- [ ] Method extracted correctly (GET, POST)
- [ ] Path extracted correctly (/user, /echo)
- [ ] Headers parsed correctly
- [ ] Cookies parsed correctly (if any)
- [ ] Body extracted with correct content-length
- [ ] Hook found (or not found)

### ✅ Response Building
- [ ] Status code correct (200, 201, 204, 404, 500)
- [ ] Status text correct (OK, Created, Not Found, etc.)
- [ ] Content-Type correct (application/json)
- [ ] Content-Length correct
- [ ] Body is valid JSON
- [ ] No extra/malformed headers

### ✅ Error Handling
- [ ] Invalid JSON → 200 with error message ✓
- [ ] Route not found → 404 ✓
- [ ] Server exception → 500 ✓
- [ ] Connection closes properly ✓

### ✅ Flow
- [ ] CTRL+C stops backend gracefully ✓
- [ ] Multiple requests handled correctly
- [ ] No memory leaks (check if processes accumulate)
- [ ] Logging is clear and helpful

---

## 🐛 TROUBLESHOOTING

### Issue: Backend doesn't start
**Solution:** Check if port 9000 is already in use
```bash
netstat -ano | findstr :9000
# Kill the process if found
taskkill /PID <PID> /F
```

### Issue: Thunder shows "Connection refused"
**Solution:** Backend not running or crashed
- Check console output
- Restart backend with `python start_sampleapp.py`

### Issue: Response is 500 error
**Solution:** Check console output for exception
- Look at `[HttpAdapter] Error handling client` message
- Check if route handler has bugs
- Check if request body is valid

### Issue: Cookies not parsed
**Solution:** Need to add cookie in request header
```
Cookie: sessionId=abc123; userId=456
```

### Issue: Body not extracted
**Solution:** Check Content-Length header
- Must match actual body length
- Thunder usually sets it automatically

---

## 📝 NEXT STEPS (if time allows)

1. [ ] Add more endpoints to sampleApp
2. [ ] Add database integration
3. [ ] Add authentication middleware
4. [ ] Add request validation
5. [ ] Add response caching
6. [ ] Add API documentation (Swagger)

---

## ✨ SUCCESS CRITERIA

✅ All 5 tests pass
✅ Console shows proper logging
✅ Response status codes are correct
✅ Response bodies are valid JSON
✅ No crashes or errors
✅ CTRL+C stops server gracefully
✅ Multiple sequential requests work
✅ Concurrent requests work (multiple Thunder instances)

---

**Happy Testing! 🎉**
