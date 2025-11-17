/**
 * P2P Chat Client - Node.js Implementation
 * 
 * This client handles:
 * 1. TCP server for receiving P2P connections
 * 2. TCP client for connecting to other peers  
 * 3. HTTP communication with WeApRous server (tracker)
 * 4. WebSocket server for browser UI communication
 */

const net = require('net');
const http = require('http');
const WebSocket = require('ws');
const readline = require('readline');

class P2PClient {
    constructor(username, serverHost = '127.0.0.1', serverPort = 8000) {
        this.username = username;
        this.serverHost = serverHost;
        this.serverPort = serverPort;
        
        // P2P Network
        this.p2pPort = null;
        this.p2pServer = null;
        this.peerConnections = new Map(); // username -> socket
        
        // Known peers from tracker
        this.knownPeers = new Map(); // username -> {ip, port}
        
        // WebSocket for browser UI
        this.wsServer = null;
        this.wsPort = null; // Will be auto-allocated
        this.browserClient = null;
        
        // Message history
        this.messageHistory = [];
    }

    /**
     * Start P2P client
     */
    async start() {
        console.log(`🚀 Starting P2P Client for user: ${this.username}`);
        
        try {
            // 1. Start P2P TCP server
            await this.startP2PServer();
            
            // 2. Register with tracker
            await this.registerWithTracker();
            
            // 3. Start WebSocket server for browser UI
            await this.startWebSocketServer();
            
            // 4. Setup CLI
            this.setupCLI();
            
            console.log(`\n${'='.repeat(60)}`);
            console.log(`✅ P2P Client ready!`);
            console.log(`${'='.repeat(60)}`);
            console.log(`   👤 User: ${this.username}`);
            console.log(`   🔗 P2P Server: localhost:${this.p2pPort}`);
            console.log(`   🌐 WebSocket: ws://localhost:${this.wsPort}`);
            console.log(`${'='.repeat(60)}`);
            console.log(`\n📱 To connect browser UI:`);
            console.log(`   1. Open: http://127.0.0.1:8000/p2p_integrated.html`);
            console.log(`   2. Enter username: ${this.username}`);
            console.log(`   3. Enter WebSocket port: ${this.wsPort}`);
            console.log(`\n💬 CLI Commands: Type 'help' for available commands\n`);
            
        } catch (error) {
            console.error('❌ Failed to start P2P client:', error);
            process.exit(1);
        }
    }

    /**
     * Start TCP server for P2P connections
     */
    startP2PServer() {
        return new Promise((resolve, reject) => {
            this.p2pServer = net.createServer((socket) => {
                console.log(`📡 Incoming P2P connection from ${socket.remoteAddress}:${socket.remotePort}`);
                this.handleIncomingPeerConnection(socket);
            });

            // Find available port
            this.p2pServer.listen(0, '0.0.0.0', () => {
                this.p2pPort = this.p2pServer.address().port;
                console.log(`🔗 P2P Server listening on port ${this.p2pPort}`);
                resolve();
            });

            this.p2pServer.on('error', reject);
        });
    }

    /**
     * Handle incoming P2P connection
     */
    handleIncomingPeerConnection(socket) {
        let peerUsername = null;
        let buffer = '';

        socket.on('data', (data) => {
            buffer += data.toString();
            
            // Process complete messages (ending with newline)
            let messages = buffer.split('\n');
            buffer = messages.pop(); // Keep incomplete message in buffer
            
            messages.forEach(msgStr => {
                if (!msgStr.trim()) return;
                
                try {
                    const message = JSON.parse(msgStr);
                
                if (message.type === 'handshake') {
                    peerUsername = message.from;
                    this.peerConnections.set(peerUsername, socket);
                    console.log(`🤝 Handshake with peer: ${peerUsername}`);
                    
                    // Send handshake response
                    socket.write(JSON.stringify({
                        type: 'handshake_response',
                        from: this.username,
                        status: 'connected'
                    }) + '\n');
                    
                    // Notify browser if connected
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'peer_connected',
                            peer: peerUsername
                        }));
                    }
                    
                } else if (message.type === 'direct_message') {
                    console.log(`💬 Direct message from ${message.from}: ${message.message}`);
                    
                    // Store message
                    const msgData = {
                        type: 'direct',
                        from: message.from,
                        to: this.username,
                        message: message.message,
                        timestamp: message.timestamp || new Date().toISOString(),
                        source: 'p2p'
                    };
                    this.messageHistory.push(msgData);
                    
                    // Forward to browser if connected
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'new_message',
                            message: msgData
                        }));
                    }
                }
                
                } catch (error) {
                    console.error('Error parsing P2P message:', error);
                }
            });
        });

        socket.on('close', () => {
            if (peerUsername) {
                console.log(`🔌 Peer disconnected: ${peerUsername}`);
                this.peerConnections.delete(peerUsername);
            }
        });

        socket.on('error', (error) => {
            console.error('P2P socket error:', error);
        });
    }

    /**
     * Register with WeApRous tracker
     */
    async registerWithTracker() {
        const data = JSON.stringify({
            username: this.username,
            p2p_port: this.p2pPort
        });

        return new Promise((resolve, reject) => {
            const req = http.request({
                hostname: this.serverHost,
                port: this.serverPort,
                path: '/submit-info',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': data.length
                }
            }, (res) => {
                let body = '';
                res.on('data', chunk => body += chunk);
                res.on('end', () => {
                    try {
                        const response = JSON.parse(body);
                        if (response.status === 'ok') {
                            console.log(`📋 Registered with tracker: ${JSON.stringify(response.peer)}`);
                            resolve(response);
                        } else {
                            reject(new Error(`Registration failed: ${response.message}`));
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }

    /**
     * Connect to another peer directly
     */
    async connectToPeer(peerUsername) {
        if (peerUsername === this.username) {
            console.log(`❌ Cannot connect to yourself`);
            return;
        }
        
        if (this.peerConnections.has(peerUsername)) {
            console.log(`Already connected to ${peerUsername}`);
            return;
        }

        // Get peer info from tracker
        const peerInfo = await this.getPeerInfo(peerUsername);
        if (!peerInfo) {
            console.log(`❌ Peer ${peerUsername} not found`);
            return;
        }

        console.log(`🔗 Connecting to ${peerUsername} at ${peerInfo.ip}:${peerInfo.port}`);

        return new Promise((resolve, reject) => {
            const socket = net.connect(peerInfo.port, peerInfo.ip, () => {
                console.log(`✅ Connected to peer: ${peerUsername}`);
                
                // Send handshake
                socket.write(JSON.stringify({
                    type: 'handshake',
                    from: this.username
                }) + '\n');
                
                this.peerConnections.set(peerUsername, socket);
                resolve();
            });

            let buffer = '';
            socket.on('data', (data) => {
                buffer += data.toString();
                
                let messages = buffer.split('\n');
                buffer = messages.pop();
                
                messages.forEach(msgStr => {
                    if (!msgStr.trim()) return;
                    
                    try {
                        const message = JSON.parse(msgStr);
                        if (message.type === 'handshake_response') {
                            console.log(`🤝 Handshake confirmed with ${peerUsername}`);
                            
                            // Notify browser
                            if (this.browserClient) {
                                this.browserClient.send(JSON.stringify({
                                    type: 'peer_connected',
                                    peer: peerUsername
                                }));
                            }
                        } else if (message.type === 'direct_message') {
                            console.log(`💬 Direct message from ${message.from}: ${message.message}`);
                            
                            // Store and forward to browser
                            const msgData = {
                                type: 'direct',
                                from: message.from,
                                to: this.username,
                                message: message.message,
                                timestamp: message.timestamp || new Date().toISOString(),
                                source: 'p2p'
                            };
                            this.messageHistory.push(msgData);
                            
                            if (this.browserClient) {
                                this.browserClient.send(JSON.stringify({
                                    type: 'new_message',
                                    message: msgData
                                }));
                            }
                        }
                    } catch (error) {
                        console.error('Error parsing peer response:', error);
                    }
                });
            });

            socket.on('error', (error) => {
                console.error(`❌ Failed to connect to ${peerUsername}:`, error);
                reject(error);
            });

            socket.on('close', () => {
                console.log(`🔌 Disconnected from ${peerUsername}`);
                this.peerConnections.delete(peerUsername);
            });
        });
    }

    /**
     * Get peer info from tracker
     */
    async getPeerInfo(peerUsername) {
        const data = JSON.stringify({
            from: this.username,
            to: peerUsername
        });

        return new Promise((resolve, reject) => {
            const req = http.request({
                hostname: this.serverHost,
                port: this.serverPort,
                path: '/connect-peer',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': data.length
                }
            }, (res) => {
                let body = '';
                res.on('data', chunk => body += chunk);
                res.on('end', () => {
                    try {
                        const response = JSON.parse(body);
                        if (response.status === 'ok') {
                            resolve(response.to);
                        } else {
                            resolve(null);
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }

    /**
     * Get all available peers from tracker
     */
    async getAllPeers() {
        return new Promise((resolve, reject) => {
            const req = http.request({
                hostname: this.serverHost,
                port: this.serverPort,
                path: '/get-list',
                method: 'GET'
            }, (res) => {
                let body = '';
                res.on('data', chunk => body += chunk);
                res.on('end', () => {
                    try {
                        const response = JSON.parse(body);
                        if (response.status === 'ok') {
                            resolve(response.peers);
                        } else {
                            resolve([]);
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.end();
        });
    }

    /**
     * Send direct message to peer via P2P
     */
    async sendDirectMessage(peerUsername, message) {
        // Connect to peer if not already connected
        if (!this.peerConnections.has(peerUsername)) {
            try {
                await this.connectToPeer(peerUsername);
            } catch (error) {
                console.error(`Failed to connect to ${peerUsername}:`, error);
                return false;
            }
        }

        const socket = this.peerConnections.get(peerUsername);
        if (!socket) {
            console.error(`No connection to ${peerUsername}`);
            return false;
        }

        const messageData = {
            type: 'direct_message',
            from: this.username,
            to: peerUsername,
            message: message,
            timestamp: new Date().toISOString()
        };

        socket.write(JSON.stringify(messageData) + '\n');
        
        // Store in local history
        this.messageHistory.push({
            ...messageData,
            source: 'p2p_sent'
        });

        console.log(`📤 Sent direct message to ${peerUsername}: ${message}`);
        return true;
    }

    /**
     * Start WebSocket server for browser UI
     */
    startWebSocketServer() {
        return new Promise((resolve, reject) => {
            // Auto-allocate WebSocket port (start from 9200)
            this.wsServer = new WebSocket.Server({ port: 0 });
            
            this.wsServer.on('listening', () => {
                this.wsPort = this.wsServer.address().port;
                console.log(`🌐 WebSocket server listening on port ${this.wsPort}`);
                resolve();
            });
            
            this.wsServer.on('error', (error) => {
                console.error('WebSocket server error:', error);
                reject(error);
            });
            
            this.wsServer.on('connection', (ws) => {
                console.log('🌐 Browser connected to WebSocket');
                this.browserClient = ws;
                
                ws.on('message', async (data) => {
                    try {
                        const command = JSON.parse(data);
                        await this.handleBrowserCommand(command);
                    } catch (error) {
                        console.error('WebSocket message error:', error);
                    }
                });
                
                ws.on('close', () => {
                    console.log('🌐 Browser disconnected');
                    this.browserClient = null;
                });
            });
        });
    }

    /**
     * Handle commands from browser
     */
    async handleBrowserCommand(command) {
        switch (command.type) {
            case 'send_message':
            case 'send_direct_message':
                // Handle both old and new command types
                const targetUser = command.to || command.username;
                const message = command.message;
                if (targetUser && message) {
                    await this.sendDirectMessage(targetUser, message);
                    
                    // Notify browser of successful send
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'new_message',
                            message: {
                                from: this.username,
                                to: targetUser,
                                message: message,
                                timestamp: new Date().toISOString(),
                                source: 'p2p_sent'
                            }
                        }));
                    }
                }
                break;
                
            case 'broadcast_message':
                // Broadcast to all connected peers
                const broadcastMsg = command.message;
                const connectedPeers = Array.from(this.peerConnections.keys());
                
                if (connectedPeers.length === 0) {
                    console.log(`⚠️ No connected peers to broadcast to`);
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'error',
                            message: 'No connected peers to broadcast to'
                        }));
                    }
                    break;
                }
                
                for (const peerUsername of connectedPeers) {
                    await this.sendDirectMessage(peerUsername, broadcastMsg);
                }
                
                console.log(`📢 Broadcast message to ${connectedPeers.length} peers: "${broadcastMsg}"`);
                
                // Notify browser of broadcast sent
                if (this.browserClient) {
                    this.browserClient.send(JSON.stringify({
                        type: 'broadcast_sent',
                        peers: connectedPeers,
                        message: broadcastMsg
                    }));
                }
                break;
                
            case 'connect_peer':
                try {
                    await this.connectToPeer(command.username);
                    // Notify browser of successful connection
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'peer_connected',
                            peer: command.username
                        }));
                    }
                } catch (error) {
                    console.error(`Failed to connect to ${command.username}:`, error);
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'error',
                            message: `Failed to connect to ${command.username}`
                        }));
                    }
                }
                break;
                
            case 'get_message_history':
                if (this.browserClient) {
                    this.browserClient.send(JSON.stringify({
                        type: 'message_history',
                        messages: this.messageHistory
                    }));
                }
                break;
                
            case 'get_peers':
                try {
                    const peers = await this.getAllPeers();
                    // Filter to show only P2P peers, excluding self
                    const p2pPeers = peers.filter(p => 
                        p.client_type === 'p2p' && p.username !== this.username
                    );
                    
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'peers',
                            peers: p2pPeers,
                            connected: Array.from(this.peerConnections.keys())
                        }));
                    }
                } catch (error) {
                    console.error('Failed to get peer list:', error);
                }
                break;
                
            case 'auto_connect_peers':
                // Auto-connect to all available P2P peers
                try {
                    const peers = await this.getAllPeers();
                    const p2pPeers = peers.filter(p => 
                        p.client_type === 'p2p' && 
                        p.username !== this.username &&
                        !this.peerConnections.has(p.username)
                    );
                    
                    console.log(`🔗 Auto-connecting to ${p2pPeers.length} peers...`);
                    
                    for (const peer of p2pPeers) {
                        try {
                            await this.connectToPeer(peer.username);
                        } catch (error) {
                            console.error(`Failed to connect to ${peer.username}:`, error);
                        }
                    }
                    
                    // Send updated peer list
                    if (this.browserClient) {
                        this.browserClient.send(JSON.stringify({
                            type: 'peers',
                            peers: p2pPeers,
                            connected: Array.from(this.peerConnections.keys())
                        }));
                    }
                } catch (error) {
                    console.error('Failed to auto-connect peers:', error);
                }
                break;
        }
    }

    /**
     * Setup CLI for testing
     */
    setupCLI() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        rl.on('line', async (input) => {
            const [command, ...args] = input.trim().split(' ');
            
            switch (command) {
                case 'help':
                    console.log('Commands:');
                    console.log('  list - Show available P2P peers from server');
                    console.log('  peers - Show currently connected peers');
                    console.log('  connect <username> - Connect to peer');
                    console.log('  send <username> <message> - Send direct message');
                    console.log('  broadcast <message> - Broadcast message to all connected peers');
                    console.log('  info - Show client information');
                    console.log('  history - Show message history');
                    console.log('  quit - Exit');
                    break;
                    
                case 'connect':
                    if (args[0]) {
                        await this.connectToPeer(args[0]);
                    }
                    break;
                    
                case 'send':
                    if (args.length >= 2) {
                        const username = args[0];
                        const message = args.slice(1).join(' ');
                        await this.sendDirectMessage(username, message);
                    }
                    break;
                    
                case 'broadcast':
                    if (args.length >= 1) {
                        const message = args.join(' ');
                        const connectedPeers = Array.from(this.peerConnections.keys());
                        
                        if (connectedPeers.length === 0) {
                            console.log('❌ No connected peers to broadcast to');
                            break;
                        }
                        
                        for (const peerUsername of connectedPeers) {
                            await this.sendDirectMessage(peerUsername, message);
                        }
                        
                        console.log(`📢 Broadcast message to ${connectedPeers.length} peers: "${message}"`);
                    } else {
                        console.log('Usage: broadcast <message>');
                    }
                    break;
                    
                case 'peers':
                    console.log('Connected peers:', Array.from(this.peerConnections.keys()));
                    break;
                    
                case 'list':
                    try {
                        const peers = await this.getAllPeers();
                        const availablePeers = peers.filter(p => p.username !== this.username && p.client_type === 'p2p');
                        console.log('Available P2P peers:');
                        if (availablePeers.length === 0) {
                            console.log('  No other P2P peers found');
                        } else {
                            availablePeers.forEach(peer => {
                                const status = this.peerConnections.has(peer.username) ? ' (connected)' : '';
                                console.log(`  ${peer.username} - ${peer.ip}:${peer.port}${status}`);
                            });
                        }
                    } catch (error) {
                        console.log('Failed to fetch peer list:', error.message);
                    }
                    break;
                    
                case 'info':
                    console.log(`User: ${this.username}`);
                    console.log(`P2P Server: localhost:${this.p2pPort}`);
                    console.log(`WebSocket: ws://localhost:${this.wsPort}`);
                    console.log(`Connected peers: ${this.peerConnections.size}`);
                    break;
                    
                case 'history':
                    this.messageHistory.forEach(msg => {
                        console.log(`[${msg.timestamp}] ${msg.from} -> ${msg.to}: ${msg.message} (${msg.source})`);
                    });
                    break;
                    
                case 'quit':
                    process.exit(0);
                    break;
                    
                default:
                    console.log('Unknown command. Type "help" for available commands.');
            }
        });
    }
}

// Command line usage
if (require.main === module) {
    const username = process.argv[2];
    if (!username) {
        console.log('Usage: node p2p_client.js <username>');
        process.exit(1);
    }
    
    const client = new P2PClient(username);
    client.start().catch(console.error);
}

module.exports = P2PClient;