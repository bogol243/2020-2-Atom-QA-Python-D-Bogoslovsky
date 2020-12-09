import json
import threading
import requests
from urllib.parse import urljoin, unquote
from flask import Flask, request, jsonify
from HW_6 import settings
from HW_6.socket_client import SocketClient
from requests.exceptions import Timeout


app = Flask(__name__)
DATA = {}
server: threading.Thread

def run_app(host=settings.APP_HOST, port=settings.APP_PORT):
    server = threading.Thread(target=app.run, kwargs={
        'host': host,
        'port': port
    })

    server.start()
    return server

def shutdown_app():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        print("TERMINATION")
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_app()

# проверка внешнего сервиса
@app.route('/checkExternalService')
def check_external_service():
    try:
        resp = requests.head(f"http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/",timeout=2)
        return jsonify("External service is up"), resp.status_code
    except requests.exceptions.ConnectionError:
        return "Can't reach external service", 504
    except Timeout:
        return "External service not responding (timeout)", 504

# авторизация в стороннем API 
@app.route('/authApi',methods=['GET'])
def authorize_api():
    # получаем от клиента данные
    uid = request.args.get('uid')
    code = request.args.get('code')
    print("starting authorizing api")
    # пытаемся авторизоваться в стороннем сервисе
    # с использованием полученных данных.
    try:
        response = requests.get(f"http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/auth?uid={uid}&code={code}",timeout=5)
    except Timeout:
        return jsonify(f"External API server timeout"), 504

    if(response.status_code==200):
        #aвторизация успешна
        return jsonify(f"OK"), 200

    elif(response.status_code==401):
        #авторизация не успешна
        return "Authorization in external API failed", 401

    elif(response.status_code//100==5):
        return "External service error", 504
    
    print(f"status code: {response.status_code}")
    return "Internal server error", 500


@app.route('/data',methods=['POST'])
def post_data():
    data = request.json()
    data_id = request.args.get("data_id")
    print(data)
    auth = request.headers.get('Authorization')
    headers = {'Authorization': auth}
    response = requests.post(
        f"http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/data?data_id={data_id}",
        json=data,
        headers=headers,
        timeout=5)
    
    res = json.loads(response.text)

    return jsonify(res), response.status_code
    

    


@app.route('/data',methods=['GET'])
def get_data():
    response = {"error":"No parameters were specified"}

    auth = request.headers.get('Authorization')
    host = f'{settings.MOCK_HOST}:{settings.MOCK_PORT}'
    headers = {'Host': host,
               'Authorization': auth}
    location = f"http://{host}/data"
    resp = requests.get(location,headers=headers)
    
    data = json.loads(resp.text)["data"]
    print(f"\n\ndata: \n{str(data)}\n-------------\n\n")

    if 'data_id' in request.args:
        data_id = request.args.get('data_id')
        if data_id in data:
            response = data[data_id]
            return jsonify(response), 200
        else:
            response = {"error":"Specified id not found"}
            return jsonify(response), 404
    
    if 'data_title' in request.args:
        data_title = unquote(request.args.get('data_title'))
        print(f"data_title: {data_title}")
        for rec_id, record in data.items():
            print(f"record: {record}")
            if record["title"] == data_title:
                response = record
                return jsonify(response), 200

        response = {"error":"Specified title not found"}
        return jsonify(response), 404

    return jsonify(response), 400


if __name__ == '__main__':
    host, port = settings.APP_HOST, settings.APP_PORT
    run_app(host, port)