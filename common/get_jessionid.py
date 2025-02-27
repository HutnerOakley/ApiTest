
import sys
import os
import webbrowser
from http.server import BaseHTTPRequestHandler
import asyncio
import websockets


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>WebSocket server is running</h1></body></html>')


def open_browser(env, port):
    url = ''
    if env == 'test':
        url = 'https://idsaas.test.leiniao.com'
    elif env == 'prod':
        url = 'https://idsaas-o.api.leiniao.com/'
    else:
        print('环境参数错误')
        sys.exit(0)
    open_url = f'{url}/page/cms-api-docs/apiDoc/?port={port}'
    webbrowser.open(open_url)


async def handle_websocket(websocket):
    jessionid_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', 'JESSIONID.txt')
    async for message in websocket:
        print(f'我的JSESSIONID是: {message}')
        with open(jessionid_path, 'w') as f:
            f.write(message)


async def start_server(port):
    ws_server = await websockets.serve(handle_websocket, 'localhost', port)
    await ws_server.wait_closed()


if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 1 else 'test'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 10215
    open_browser(env, port)
    asyncio.run(start_server(port))
