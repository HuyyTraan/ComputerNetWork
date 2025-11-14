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
daemon.response
~~~~~~~~~~~~~~~~~

This module provides a :class: `Response <Response>` object to manage and persist 
response settings (cookies, auth, proxies), and to construct HTTP responses
based on incoming requests. 

The current version supports MIME type detection, content loading and header formatting
"""
import datetime
import os
import mimetypes
import json
from .dictionary import CaseInsensitiveDict
from .request import Request

BASE_DIR = ""

class Response():   
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.

    Instances are generated from a :class:`Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    :class:`Response <Response>` object encapsulates headers, content, 
    status code, cookies, and metadata related to the request-response cycle.
    It is used to construct and serve HTTP responses in a custom web server.

    :attrs status_code (int): HTTP status code (e.g., 200, 404).
    :attrs headers (dict): dictionary of response headers.
    :attrs url (str): url of the response.
    :attrsencoding (str): encoding used for decoding response content.
    :attrs history (list): list of previous Response objects (for redirects).
    :attrs reason (str): textual reason for the status code (e.g., "OK", "Not Found").
    :attrs cookies (CaseInsensitiveDict): response cookies.
    :attrs elapsed (datetime.timedelta): time taken to complete the request.
    :attrs request (PreparedRequest): the original request object.

    Usage::

      >>> import Response
      >>> resp = Response()
      >>> resp.build_response(req)
      >>> resp
      <Response>
    """

    __attrs__ = [
        "_content",
        "_header",
        "status_code",
        "method",
        "headers",
        "url",
        "history",
        "encoding",
        "reason",
        "cookies",
        "elapsed",
        "request",
        "body",
        "reason",
    ]


    def __init__(self, request=None):
        """
        Initializes a new :class:`Response <Response>` object.

        : params request : The originating request object.
        """

        self._content = False
        self._content_consumed = False
        self._next = None

        #: Integer Code of responded HTTP Status, e.g. 404 or 200.
        self.status_code = None

        #: Case-insensitive Dictionary of Response Headers.
        #: For example, ``headers['content-type']`` will return the
        #: value of a ``'Content-Type'`` response header.
        self.headers = {}

        #: URL location of Response.
        self.url = None

        #: Encoding to decode with when accessing response text.
        self.encoding = None

        #: A list of :class:`Response <Response>` objects from
        #: the history of the Request.
        self.history = []

        #: Textual reason of responded HTTP Status, e.g. "Not Found" or "OK".
        self.reason = None

        #: A of Cookies the response headers.
        self.cookies = CaseInsensitiveDict()

        #: The amount of time elapsed between sending the request
        self.elapsed = datetime.timedelta(0)

        #: The :class:`PreparedRequest <PreparedRequest>` object to which this
        #: is a response.
        self.request = None


    def get_mime_type(self, path):
        """
        Determines the MIME type of a file based on its path.

        "params path (str): Path to the file.

        :rtype str: MIME type string (e.g., 'text/html', 'image/png').
        """

        try:
            mime_type, _ = mimetypes.guess_type(path)
        except Exception:
            return 'application/octet-stream'
        return mime_type or 'application/octet-stream'


    def prepare_content_type(self, mime_type='text/html'):
        """
        Prepares the Content-Type header and determines the base directory
        for serving the file based on its MIME type.

        :params mime_type (str): MIME type of the requested resource.

        :rtype str: Base directory path for locating the resource.

        :raises ValueError: If the MIME type is unsupported.
        """
        
        base_dir = ""

        # Processing mime_type based on main_type and sub_type
        main_type, sub_type = mime_type.split('/', 1)
        print("[Response] processing MIME main_type={} sub_type={}".format(main_type,sub_type))
        if main_type == 'text':
            self.headers['Content-Type']='text/{}'.format(sub_type)
            if sub_type == 'plain' or sub_type == 'css':
                base_dir = BASE_DIR+"static/"
            elif sub_type == 'html':
                base_dir = BASE_DIR+"www/"
            else:
                handle_text_other(sub_type)
        elif main_type == 'image':
            base_dir = BASE_DIR+"static/"
            self.headers['Content-Type']='image/{}'.format(sub_type)
        elif main_type == 'application':
            base_dir = BASE_DIR+"apps/"
            self.headers['Content-Type']='application/{}'.format(sub_type)
        #
        #  TODO: process other mime_type
        #        application/xml       
        #        application/zip
        #        ...
        #        text/csv
        #        text/xml
        #        ...
        #        video/mp4 
        #        video/mpeg
        #        ...
        #
        else:
            raise ValueError("Invalid MEME type: main_type={} sub_type={}".format(main_type,sub_type))

        return base_dir


    def build_content(self, path, base_dir):
        """
        Loads the objects file from storage space.

        :params path (str): relative path to the file.
        :params base_dir (str): base directory where the file is located.

        :rtype tuple: (int, bytes) representing content length and content data.
        """

        filepath = os.path.join(base_dir, path.lstrip('/'))

        print("[Response] serving the object at location {}".format(filepath))
            #
            #  TODO: implement the step of fetch the object file
            #        store in the return value of content
            #
        return len(content), content
    
    def build_file_response(self, request: "Request"):
        """
        Serve static HTML file from ./www directory.

        Quy ước:
        - "/"               -> "/index.html"
        - "/login"          -> "/login.html"
        - "/chat"           -> "/chat.html"
        - "/abc.html"       -> "/abc.html"
        """
        path = getattr(request, "path", "/") or "/"

        # Bỏ query string nếu có: /login?x=1 -> /login
        if "?" in path:
            path = path.split("?", 1)[0]

        # Mặc định root
        if path == "/" or path == "":
            path = "/index.html"

        # Nếu đoạn cuối không có dấu chấm -> tự thêm ".html"
        # VD: /login -> /login.html
        import os
        if "." not in os.path.basename(path):
            path = path + ".html"

        base_dir = "www"
        filepath = os.path.join(base_dir, path.lstrip("/"))

        if not os.path.exists(filepath):
            print(f"[Response] File not found: {filepath}")
            return self.build_error_response(404, f"File not found: {path}")

        with open(filepath, "rb") as f:
            content = f.read()

        mime_type = self.get_mime_type(filepath)  # sẽ là text/html cho .html

        status_line = "HTTP/1.1 200 OK\r\n"
        headers = ""
        headers += f"Content-Type: {mime_type}\r\n"
        headers += f"Content-Length: {len(content)}\r\n"
        headers += "\r\n"

        print(f"[Response] Serving static file: {filepath} ({len(content)} bytes)")
        return status_line.encode("utf-8") + headers.encode("utf-8") + content




    def build_response_header(self, request):
        """
        Constructs the HTTP response headers based on the class:`Request <Request>
        and internal attributes.

        :params request (class:`Request <Request>`): incoming request object.

        :rtypes bytes: encoded HTTP response header.
        """
        reqhdr = request.headers
        rsphdr = self.headers

        #Build dynamic headers
        headers = {
                "Accept": "{}".format(reqhdr.get("Accept", "application/json")),
                "Accept-Language": "{}".format(reqhdr.get("Accept-Language", "en-US,en;q=0.9")),
                "Authorization": "{}".format(reqhdr.get("Authorization", "Basic <credentials>")),
                "Cache-Control": "no-cache",
                "Content-Type": "{}".format(self.headers['Content-Type']),
                "Content-Length": "{}".format(len(self._content)),
#                "Cookie": "{}".format(reqhdr.get("Cookie", "sessionid=xyz789")), #dummy cooki
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
                "Date": "{}".format(datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
                "Max-Forward": "10",
                "Pragma": "no-cache",
                "Proxy-Authorization": "Basic dXNlcjpwYXNz",  # example base64
                "Warning": "199 Miscellaneous warning",
                "User-Agent": "{}".format(reqhdr.get("User-Agent", "Chrome/123.0.0.0")),
            }

        # Header text alignment
            #
            #  TODO: implement the header building to create formated
            #        header from the provied headers
            #
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        return str(fmt_header).encode('utf-8')


    def build_notfound(self):
        """
        Constructs a standard 404 Not Found HTTP response.

        :rtype bytes: Encoded 404 response.
        """
        return self.build_error_response(404, "Not Found")


    # def build_response(self, request: Request):
    #     """
    #     Builds a full HTTP response based on the request.
        
    #     Two cases:
    #     1. If request has a hook (route handler) → build JSON response
    #     2. Otherwise → try to serve static file or 404
        
    #     :params request: incoming request object
    #     :rtype bytes: complete HTTP response
    #     """
        
    #     # Case 1: Request has a hook (route handler) → call it
    #     if request.hook:
    #         return self.build_json_response(request)
        
    #     # # Case 2: No hook → try to serve static file
    #     # elif request.path.endswith(('.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif')):
    #     #     return self.build_file_response(request)
        
    #     # Case 3: No hook, not a file → 404
    #     else:
    #         return self.build_error_response(404, "Route not found")
    def build_response(self, request: "Request"):
        """
        Builds a full HTTP response based on the request.

        - Nếu request có hook (route của WeApRous) → JSON (RESTful)
        - Nếu không có hook → thử serve static HTML
        """
        # Safety: request rỗng
        if request is None:
            return self.build_error_response(500, "Empty request object")

        # Case 1: có route handler → JSON
        if getattr(request, "hook", None):
            return self.build_json_response(request)

        # Case 2: không có route → serve static HTML từ ./www
        return self.build_file_response(request)


    # def build_json_response(self, request: Request):
    #     """
    #     Build JSON response from hook handler.
        
    #     Supports:
    #     - (status_code, data) tuple return from handlers
    #     - (status_code, data, cookies) tuple for Set-Cookie support
    #     - Single value return (defaults to 200)
    #     """
    #     try:
    #         print("[Response] Calling hook handler for {} {}".format(
    #             request.method, request.path))
            
    #         # Gọi hook handler - pass request object so handler can access cookies, headers, etc.
    #         result = request.hook(request=request)
            
    #         # Extract status code, data, and optional cookies
    #         status_code = 200
    #         data = result
    #         response_cookies = None
            
    #         if isinstance(result, tuple):
    #             if len(result) == 3:
    #                 # (status_code, data, cookies)
    #                 status_code, data, response_cookies = result
    #                 print("[Response] cookies: {}, status code : {}, data: {}".format(response_cookies, status_code, data))
    #             elif len(result) == 2:
    #                 # (status_code, data)
    #                 status_code, data = result
    #                 print("[Response] status code : {}, data: {}".format(status_code, data))
    #             else:
    #                 data = result
    #                 print("[Response] data: {}".format(data))
            
    #         # Convert to JSON
    #         response_body = json.dumps(data).encode('utf-8')
            
    #         # Map status code to text
    #         status_map = {
    #             200: "OK",
    #             201: "Created",
    #             204: "No Content",
    #             400: "Bad Request",
    #             401: "Unauthorized",
    #             404: "Not Found",
    #             500: "Internal Server Error"
    #         }
    #         status_text = status_map.get(status_code, "OK")
            
    #         # Build HTTP response
    #         status_line = "HTTP/1.1 {} {}\r\n".format(status_code, status_text)
    #         headers = "Content-Type: application/json\r\n"
            
    #         # Add Set-Cookie header if provided
    #         if response_cookies:
    #             if isinstance(response_cookies, dict):
    #                 # response_cookies = {"auth": "true", "sessionid": "xyz"}
    #                 for cookie_name, cookie_value in response_cookies.items():
    #                     headers += "Set-Cookie: {}={}\r\n".format(cookie_name, cookie_value)
    #             elif isinstance(response_cookies, str):
    #                 # response_cookies = "auth=true; Path=/; HttpOnly"
    #                 headers += "Set-Cookie: {}\r\n".format(response_cookies)
            
    #         headers += "Content-Length: {}\r\n\r\n".format(len(response_body))
            
    #         print("[Response] JSON response: status={}, content-length={}".format(
    #             status_code, len(response_body)))
            
    #         return status_line.encode('utf-8') + headers.encode('utf-8') + response_body
        
    #     except Exception as e:
    #         print("[Response] Error in hook handler: {}".format(e))
    #         return self.build_error_response(500, str(e))
    def build_json_response(self, request: "Request"):
        """
        Build JSON response from hook handler.

        Hỗ trợ:
        - handler trả (status_code, data)
        - handler trả (status_code, data, cookies_dict)
        - handler trả 1 object duy nhất (mặc định status 200)
        """
        try:
            print("[Response] Calling hook handler for {} {}".format(
                request.method, request.path))

            # Gọi route handler, luôn truyền request để handler dùng cookies, body, ...
            result = request.hook(request=request)

            status_code = 200
            data = result
            response_cookies = None

            if isinstance(result, tuple):
                if len(result) == 3:
                    status_code, data, response_cookies = result
                    print("[Response] cookies: {}, status code : {}, data: {}".format(
                        response_cookies, status_code, data))
                elif len(result) == 2:
                    status_code, data = result
                    print("[Response] status code : {}, data: {}".format(
                        status_code, data))
                else:
                    # Tuple nhưng không đúng 2 hoặc 3 phần tử → coi như data
                    data = result
                    print("[Response] data (tuple with len !=2,3): {}".format(data))
            else:
                print("[Response] data: {}".format(data))

            # Convert body sang JSON bytes
            response_body = json.dumps(data).encode("utf-8")

            # Map status→status text
            status_map = {
                200: "OK",
                201: "Created",
                204: "No Content",
                400: "Bad Request",
                401: "Unauthorized",
                404: "Not Found",
                500: "Internal Server Error",
            }
            status_text = status_map.get(status_code, "OK")

            status_line = "HTTP/1.1 {} {}\r\n".format(status_code, status_text)
            headers = "Content-Type: application/json\r\n"

            # Thêm Set-Cookie nếu có
            if response_cookies:
                if isinstance(response_cookies, dict):
                    for cookie_name, cookie_value in response_cookies.items():
                        headers += "Set-Cookie: {}={}\r\n".format(cookie_name, cookie_value)
                elif isinstance(response_cookies, str):
                    headers += "Set-Cookie: {}\r\n".format(response_cookies)

            headers += "Content-Length: {}\r\n\r\n".format(len(response_body))

            print("[Response] JSON response: status-{}, content-length={}".format(
                status_code, len(response_body)))

            return status_line.encode("utf-8") + headers.encode("utf-8") + response_body

        except Exception as e:
            print("[Response] Error in hook handler: {}".format(e))
            return self.build_error_response(500, str(e))

    # def build_file_response(self, request):
    #     """
    #     Serve static file (HTML, CSS, JS, images, etc.)
    #     """
    #     try:
    #         path = request.path
    #         # Determine base directory based on file extension
    #         if path.endswith('.html'):
    #             base_dir = "www"
    #         elif path.endswith('.css'):
    #             base_dir = "static/css"
    #         elif path.endswith('.js'):
    #             base_dir = "static/js"
    #         elif path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
    #             base_dir = "static/images"
    #         else:
    #             return self.build_error_response(404, "File type not supported")
            
    #         # Build full file path
    #         filepath = os.path.join(base_dir, path.lstrip('/'))
            
    #         print("[Response] Serving file: {}".format(filepath))
            
    #         # Read file
    #         if not os.path.exists(filepath):
    #             print("[Response] File not found: {}".format(filepath))
    #             return self.build_error_response(404, "File not found: {}".format(filepath))
            
    #         with open(filepath, 'rb') as f:
    #             file_content = f.read()
            
    #         # Determine content type
    #         mime_type = self.get_mime_type(path)
            
    #         # Build HTTP response
    #         status_line = "HTTP/1.1 200 OK\r\n"
    #         headers = "Content-Type: {}\r\n".format(mime_type)
    #         headers += "Content-Length: {}\r\n\r\n".format(len(file_content))
            
    #         response = status_line + headers
            
    #         return response.encode('utf-8') + file_content
        
    #     except Exception as e:
    #         print("[Response] Error serving file: {}".format(e))
    #         return self.build_error_response(500, str(e))

    def build_error_response(self, status_code, message):
        """
        Build error response for various status codes.
        
        Supports: 400, 401, 404, 500
        """
        status_map = {
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error"
        }
        
        status_text = status_map.get(status_code, "Error")
        
        # Build JSON error body
        error_body = {"error": message, "status": status_code}
        response_body = json.dumps(error_body).encode('utf-8')
        
        # Build HTTP response
        status_line = "HTTP/1.1 {} {}\r\n".format(status_code, status_text)
        headers = "Content-Type: application/json\r\n"
        headers += "Content-Length: {}\r\n\r\n".format(len(response_body))
        
        print("[Response] Error response: status={}, message={}".format(
            status_code, message))
        
        response = status_line + headers
        
        return response.encode('utf-8') + response_body