#!/usr/bin/env python3
#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#
# WeApRous release - Task 1A Entry Point
#

"""
start_app
~~~~~~~~~

Entry point to start the WeApRous backend server for Task 1A: Authentication Handling.

Usage:
    python start_app.py                          (default: 0.0.0.0:9000)
    python start_app.py --server-ip localhost    (localhost:9000)
    python start_app.py --server-port 8080       (0.0.0.0:8080)
    python start_app.py --server-ip 127.0.0.1 --server-port 5000

This script:
    1. Imports the Task 1A application (apps.app)
    2. Configures the server address and port
    3. Starts the backend server with threading support
    4. Handles CTRL+C gracefully for shutdown
"""

if __name__ == "__main__":
    from apps.app import app, PORT
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        prog='start_app',
        description='Start WeApRous backend for Task 1A: Authentication Handling',
        epilog='Example: python start_app.py --server-port 8080'
    )
    parser.add_argument(
        '--server-ip',
        default='0.0.0.0',
        help='Server IP address (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--server-port',
        type=int,
        default=PORT,
        help=f'Server port (default: {PORT})'
    )
    
    args = parser.parse_args()
    ip = args.server_ip
    port = args.server_port
    
    print(f"\n{'='*70}")
    print(f"Starting WeApRous Backend - Task 1A: Authentication Handling")
    print(f"{'='*70}")
    print(f"Server listening on: {ip}:{port}")
    
    # Get display IP (use actual bind IP if not 0.0.0.0, otherwise show both local and network options)
    display_ip = ip if ip != "0.0.0.0" else "127.0.0.1"
    
    # Print clickable startup info
    print("\n==============================================================")
    print("WeApRous Chat Application is running!")
    print("==============================================================")
    print(f"Backend listening on: http://{args.server_ip}:{args.server_port}")
    print("")
    
    if ip == "0.0.0.0":
        # Show both local and network access when binding to all interfaces
        print("Access URLs:")
        print(f"  🏠 Local:   http://127.0.0.1:{args.server_port}/chat.html")
        print(f"  🌍 Network: http://YOUR_NETWORK_IP:{args.server_port}/chat.html")
        print("     (Replace YOUR_NETWORK_IP with your actual IP from 'ipconfig')")
        print("")
        print("Task 1A APIs:")
        print(f"  • GET  http://127.0.0.1:{args.server_port}/")
        print(f"  • POST http://127.0.0.1:{args.server_port}/login")
        print(f"  • GET  http://YOUR_NETWORK_IP:{args.server_port}/")
        print(f"  • POST http://YOUR_NETWORK_IP:{args.server_port}/login")
    else:
        # Show specific IP access
        print("Access URLs:")
        print(f"  👉 http://{display_ip}:{args.server_port}/chat.html")
        print("")
        print("Task 1A APIs:")
        print(f"  • GET  http://{display_ip}:{args.server_port}/")
        print(f"  • POST http://{display_ip}:{args.server_port}/login")
    print("")
    print("🔥 Proxy Access (if proxy server is running):")
    if args.server_port == 8000:
        print(f"  • Via Proxy: http://127.0.0.1:8080/ (Task 1A)")
        print(f"  • Via Proxy: http://127.0.0.1:8081/ (Task 2 Chat)")
        print(f"  • Network:   http://YOUR_NETWORK_IP:8080/")
    else:
        print(f"  • Note: Update proxy.conf to forward to port {args.server_port}")
    print("--------------------------------------------------------------")
    print("Press CTRL + C to stop the server")
    print("==============================================================\n")

    
    print(f"\n🔑 Default Login Credentials:")
    print(f"  • Username: admin")
    print(f"  • Password: password")
    print(f"\n📝 Usage Tips:")
    print(f"  • Test with Thunder Client or browser")
    print(f"  • For network access: Configure proxy.conf with your IP")
    print(f"  • Open multiple tabs to simulate multiple users")
    print(f"\nPress CTRL+C to stop the server")
    print(f"{'='*70}\n")
    
    try:
        # Prepare and run the application
        app.prepare_address(ip, port)
        app.run()
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("Server shutting down gracefully...")
        print("="*70)
