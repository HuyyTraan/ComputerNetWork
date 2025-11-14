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
daemon.backend
~~~~~~~~~~~~~~~~~

This module provides a backend object to manage and persist backend daemon. 
It implements a basic backend server using Python's socket and threading libraries.
It supports handling multiple client connections concurrently and routing requests using a
custom HTTP adapter.

Requirements:
--------------
- socket: provide socket networking interface.
- threading: Enables concurrent client handling via threads.
- response: response utilities.
- httpadapter: the class for handling HTTP requests.
- CaseInsensitiveDict: provides dictionary for managing headers or routes.


Notes:
------
- The server create daemon threads for client handling.
- The current implementation error handling is minimal, socket errors are printed to the console.
- The actual request processing is delegated to the HttpAdapter class.

Usage Example:
--------------
>>> create_backend("127.0.0.1", 9000, routes={})

"""

import socket
import threading
import argparse

from .response import *
from .httpadapter import HttpAdapter
from .dictionary import CaseInsensitiveDict

def handle_client(ip, port, conn, addr, routes):
    """
    Initializes an HttpAdapter instance and delegates the client handling logic to it.

    :param ip (str): IP address of the server.
    :param port (int): Port number the server is listening on.
    :param conn (socket.socket): Client connection socket.
    :param addr (tuple): client address (IP, port).
    :param routes (dict): Dictionary of route handlers.
    """
    daemon = HttpAdapter(ip, port, conn, addr, routes)

    # Handle client
    daemon.handle_client(conn, addr, routes)

def run_backend(ip, port, routes):
    """
    Starts the backend server, binds to the specified IP and port, and listens for incoming
    connections. Each connection is handled in a separate thread. The backend accepts incoming
    connections and spawns a thread for each client.


    :param ip (str): IP address to bind the server.
    :param port (int): Port number to listen on.
    :param routes (dict): Dictionary of route handlers.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((ip, port))
        server.listen(50)
        server.settimeout(1)  # Set timeout 1 giây để CTRL+C hoạt động
        print("[Backend] Listening on port {}".format(port))
        if routes != {}:
            print("[Backend] route settings {}".format(routes))

        while True:
            try:
                conn, addr = server.accept()
                #
                #  TODO: implement the step of the client incomping connection
                #        using multi-thread programming with the
                #        provided handle_client routine
                #
                # Chấp nhận kết nối client (blocking)

                # Tạo một thread mới để xử lý kết nối này bằng hàm handle_client
                t = threading.Thread(
                    target=handle_client,
                    args=(ip, port, conn, addr, routes),
                    name="backend-client-{}:{}".format(addr[0], addr[1]) # for debugging purposes
                )
                # Đặt thread là daemon để khi process chính kết thúc thì các thread con cũng không ngăn chương trình thoát
                t.daemon = True

                # Khởi động thread (thread sẽ gọi handle_client(conn, addr, routes))
                t.start()
            except socket.timeout:
                # Timeout để CTRL+C có thể gián đoạn
                continue
            except KeyboardInterrupt:
                print("\n[Backend] Shutting down the server.")
                try:
                    server.close()
                except Exception as e:
                    print("Error closing server: {}".format(e))
                    pass
                break

            except socket.error as e:
                print("[Backend] Socket error on accept: {}".format(e))
                continue
    except socket.error as e:
      print("Socket error: {}".format(e))

def create_backend(ip, port, routes={}):
    """
    Entry point for creating and running the backend server.

    :param ip (str): IP address to bind the server.
    :param port (int): Port number to listen on.
    :param routes (dict, optional): Dictionary of route handlers. Defaults to empty dict.
    """

    run_backend(ip, port, routes)