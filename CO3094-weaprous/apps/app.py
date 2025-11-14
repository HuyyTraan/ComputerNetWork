#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#
# WeApRous release - Task 1A: Authentication Handling
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

"""
apps.app
~~~~~~~~~

Task 1A: Authentication Handling

This application demonstrates authentication with login validation and session management
using Set-Cookie headers.

Routes:
    GET /           - Return welcome message (simulating index page)
    POST /login     - Validate credentials and set auth cookie
    
Features:
    - Header parsing from HTTP requests
    - Session management via Set-Cookie headers
    - Error handling (401 Unauthorized for invalid credentials)
    - Concurrency support (handled by backend threading)
"""

import json
import argparse
import datetime
from daemon.weaprous import WeApRous

PORT = 9000  # Default port

app = WeApRous()

# ============================================================================
# Task 1A: Authentication Routes
# ============================================================================

# Simulated database (in production: Redis, PostgreSQL, etc.)
SESSIONS = {
    "abc123def456": {
        "username": "admin",
        "created_at": "2025-11-12 10:00:00",
        "expires_at": "2025-11-12 11:00:00"
    }
}

@app.route('/', methods=['GET'])
def index(request=None, body=""):
    """
    Task 1B: Cookie-based access control with session validation
    """
    print("[App] GET / - checking authentication via cookie")
    
    # Check if auth cookie exists
    if request and hasattr(request, 'cookies') and request.cookies:
        auth_cookie = request.cookies.get('auth', '')
        sessionid = request.cookies.get('sessionid', '')
        username = request.cookies.get('username', '')
        
        print(f"[App] Cookies found: auth={auth_cookie}, sessionid={sessionid}, username={username}")
        
        # Task 1B: Check auth flag AND validate sessionid
        if auth_cookie == 'true' and sessionid in SESSIONS:
            session_data = SESSIONS[sessionid]
            print(f"[App] Valid session found for user: {session_data['username']}")
            
            return (200, {
                "page": "index",
                "message": "Welcome to the RESTful TCP WebApp",
                "status": "You are viewing the index page",
                "authenticated": True,
                "user": session_data['username']
            })
        elif auth_cookie == 'true':
            print(f"[App] Invalid sessionid: {sessionid}")
            return (401, {
                "status": "unauthorized",
                "message": "Session invalid or expired",
                "authenticated": False
            })
        else:
            print(f"[App] Invalid auth cookie: {auth_cookie}")
            return (401, {
                "status": "unauthorized",
                "message": "Invalid or missing auth cookie",
                "authenticated": False
            })
    else:
        print("[App] No auth cookie found")
        return (401, {
            "status": "unauthorized",
            "message": "Auth cookie required. Please login first.",
            "authenticated": False
        })


@app.route('/login', methods=['POST'])
def login(request=None, body=""):
    """
    Handle user login via POST request.
    
    Task 1A: Validate credentials (username=admin, password=password)
    - If valid: Return 200 OK with Set-Cookie header
    - If invalid: Return 401 Unauthorized
    
    :param request: Request object containing headers, body, cookies, etc.
    :param body (str): Request body containing login credentials (JSON)
    :return: (status_code, data) or (status_code, data, cookies_dict)
    
    Response Format:
        Success (200):
            - Status: 200 OK
            - Body: {"status": "logged_in", "message": "..."}
            - Headers: Set-Cookie headers with auth=true, sessionid, username
        
        Failure (401):
            - Status: 401 Unauthorized
            - Body: {"status": "unauthorized", "message": "..."}
    """
    print("[App] POST /login - processing authentication request")
    
    try:
        # Get request body
        actual_body = body
        if request and hasattr(request, 'body'):
            actual_body = request.body
        
        # Parse request body
        if not actual_body or not actual_body.strip():
            print("[App] Login failed: Empty body")
            return (401, {"status": "unauthorized", "message": "Missing credentials"})
        
        credentials = json.loads(actual_body)
        username = credentials.get("username", "")
        password = credentials.get("password", "")
        
        print(f"[App] Login attempt: username='{username}'")
        
        # Task 1A: Validate credentials
        # Valid credentials: username=admin, password=password
        if username == "admin" and password == "password":
            print("[App] Login successful - valid credentials")
            # Return with Set-Cookie header
            # Format: (status_code, data, cookies_dict)
            cookies = {
                "auth": "true",
                "sessionid": "abc123def456",
                "username": username
            }
            return (200, {
                "status": "logged_in",
                "message": "Authentication successful",
                "username": username,
                "auth": True
            }, cookies)
        else:
            print(f"[App] Login failed - invalid credentials (username={username})")
            return (401, {
                "status": "unauthorized",
                "message": "Invalid username or password",
                "auth": False
            })
    
    except json.JSONDecodeError as e:
        print(f"[App] Login failed: Invalid JSON - {e}")
        return (401, {
            "status": "unauthorized",
            "message": "Invalid JSON format in request body"
        })
    except Exception as e:
        print(f"[App] Login error: {e}")
        return (500, {
            "status": "error",
            "message": "Internal server error during login"
        })




# ============================================================================
# Task 2.2 - Hybrid Chat Application (simple implementation)
# ============================================================================

# Lưu thông tin peer đã đăng ký
CHAT_PEERS = {}          # username -> {"ip": "...", "port": 1234, "last_seen": "..."}
# Lưu message theo channel
CHAT_CHANNELS = {}       # channel -> [ {from, type, to, message, timestamp}, ... ]
# Lưu thành viên channel
CHAT_CHANNEL_MEMBERS = {}   # channel -> set(usernames)


def _chat_ensure_channel(name: str):
    """Đảm bảo channel tồn tại trong CHAT_CHANNELS & CHAT_CHANNEL_MEMBERS."""
    if name not in CHAT_CHANNELS:
        CHAT_CHANNELS[name] = []
    if name not in CHAT_CHANNEL_MEMBERS:
        CHAT_CHANNEL_MEMBERS[name] = set()


def _chat_read_json_body(request, body: str):
    """
    Helper: lấy JSON body (dùng cho mọi route Task 2.2)
    - Ưu tiên request.body nếu có
    - Hỗ trợ bytes / str
    """
    raw = body
    if request is not None and getattr(request, "body", None):
        raw = request.body

    if not raw:
        raise ValueError("Empty body")

    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")

    return json.loads(raw)


# ------------------------- Initialization phase -----------------------------

@app.route("/submit-info", methods=["POST"])
def chat_submit_info(request=None, body=""):
    """
    Đăng ký peer với tracker.
    Body JSON:
        {
            "username": "alice",
            "ip": "127.0.0.1",
            "port": 9001
        }
    """
    print("[Chat] /submit-info")

    try:
        data = _chat_read_json_body(request, body)
        username = data.get("username")
        ip = data.get("ip")
        port = data.get("port")

        if not username or not ip or port is None:
            return (400, {
                "status": "bad_request",
                "message": "username, ip, port are required"
            })

        CHAT_PEERS[username] = {
            "ip": ip,
            "port": int(port),
            "last_seen": datetime.datetime.utcnow().isoformat() + "Z",
        }

        print(f"[Chat] Registered peer {username} @ {ip}:{port}")
        return (200, {
            "status": "ok",
            "peer": CHAT_PEERS[username]
        })

    except Exception as e:
        print("[Chat] /submit-info error:", e)
        return (500, {"status": "error", "message": str(e)})


@app.route("/add-list", methods=["POST"])
def chat_add_list(request=None, body=""):
    """
    Peer join 1 channel.
    Body JSON:
        {
            "username": "alice",
            "channel": "general"
        }
    """
    print("[Chat] /add-list")

    try:
        data = _chat_read_json_body(request, body)
        username = data.get("username")
        channel = data.get("channel", "general")

        if not username:
            return (400, {
                "status": "bad_request",
                "message": "username is required"
            })

        # Nếu peer chưa submit-info thì auto thêm với ip/port default
        if username not in CHAT_PEERS:
            CHAT_PEERS[username] = {
                "ip": "0.0.0.0",
                "port": 0,
                "last_seen": datetime.datetime.utcnow().isoformat() + "Z",
            }

        _chat_ensure_channel(channel)
        CHAT_CHANNEL_MEMBERS[channel].add(username)

        print(f"[Chat] {username} joined channel {channel}")

        return (200, {
            "status": "ok",
            "channel": channel,
            "members": sorted(list(CHAT_CHANNEL_MEMBERS[channel]))
        })

    except Exception as e:
        print("[Chat] /add-list error:", e)
        return (500, {"status": "error", "message": str(e)})


@app.route("/get-list", methods=["GET"])
def chat_get_list(request=None, body=""):
    """
    Trả về danh sách peer & channel.
    Response:
        {
            "status": "ok",
            "peers": [...],
            "channels": [...]
        }
    """
    print("[Chat] /get-list")

    peers_out = []
    for username, info in CHAT_PEERS.items():
        peers_out.append({
            "username": username,
            "ip": info.get("ip", "0.0.0.0"),
            "port": info.get("port", 0),
            "channels": [
                ch for ch, members in CHAT_CHANNEL_MEMBERS.items()
                if username in members
            ]
        })

    channels = sorted(CHAT_CHANNELS.keys())

    return (200, {
        "status": "ok",
        "peers": peers_out,
        "channels": channels
    })

@app.route("/connect-peer", methods=["POST"])
def chat_connect_peer(request=None, body=""):
    """
    API hỗ trợ bước 'Connection setup'.
    Body JSON:
        {
            "from": "alice",
            "to": "bob"
        }
    Trả về thông tin IP/port của peer 'to'.
    """
    print("[Chat] /connect-peer")
    try:
        data = _chat_read_json_body(request, body)
        from_user = data.get("from")
        to_user = data.get("to")

        if not from_user or not to_user:
            return (400, {
                "status": "bad_request",
                "message": "from and to are required"
            })

        if to_user not in CHAT_PEERS:
            return (404, {
                "status": "not_found",
                "message": f"Peer {to_user} not found"
            })

        target = CHAT_PEERS[to_user]
        return (200, {
            "status": "ok",
            "from": from_user,
            "to": {
                "username": to_user,
                "ip": target.get("ip", "0.0.0.0"),
                "port": target.get("port", 0)
            }
        })

    except Exception as e:
        print("[Chat] /connect-peer error:", e)
        return (500, {"status": "error", "message": str(e)})

# --------------------------- Chatting phase ---------------------------------

@app.route("/broadcast-peer", methods=["POST"])
def chat_broadcast_peer(request=None, body=""):
    """
    Gửi message broadcast trong 1 channel.
    Body JSON:
        {
            "from": "alice",
            "channel": "general",
            "message": "hello"
        }
    """
    print("[Chat] /broadcast-peer")

    try:
        data = _chat_read_json_body(request, body)
        sender = data.get("from")
        channel = data.get("channel", "general")
        message = data.get("message", "")

        if not sender or not message:
            return (400, {
                "status": "bad_request",
                "message": "from and message are required"
            })

        _chat_ensure_channel(channel)
        event = {
            "type": "broadcast",
            "from": sender,
            "to": None,
            "channel": channel,
            "message": message,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        CHAT_CHANNELS[channel].append(event)

        print(f"[Chat] broadcast in {channel} by {sender}: {message}")

        return (200, {
            "status": "sent",
            "channel": channel,
            "message": event
        })

    except Exception as e:
        print("[Chat] /broadcast-peer error:", e)
        return (500, {"status": "error", "message": str(e)})


@app.route("/send-peer", methods=["POST"])
def chat_send_peer(request=None, body=""):
    """
    Gửi message direct (logic).
    Body JSON:
        {
            "from": "alice",
            "to": "bob",
            "channel": "general",
            "message": "hi"
        }
    """
    print("[Chat] /send-peer")

    try:
        data = _chat_read_json_body(request, body)
        sender = data.get("from")
        receiver = data.get("to")
        channel = data.get("channel", "direct")
        message = data.get("message", "")

        if not sender or not receiver or not message:
            return (400, {
                "status": "bad_request",
                "message": "from, to and message are required"
            })

        _chat_ensure_channel(channel)
        event = {
            "type": "direct",
            "from": sender,
            "to": receiver,
            "channel": channel,
            "message": message,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        CHAT_CHANNELS[channel].append(event)

        print(f"[Chat] direct {sender} -> {receiver} in {channel}: {message}")

        return (200, {
            "status": "sent",
            "channel": channel,
            "message": event
        })

    except Exception as e:
        print("[Chat] /send-peer error:", e)
        return (500, {"status": "error", "message": str(e)})


@app.route("/channel/messages", methods=["POST"])
def chat_channel_messages(request=None, body=""):
    """
    Lấy tất cả message trong 1 channel.
    Body JSON:
        {
            "channel": "general"
        }
    """
    print("[Chat] /channel/messages")

    try:
        data = _chat_read_json_body(request, body)
        channel = data.get("channel", "general")

        _chat_ensure_channel(channel)

        return (200, {
            "status": "ok",
            "channel": channel,
            "messages": CHAT_CHANNELS[channel]
        })

    except Exception as e:
        print("[Chat] /channel/messages error:", e)
        return (500, {"status": "error", "message": str(e)})

# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    # Parse command-line arguments to configure server IP and port
    parser = argparse.ArgumentParser(
        prog='Task1A-App',
        description='WeApRous - Task 1A: Authentication Handling',
        epilog='Daemon for handling HTTP requests with authentication'
    )
    parser.add_argument('--server-ip', default='0.0.0.0', help='Server IP address')
    parser.add_argument('--server-port', type=int, default=PORT, help='Server port')
    
    args = parser.parse_args()
    ip = args.server_ip
    port = args.server_port
    
    print(f"\n{'='*60}")
    print(f"Task 1A: Authentication Handling")
    print(f"{'='*60}")
    print(f"Server: {ip}:{port}")
    print(f"Routes:")
    print(f"  - GET  /        (index page)")
    print(f"  - POST /login   (authentication)")
    print(f"{'='*60}\n")
    
    # Prepare and launch the application
    app.prepare_address(ip, port)
    app.run()
