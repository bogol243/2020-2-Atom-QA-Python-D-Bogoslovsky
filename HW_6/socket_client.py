import socket
import json
from HW_6 import settings


class SocketClient:

    def __init__(self, host: str, port: int, timeout: int = 1, headers=None):
        self.host = host
        self.port = port

        self.base_headers = {"Host": f'{host}:{str(port)}'}
        if headers is not None:
            self.base_headers.update(headers)

        self._init_socket()
        self.socket.settimeout(timeout)
    
    def _init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def _parse_headers(self,headers_bytes:str):
        lines = headers_bytes.splitlines()
        res = {}
        for line in lines:
            name, val = line.split(": ")
            res[name] = val
        return res

    def request(self, method: str = "GET", target: str = "/", headers: dict = {}, body: str = ""):
        self._init_socket()
        self.socket.connect((self.host, self.port))
        nl = "\r\n"
        content_length = len(body.encode('utf-8'))
        self.base_headers["Content-Length"] = content_length
        if content_length>0:
            self.base_headers["Content-Type"] = "application/json"
        self.base_headers.update(headers)
        headers_str = nl.join(
            [f'{name}: {str(val)}' for (name, val) in self.base_headers.items()])

        request = f"{method.upper()} {target} HTTP/1.1{nl}"\
                  f"{headers_str}{nl*2}"\
                  f"{body}"
        print(f"request:\n {request}")
        self.socket.send(request.encode('utf-8'))
        response_bytes = self._recv()
        print(response_bytes)

        response = {}
        response["status_code"] = int(response_bytes.splitlines()[0].split(" ")[1])
        
        response_bytes = '\n'.join(response_bytes.splitlines()[1:])
        response["body"] = response_bytes.split("\n")[-1]
        headers_bytes = response_bytes.split("\n")[0]
        response["headers"] = self._parse_headers(headers_bytes)
        
        print(response)
        self.socket.recv(4096)
        self.socket.close()
        return response

    def _recv(self, buff_size: int = 4096) -> str:
        total_data = []
        while True:
            data = self.socket.recv(buff_size)
            if data:
                total_data.append(data.decode())
            else:
                break

        data = ''.join(total_data)
        return data

    def set_headers(self, headers):
        self.base_headers.update(headers)

if __name__ == "__main__":
    client_mock = SocketClient(settings.MOCK_HOST,settings.MOCK_PORT)
    client_mock.request(method="POST",
                        target="/setupMock/timeout",
                        body=json.dumps({"timeout":11}))


