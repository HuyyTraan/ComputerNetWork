# WeApRous P2P Implementation

## 🎯 True P2P Chat System

This branch implements **True Peer-to-Peer** chat where clients connect directly to each other, bypassing the server for direct messages.

## 📋 Architecture

```
Node.js Client A ←──TCP P2P──→ Node.js Client B
        ↓                              ↓
    WebSocket                      WebSocket
        ↓                              ↓
   Browser UI A                   Browser UI B
        ↓                              ↓
        └──────── HTTP ────────────────┘
                    ↓
              WeApRous Server
                (Tracker)
```

### Components:

1. **WeApRous Server (Tracker)**

   - Manages peer discovery (`/submit-info`, `/get-list`, `/connect-peer`)
   - Handles broadcast messages
   - Stores offline messages

2. **Node.js P2P Client**

   - TCP Server: Listens for incoming peer connections
   - TCP Client: Connects to other peers directly
   - WebSocket Server: Communicates with browser UI
   - CLI: Command-line interface for testing

3. **Browser UI**
   - Connects to Node.js client via WebSocket
   - Same HTML interface as before
   - Direct messages routed through P2P

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Test Environment

```bash
# Windows
start_p2p_test.bat

# Manual start
python start_app.py                # WeApRous server
node p2p_client.js alice          # P2P client for Alice
node p2p_client.js bob            # P2P client for Bob
```

### 3. Test P2P Communication

**In Alice terminal:**

```
connect bob
send bob Hello from Alice!
```

**In Bob terminal:**

```
connect alice
send alice Hi Alice, this is Bob!
```

### 4. Browser UI (Optional)

- Open: http://127.0.0.1:8000/chat.html
- Connect WebSocket to P2P client for GUI

## 🔧 P2P Client Commands

| Command             | Description              | Example           |
| ------------------- | ------------------------ | ----------------- |
| `help`              | Show available commands  | `help`            |
| `connect <user>`    | Connect to peer directly | `connect bob`     |
| `send <user> <msg>` | Send direct P2P message  | `send bob Hello!` |
| `peers`             | List connected peers     | `peers`           |
| `history`           | Show message history     | `history`         |
| `quit`              | Exit client              | `quit`            |

## 📡 Message Flow

### Direct Messages (P2P):

```
Alice → TCP Socket → Bob (Direct)
```

### Broadcast Messages (Server):

```
Alice → HTTP → Server → HTTP → Bob
```

## 🔍 Differences from Fake P2P

| Aspect               | Fake P2P (main branch) | True P2P (this branch) |
| -------------------- | ---------------------- | ---------------------- |
| **Direct Messages**  | Via HTTP server        | Direct TCP connection  |
| **Client Type**      | Browser only           | Node.js + Browser      |
| **Real-time**        | Polling (5s)           | Instant TCP            |
| **Server Load**      | High (all messages)    | Low (tracker only)     |
| **Offline Messages** | Server storage         | Server backup          |

## 🎯 Testing Scenarios

### Scenario 1: CLI P2P Chat

1. Start 2 P2P clients
2. Connect peers using `connect` command
3. Send direct messages using `send` command
4. Verify messages arrive instantly

### Scenario 2: Mixed Environment

1. P2P client (Alice) + Browser client (Bob)
2. Alice sends direct message to Bob
3. Bob receives via server (not P2P capable)
4. Bob sends broadcast to Alice
5. Alice receives broadcast via server

### Scenario 3: Network Discovery

1. Start multiple P2P clients
2. Use `/get-list` API to discover peers
3. Auto-connect to all available peers
4. Test multi-peer chat

## 🐛 Troubleshooting

### Port Conflicts

- P2P clients auto-allocate TCP ports
- WebSocket server uses port 9200+
- Check `netstat -an` for port usage

### Connection Issues

```bash
# Check if peer is reachable
telnet <peer_ip> <peer_port>

# Check WebSocket connection
# Browser console: new WebSocket('ws://localhost:9200')
```

### Server Communication

```bash
# Test tracker API
curl -X POST http://127.0.0.1:8000/submit-info \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "p2p_port": 9300}'
```

## 📝 Implementation Notes

- **TCP Protocol**: Custom JSON-based message protocol
- **WebSocket Integration**: Bridge between browser and P2P client
- **Error Handling**: Robust connection management and retries
- **Scalability**: Direct P2P scales better than centralized server
- **Security**: No encryption in this demo (production needs TLS)

## 🚀 Next Steps

1. **Browser WebSocket Integration**: Connect chat.html to P2P client
2. **Message Sync**: Synchronize P2P and server messages
3. **Peer Discovery**: Auto-connect to available peers
4. **File Transfer**: P2P file sharing capabilities
5. **Encryption**: Secure P2P communication
