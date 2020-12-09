import pytest
import time
import random
import json
from HW_6.socket_client import SocketClient
from HW_6 import my_app
from HW_6 import settings
from HW_6.mock_server import MockHTTPServer
from urllib.parse import quote


#@pytest.fixture(scope='session')
def app_server():
    server = MockHTTPServer(settings.MOCK_HOST,settings.MOCK_PORT)
    server.start()
    yield server
    server.stop()

@pytest.fixture(scope='session', autouse=True)
def app_mock():
    my_app.run_app(settings.APP_HOST, settings.APP_PORT)
    mock_server = MockHTTPServer(settings.MOCK_HOST,settings.MOCK_PORT)
    mock_server.start()

    yield
    client_mock = SocketClient(settings.MOCK_HOST,settings.MOCK_PORT)
    client_app = SocketClient(settings.APP_HOST, settings.APP_PORT)
    
    client_app.request(method="GET",target="/shutdown")
    try:
        client_mock.request(method="GET",target="/shutdown")
    except:
        pass
    
@pytest.fixture(scope="function")
def client_mock():
    return SocketClient(settings.MOCK_HOST,settings.MOCK_PORT)

@pytest.fixture(scope="function")
def client_app():
    return SocketClient(settings.APP_HOST,settings.APP_PORT)

# приложение поднято, а мок не поднят.
# поднимем приложение, которое ходит в неподнятый мок.
@pytest.mark.skip
@pytest.mark.MOCK
def test_app_up_mock_down():
    host, port = settings.APP_HOST, settings.APP_PORT
    my_app.run_app(host, port)
    # подождём пока приложение запуститься
    time.sleep(2)
    
    # делаем запрос к приложению
    client = SocketClient(host=host,port=port)
    resp_check = client.request(method="GET",target=f"/checkExternalService")
    print(f"resp_check: {resp_check}")

    resp = client.request(method="GET",target="/shutdown")
    print(resp)

    # приложение внутри пытается сходить в мок,
    # обламывается, потому что мы его не подняли
    # сообщает нам что внешний сервис недоступен
    # проверяем это
    assert resp_check["status_code"] == 504
    assert resp_check["body"] == "Can't reach external service"

# приложение поднято, а мок не отвечает (timeout)
@pytest.mark.MOCK
def test_app_up_mock_not_responding(client_mock, client_app):
    # устанавливаем в мок большой таймаут
    client_mock.request(method="POST",
                        target="/setupMock/timeout",
                        body=json.dumps({"timeout":10}))
    time.sleep(0.2)

    # делаем запрос к приложению
    resp = client_app.request(method="GET",target=f"/checkExternalService")
    # приложение внутри пытается сходить в мок,
    # ждёт, потому что в моке sleep(),
    # сообщает нам что внешний сервис недоступен
    # проверяем это
    assert resp["status_code"] == 504
    assert resp["body"] == "External service not responding (timeout)"


# приложение сходило в мок, а мок отдал 500
@pytest.mark.MOCK
def test_mock_server_error(client_mock, client_app):

    uid, code = settings.CAUSE_500.split(",")
    # делаем запрос к приложению
    resp = client_app.request(method="GET",target=f"/authApi?uid={uid}&code={code}")
    assert resp["status_code"] == 504
    assert resp["body"] == "External service error"


# ----------------------------------------------------------------
# мои тесты:

@pytest.mark.MOCK
def test_get_by_id (client_app):
    # тестируем фильтрацию
    auth = random.choice(list(settings.MOCK_DATA["data"].keys()))
    rand_id = random.choice(list(settings.MOCK_DATA["data"][auth]["data"].keys()))
    data_text = settings.MOCK_DATA["data"][auth]["data"][rand_id]["text"]
    data_title = settings.MOCK_DATA["data"][auth]["data"][rand_id]["title"]

    headers = {'Authorization': auth}
    location = f"/data?data_id={rand_id}"
    resp = client_app.request(method="GET",target=location,headers=headers)
    
    data = json.loads(resp["body"])

    assert resp["status_code"] == 200
    assert data["text"] == data_text
    assert data["title"] == data_title

@pytest.mark.MOCK
def test_get_by_title (client_app):
    # тестируем фильтрацию
    auth = random.choice(list(settings.MOCK_DATA["data"].keys()))
    rand_id = random.choice(list(settings.MOCK_DATA["data"][auth]["data"].keys()))
    data_text = settings.MOCK_DATA["data"][auth]["data"][rand_id]["text"]
    data_title = settings.MOCK_DATA["data"][auth]["data"][rand_id]["title"]

    headers = {'Authorization': auth}
    location = f"/data?data_title={quote(data_title)}"
    resp = client_app.request(method="GET",target=location,headers=headers)
    
    data = json.loads(resp["body"])

    assert resp["status_code"] == 200
    assert data["text"] == data_text
    assert data["title"] == data_title

@pytest.mark.MOCK
def test_get_by_id_absent (client_app):
    # тестируем фильтрацию
    auth = random.choice(list(settings.MOCK_DATA["data"].keys()))
    absent_id = settings.ABSENT_ID

    headers = {'Authorization': auth}
    location = f"/data?data_id={absent_id}"
    resp = client_app.request(method="GET",target=location,headers=headers)
    
    data = json.loads(resp["body"])

    assert resp["status_code"] == 404
    assert data["error"] == "Specified id not found"


@pytest.mark.MOCK
def test_get_by_title_absent (client_app):
    # тестируем фильтрацию
    auth = random.choice(list(settings.MOCK_DATA["data"].keys()))
    absent_title = settings.ABSENT_TITLE

    headers = {'Authorization': auth}
    location = f"/data?data_title={quote(absent_title)}"
    resp = client_app.request(method="GET",target=location,headers=headers)
    
    data = json.loads(resp["body"])

    assert resp["status_code"] == 404
    assert data["error"] == "Specified title not found"

@pytest.mark.MOCK
def test_get_no_params (client_app):
    auth = random.choice(list(settings.MOCK_DATA["data"].keys()))
    headers = {'Authorization': auth}
    location = f"/data"
    resp = client_app.request(method="GET",target=location,headers=headers)
    
    data = json.loads(resp["body"])

    assert resp["status_code"] == 400
    assert data["error"] == "No parameters were specified"
