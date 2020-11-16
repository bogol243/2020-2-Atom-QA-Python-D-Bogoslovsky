import json
import threading
import time
from HW_6 import settings
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, HTTPServer


# Это mock сервер, его будем использовать в качестве
# провайдера стороннего API.
 

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def _parse_path(self):
        path_list = self.path.split("?")
        location = path_list[0]
        res = {}
        if len(path_list)>1:
            args = self.path.split("?")[-1].split("&")
            for arg in args:
                res[arg.split("=")[0]]= arg.split("=")[1]
        return location, res
    
    def _parse_body_json(self):
        print(self.headers)
        content_len = int(self.headers.get("Content-Length"))
        print(f"content len: {content_len}")
        
        post_body = self.rfile.read(content_len)
        return json.loads(post_body)


    def _set_headers(self,code):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    
    def _write_json(self,obj):
        self.wfile.write(json.dumps(obj).encode())
    
    def do_PUT(self):

        location, args = self._parse_path()

        if location=="/data":
            # Обновление конкретных данных (PUT)
            # принимает токен (в заголовке Authorization), 
            # id обновляемого ресурса (в аргументах) 
            # и новые данные в формате json (в теле)
            
            # сначала проверяем авторизацию
            if "Authorization" in self.headers:
                # Заголовок есть, теперь проверяем что он чему-то соответствует
                if (auth:=self.headers["Authorization"]) in self.server.data:
                    # пользователь с таким токеном имеется
                    # можно обновлять данные
                    data_id = str(args["data_id"])
                    user_data = self.server.data[auth]
                    
                    # Определяем какой вернуть статус код
                    if data_id in user_data["data"]:
                        # Если уже есть ресурс - обновляем
                        self._set_headers(200)
                        # соответствие полей не проверяю...
                        user_data["data"][data_id] = self._parse_body_json()
                        print("new data:"+str(user_data["data"][data_id]))
                        self._write_json({"data_count":len(user_data["data"])})
                        return
                    else:
                        # Если нет -- ресурс не найден
                        self._set_headers(404)
                        self._write_json({"error":"There's no data with this id"})
                        return
                else:
                    # пользователя с таким токеном нет:(
                    # поэтому взаимодействие запрещено
                    self._set_headers(403)
                    self._write_json({"error": "Wrong token or token expired"})
                    return
            else:
                #Если нет заголовка отвечаем что Bad Request
                self._set_headers(400)
                self._write_json({"error":"No token provided in Authorization header"})
                return
        else:
            # ответ на любой другой локейшн
            self._set_headers(200)
            self._write_json({"pass":"pass"})
    
    def do_POST(self):

        location, args = self._parse_path()

        if location=="/data":
            # добавление данных (POST)
            # принимает токен (в заголовке Authorization)
            # и новые данные в формате json (в теле)
            
            # сначала проверяем авторизацию
            if "Authorization" in self.headers:
                # Заголовок есть, теперь проверяем что он чему-то соответствует
                if (auth:=self.headers["Authorization"]) in self.server.data:
                    # пользователь с таким токеном имеется
                    # можно добавлять данные
                    user_data = self.server.data[auth]
                    data_id = str(user_data["last_id"] + 1) #генерируем новый id для данных
                    
                    # соответствие полей не проверяю...
                    user_data["data"][data_id] = self._parse_body_json()
                    print("new data:"+str(user_data["data"][data_id]))
                    
                    self._set_headers(201) # Created
                    self._write_json({"data_count":len(user_data["data"])})
                    return
                else:
                    # пользователя с таким токеном нет:(
                    # поэтому взаимодействие запрещено
                    self._set_headers(403)
                    self._write_json({"error": "Wrong token or token expired"})
                    return
            else:
                #Если нет заголовка отвечаем что Bad Request
                self._set_headers(400)
                self._write_json({"error":"No token provided in Authorization header"})
                return
        elif location == "/setupMock/data":
            #локейшн для загрузки данных в мок
            print("Setting up mock...")
            setup_data = self._parse_body_json()
            self.server.data = setup_data["data"]
            self.server.tokens = setup_data["tokens"]
            self._set_headers(200)

        elif location == "/setupMock/timeout":
            #локейшн для загрузки данных в мок
            print("Setting up mock...")
            setup_data = self._parse_body_json()
            print(setup_data)
            print(f"old timeout: {self.server.timeout}")
            self.server.timeout = int(setup_data["timeout"])
            print(f"new timeout: {self.server.timeout}")
            self._set_headers(200)

        else:
            # ответ на любой другой локейшн
            self._set_headers(200)
            self._write_json({"pass":"pass"})


    def do_GET(self):
        location, args = self._parse_path()
        print(f"location: {location}")
        # 1) Авторизация в API с получением токена для следующих запросов (через GET)
        #       принимает в аргументах uid и код авторизации, возвращает токен
        if location=="/auth":
            # пришёл запрос на авторизацию
            id_pair = f"{args['uid']},{args['code']}"
            print(f"id pair:{id_pair}")
            
            if id_pair == settings.CAUSE_500:
                #для теста ошибки сервера
                self._set_headers(code=500)
                print("returning error 500")
                self._write_json({"error":"internal server error"})
                return

            # проверяем данные
            if id_pair in self.server.tokens:
                # пара uid-code верна, отдаём токен
                # получаем данные пользователя
                token = self.server.tokens[id_pair]
                self._set_headers(code=200)
                self._write_json({"token":token})
            else:
                # нет запрошеной пары, отдаём ошибку
                self._set_headers(code=401)
                self._write_json({"error": "uid is not found or code expired"})
        elif location=="/data":
            #получаем данные для этого пользователя
            #data_id = str(args["data_id"])
            #print(f"data_id: {data_id}")
            if "Authorization" in self.headers:
                if (auth:=self.headers["Authorization"]) in self.server.data:
                    user_data = self.server.data[auth]["data"]
                    print(user_data)
                    self._set_headers(200)
                    self._write_json({"data":user_data})
                    return
                    #if data_id in user_data:
                    #    requested_data = user_data[data_id]
                    #    self._set_headers(200) #Found
                    #    self._write_json(requested_data)
                    #    return
                    #else:
                    #    self._set_headers(404) #Not Found
                    #    self._write_json({"error":"There's no data with this id"})
                    #    return
                else:
                    # пользователя с таким токеном нет:(
                    # поэтому взаимодействие запрещено
                    self._set_headers(403)
                    self._write_json({"error": "Wrong token or token expired"})
                    return
            else:
                #Если нет заголовка отвечаем что Bad Request
                self._set_headers(400)
                self._write_json({"error":"No token provided in Authorization header"})
                return
        elif location=="/shutdown":
            print("shuting down the server")
            assassin = threading.Thread(target=self.server.shutdown)
            assassin.daemon = True
            assassin.start()

        else:
            #все остальные запросы
            print(f"loaction: {location}")
            self._set_headers(code=200)
            self._write_json({"pass":"pass"})
    
    def do_HEAD(self):
        location, args = self._parse_path()

        # чтобы проверять что к серверу вообще можно подключиться
        print(f"loaction: {location}")
        print(f"timeout: {self.server.timeout}")
        time.sleep(self.server.timeout)
        self._set_headers(code=200)
        
        
        

        

class MockHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stop_server = False
        self.handler = HTTPRequestHandler
        self.server = ThreadingHTTPServer((self.host, self.port), self.handler)
        self.server.timeout = 0

        #init with default data
        self.server.data = settings.MOCK_DATA["data"]
        self.server.tokens = settings.MOCK_DATA["tokens"]

    def start(self):
        self.server.allow_reuse_address = True
        self.th = threading.Thread(target=self.server.serve_forever)#, daemon=True)
        print("server starting")
        self.th.start()
        return self.server

    def stop(self):
        self.server.server_close()
        self.server.shutdown()
        self.stop_server = True

    def set_data(self, data):
        self.handler.data = json.dumps(data).encode()


if __name__ == "__main__" :
    server = MockHTTPServer(settings.MOCK_HOST,settings.MOCK_PORT)
    server = server.start()

