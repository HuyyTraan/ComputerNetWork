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
daemon.request
~~~~~~~~~~~~~~~~~

This module provides a Request object to manage and persist 
request settings (cookies, auth, proxies).
"""
from .dictionary import CaseInsensitiveDict

class Request():
    """The fully mutable "class" `Request <Request>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a "class" `Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import deamon.request
      >>> req = request.Request()
      ## Incoming message obtain aka. incoming_msg
      >>> r = req.prepare(incoming_msg)
      >>> r
      <Request>
    """
    __attrs__ = [
        "method",
        "url",
        "headers",
        "body",
        "reason",
        "cookies",
        "body",
        "routes",
        "hook",
    ]

    def __init__(self):
        #: HTTP verb to send to the server.
        self.method = None
        #: HTTP URL to send the request to.
        self.url = None
        #: dictionary of HTTP headers.
        self.headers = None
        #: HTTP path
        self.path = None        
        # The cookies set used to create Cookie header
        self.cookies = None
        #: request body to send to the server.
        self.body = None
        #: Routes
        self.routes = {}
        #: Hook point for routed mapped-path
        self.hook = None
        #: Auth
        self.auth = None

    def extract_request_line(self, request):
        try:
            lines = request.splitlines()
            first_line = lines[0]
            method, path, version = first_line.split()

            # if path == '/':
            #     path = '/index.html'
        except Exception:
            return None, None

        return method, path, version
             
    def prepare_headers(self, request) -> dict:
        """Prepares the given HTTP headers."""
        lines = request.split('\r\n')
        headers = {}
        for line in lines[1:]:
            if ': ' in line:
                key, val = line.split(': ', 1)
                headers[key.lower()] = val
        return headers

    def prepare(self, request, routes:dict=None):
        """Prepares the entire request with the given parameters."""

        # Prepare the request line from the request header
        print("[Request] preparing request...\n{}".format(request))

        # extract request line
        self.method, self.path, self.version = self.extract_request_line(request)
        print("[Request] {} path {} version {}".format(self.method, self.path, self.version))
        #
        # @bksysnet Preapring the webapp hook with WeApRous instance
        # The default behaviour with HTTP server is empty routed
        #
        # TODO manage the webapp hook in this mounting point
        #
        
        
        # prepare headers
        self.headers = self.prepare_headers(request)
        print("[Request] prepared headers: {}".format(self.headers))

        # prepare cookies
        cookies_str = self.headers.get('cookie', '')
        self.cookies = self.prepare_cookies(cookies_str=cookies_str)
        
        # prepare body
        if self.method not in ['GET']:
            self.prepare_body(request)

        # prepare auth
        auth_str = self.headers.get('authorization', '')
        self.auth = self.prepare_auth(auth_str)
        
        # find hook from routes dict
        if routes:
            self.routes = routes
            route_key = (self.method, self.path)
            self.hook = routes.get(route_key)
            
            if self.hook:
                print("[Request] Found hook for {} {}".format(self.method, self.path))
            else:
                print("[Request] No route handler for {} {}".format(self.method, self.path))
        else:
            self.hook = None
            print("[Request] No routes available")
        return

    def prepare_body(self, request : str):
        content_length = self.prepare_content_length()
        
        try:
            parts = request.split('\r\n\r\n', 1)
            if len(parts) > 1:
                body_full = parts[1]
                self.body = body_full[:content_length]
                print("[Request] prepared body: {}".format(self.body))
            else:
                self.body = None
        except Exception as e:
            print("[Request] Error preparing body: {}".format(e))
            self.body = None
        return


    def prepare_content_length(self):
        return int(self.headers.get("content-length", "0"))

    def prepare_auth(self, auth_str:str) -> dict:
        """Prepare authentication from the Authorization header."""
        if not auth_str:
            return None
        try:
            parts = auth_str.split(' ', 1)

            if len(parts) == 2:
                auth_type, auth_value = parts
                auth = {
                    'type': auth_type.lower(),    # 'bearer', 'basic', etc.
                    'value': auth_value           # token hoặc credentials
                }
                print("[Request] auth: type={}, value={}".format(
                    auth['type'], 
                    auth['value'][:20] + '...' if len(auth['value']) > 20 else auth['value']
                ))
                return auth
            else:
                return None
        except Exception as e:
            print("[Request] Error parsing auth: {}".format(e))
            return None

    def prepare_cookies(self, cookies_str: str) -> dict:
        """Parse cookies string and prepare cookies dictionary."""
        cookies = {}
        if cookies_str:
            for pair in cookies_str.split(";"):
                pair = pair.strip()
                if not pair:  # Skip empty cookies
                    continue
                
                if "=" not in pair:  # Skip invalid format
                    print("[Request] Warning: Invalid cookie format: {}".format(pair))
                    continue
                
                # Split ONLY on first "=" (maxsplit=1)
                key, value = pair.split("=", 1)  # ← maxsplit=1!
                cookies[key.strip()] = value.strip()
        
        return cookies