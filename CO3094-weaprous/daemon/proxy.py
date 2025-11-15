#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

"""
daemon.proxy
~~~~~~~~~~~~~~~~~

This module implements a simple proxy server using Python's socket and threading libraries.
It routes incoming HTTP requests to backend services based on hostname mappings and returns
the corresponding responses to clients.

Requirement:
-----------------
- socket: provides socket networking interface.
- threading: enables concurrent client handling via threads.
- response: customized :class: `Response <Response>` utilities.
- httpadapter: :class: `HttpAdapter <HttpAdapter >` adapter for HTTP request processing.
- dictionary: :class: `CaseInsensitiveDict <CaseInsensitiveDict>` for managing headers and cookies.

"""
import socket
import threading
import random
from .response import *
from .httpadapter import HttpAdapter
from .dictionary import CaseInsensitiveDict

# Global counter for round-robin load balancing
_round_robin_counter = {}

#: A dictionary mapping hostnames to backend IP and port tuples.
#: Used to determine routing targets for incoming requests.
PROXY_PASS = {
    "127.0.0.1:8080": ('127.0.0.1', 8000),
    "localhost:8080": ('127.0.0.1', 8000),
    "172.16.0.117:8080": ('127.0.0.1', 8000),
    "backend.local": ('127.0.0.1', 9000),
    "app1.local": ('127.0.0.1', 9001),
    "app2.local": ('127.0.0.1', 9002),
}


def forward_request(host, port, request):
    """
    Forwards an HTTP request to a backend server and retrieves the response.

    :params host (str): IP address of the backend server.
    :params port (int): port number of the backend server.
    :params request (str): incoming HTTP request.

    :rtype bytes: Raw HTTP response from the backend server. If the connection
                  fails, returns a 404 Not Found response.
    """

    backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend.settimeout(10)  # 10 second timeout

    try:
        print("[Proxy] Connecting to backend {}:{}".format(host, port))
        backend.connect((host, port))
        print("[Proxy] Connected! Sending request to backend...")
        backend.sendall(request.encode())
        
        response = b""
        while True:
            chunk = backend.recv(4096)
            if not chunk:
                break
            response += chunk
        
        print("[Proxy] Received {} bytes from backend".format(len(response)))
        return response
        
    except socket.timeout:
        print("[Proxy] Timeout connecting to backend {}:{}".format(host, port))
        return (
            "HTTP/1.1 504 Gateway Timeout\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 19\r\n"
            "Connection: close\r\n"
            "\r\n"
            "504 Gateway Timeout"
        ).encode('utf-8')
        
    except socket.error as e:
        print("[Proxy] Socket error connecting to {}:{} - {}".format(host, port, e))
        return (
            "HTTP/1.1 502 Bad Gateway\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 15\r\n"
            "Connection: close\r\n"
            "\r\n"
            "502 Bad Gateway"
        ).encode('utf-8')
        
    finally:
        try:
            backend.close()
        except:
            pass


def resolve_routing_policy(hostname, routes):
    """
    Handles an routing policy to return the matching proxy_pass.
    It determines the target backend to forward the request to.

    :params host (str): IP address of the request target server.
    :params port (int): port number of the request target server.
    :params routes (dict): dictionary mapping hostnames and location.
    """

    print(hostname)
    proxy_map, policy = routes.get(hostname,('127.0.0.1:9000','round-robin'))
    print(proxy_map)
    print(policy)

    proxy_host = ''
    proxy_port = '9000'
    if isinstance(proxy_map, list):
        if len(proxy_map) == 0:
            print("[Proxy] Empty resolved routing of hostname {}".format(hostname))
            print("[Proxy] Applying fallback strategy for unmapped host")
            
            # Fallback strategy: try to route to default backend
            # This allows for graceful degradation instead of hard failure
            fallback_backends = ['127.0.0.1:8000', '127.0.0.1:9000']
            
            for fallback in fallback_backends:
                try:
                    proxy_host, proxy_port = fallback.split(':', 1)
                    print("[Proxy] Using fallback backend: {}".format(fallback))
                    break
                except:
                    continue
            else:
                # Last resort fallback
                proxy_host = '127.0.0.1'
                proxy_port = '8000'
                print("[Proxy] Using last resort fallback: {}:{}".format(proxy_host, proxy_port))
        elif len(proxy_map) == 1:
            proxy_host, proxy_port = proxy_map[0].split(":", 1)
        else:
            # Apply load balancing policy for multiple backends
            if policy == 'round-robin':
                # Round-robin selection
                if hostname not in _round_robin_counter:
                    _round_robin_counter[hostname] = 0
                
                index = _round_robin_counter[hostname] % len(proxy_map)
                selected_backend = proxy_map[index]
                proxy_host, proxy_port = selected_backend.split(":", 1)
                
                _round_robin_counter[hostname] += 1
                print("[Proxy] Round-robin selected backend {}/{}: {}".format(
                    index + 1, len(proxy_map), selected_backend))
                    
            elif policy == 'random':
                # Random selection
                selected_backend = random.choice(proxy_map)
                proxy_host, proxy_port = selected_backend.split(":", 1)
                print("[Proxy] Random selected backend: {}".format(selected_backend))
                
            else:
                # Default to first backend if policy unknown
                proxy_host, proxy_port = proxy_map[0].split(":", 1)
                print("[Proxy] Unknown policy '{}', using first backend".format(policy))
    else:
        print("[Proxy] resolve route of hostname {} is a singulair to".format(hostname))
        proxy_host, proxy_port = proxy_map.split(":", 1)

    return proxy_host, proxy_port

def handle_client(ip, port, conn, addr, routes):
    """
    Handles an individual client connection by parsing the request,
    determining the target backend, and forwarding the request.

    The handler extracts the Host header from the request to
    matches the hostname against known routes. In the matching
    condition,it forwards the request to the appropriate backend.

    The handler sends the backend response back to the client or
    returns 404 if the hostname is unreachable or is not recognized.

    :params ip (str): IP address of the proxy server.
    :params port (int): port number of the proxy server.
    :params conn (socket.socket): client connection socket.
    :params addr (tuple): client address (IP, port).
    :params routes (dict): dictionary mapping hostnames and location.
    """
    
    try:
        # Receive and parse request
        request = conn.recv(1024).decode()
        
        if not request.strip():
            print("[Proxy] {} sent empty request".format(addr))
            conn.close()
            return

        # Extract hostname from Host header
        hostname = None
        for line in request.splitlines():
            if line.lower().startswith('host:'):
                hostname = line.split(':', 1)[1].strip()
                break
        
        if not hostname:
            print("[Proxy] {} missing Host header, using default".format(addr))
            hostname = "127.0.0.1:8000"  # Default fallback
            
        print("[Proxy] {} at Host: {}".format(addr, hostname))
        
        # Resolve the matching destination in routes and convert port to integer
        resolved_host, resolved_port = resolve_routing_policy(hostname, routes)
        try:
            resolved_port = int(resolved_port)
        except ValueError:
            print("[Proxy] Not a valid port integer: {}".format(resolved_port))
            resolved_port = 8000  # Default fallback port

        # Forward request to resolved backend
        if resolved_host:
            print("[Proxy] Host name {} is forwarded to {}:{}".format(hostname, resolved_host, resolved_port))
            response = forward_request(resolved_host, resolved_port, request)        
        else:
            print("[Proxy] No valid backend found for {}".format(hostname))
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "Connection: close\r\n"
                "\r\n"
                "404 Not Found"
            ).encode('utf-8')
        
        # Send response back to client (handle client disconnect gracefully)
        try:
            conn.sendall(response)
            print("[Proxy] Response sent to {}".format(addr))
        except Exception as e:
            print("[Proxy] Error sending response to {}: {}".format(addr, e))
        
    except Exception as e:
        print("[Proxy] Unexpected error handling client {}: {}".format(addr, e))
    finally:
        # Always close connection
        try:
            conn.close()
        except:
            pass

def run_proxy(ip, port, routes):
    """
    Starts the proxy server and listens for incoming connections. 

    The process dinds the proxy server to the specified IP and port.
    In each incomping connection, it accepts the connections and
    spawns a new thread for each client using `handle_client`.
 

    :params ip (str): IP address to bind the proxy server.
    :params port (int): port number to listen on.
    :params routes (dict): dictionary mapping hostnames and location.

    """

    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        proxy.bind((ip, port))
        proxy.listen(50)
        proxy.settimeout(1)  # Set timeout for CTRL+C handling
        print("[Proxy] Listening on IP {} port {}".format(ip,port))
        
        while True:
            try:
                conn, addr = proxy.accept()
                
                # Create thread for each client connection
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(ip, port, conn, addr, routes),
                    name="proxy-client-{}:{}".format(addr[0], addr[1])
                )
                # Set as daemon thread so main program can exit
                client_thread.daemon = True
                client_thread.start()
                
            except socket.timeout:
                # Timeout allows CTRL+C to interrupt
                continue
            except KeyboardInterrupt:
                print("\n[Proxy] Shutting down gracefully...")
                break
                
    except socket.error as e:
        print("Socket error: {}".format(e))
    finally:
        try:
            proxy.close()
        except:
            pass

def create_proxy(ip, port, routes):
    """
    Entry point for launching the proxy server.

    :params ip (str): IP address to bind the proxy server.
    :params port (int): port number to listen on.
    :params routes (dict): dictionary mapping hostnames and location.
    """

    run_proxy(ip, port, routes)
