import os
import socket
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import cast

import dotenv


class _ReusingHTTPServer(HTTPServer):
    allow_reuse_address = True
    auth_code: str


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            cast(_ReusingHTTPServer, self.server).auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful. You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing authorization code.")


def token_expired(auth_url: str, port: int) -> bool:
    dotenv.load_dotenv(dotenv_path="src/.env", override=True)
    expiry_str: str = str(os.environ.get("EXPIRY")).strip("'")
    if (expiry_str == "" or int(expiry_str)) <= float(time.time()):
        _open_auth_url(auth_url, port)
        return True
    else:
        return False


def _open_auth_url(auth_url: str, port: int) -> None:
    httpd = _ReusingHTTPServer(("localhost", port), CallbackHandler)
    webbrowser.open(auth_url)
    try:
        httpd.handle_request()
        os.environ["AUTH"] = httpd.auth_code
        dotenv.set_key("src/.env", "AUTH", httpd.auth_code)
    except OSError:
        os.environ["AUTH"] = ""
        print("ERROR: Port in use. Please restart your terminal.")
        exit(1)
    finally:
        httpd.socket.shutdown(socket.SHUT_RDWR)
        httpd.server_close()
