import uuid

import pytest
from tests_api.api.client import ApiClient
from tests_ui.ui.settings import credentials


class TestApi:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient("https://target.my.com", credentials["email"], credentials["password"])

    @pytest.fixture(scope='function')
    def segment_id_for_delete(self, client: ApiClient):
        seg_id = client.create_segment("test name")["id"]

        return seg_id

    @pytest.mark.API
    def test_create(self, client: ApiClient):
        name = str(uuid.uuid4)

        id_created = client.create_segment(name)["id"]

        segment = client.get_segment(id_created)

        assert ("id" in segment) and (segment["id"] == id_created)

        #сегмент создался успешно, удалим его
        client.delete_segment(id_created)

    @pytest.mark.API
    def test_delete(self, client: ApiClient, segment_id_for_delete):
        seg_id = segment_id_for_delete

        # Если сегмент удалился, вернётся True
        # иначе вернётся Json с описанием ошибки
        delete_res = client.delete_segment(seg_id)

        # Пытаемся получить только что удалённый сегмент
        res = client.get_segment(seg_id)

        # если не пришла ошибка, то сегмент не удалился
        # ожидаем конкретный код, что запрашиваемого сегмента нет
        assert res["error"]["code"] == "not_found"

        assert delete_res is True
