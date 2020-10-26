import json
from urllib.parse import urljoin

import requests


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.login(email, password)

    def _request(self, method, location, data={}):

        url = urljoin(self.base_url, location)

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # важно чтобы этот заголовок совпадал со значением csrftoken в куках запросов
            'X-CSRFToken': self.auth_cookies["csrftoken"],
            'Content-Type': 'application/json'
        }

        return requests.request(method, url, headers=headers, data=data, cookies=self.auth_cookies)

    def login(self, email, password):
        # Базовый URL авторизации отличается от базового URL для API
        # поэтому не используем общий метод _request
        url = "https://auth-ac.my.com/auth"

        form_data = f'email={email}&password={password}&continue=https%3A//target.my.com/auth/mycom%3Fstate%3Dtarget_login%253D1%2526ignore_opener%253D1%23email&failure=https%3A//account.my.com/login/%3Fcontinue%3Dhttps%253A%252F%252Faccount.my.com&nosavelogin=0'

        headers = {
            'Referer': 'https://account.my.com/'
        }

        # при запросе происходит три редиректа с
        # которых можно собрать необходимые куки
        response = requests.post(url, headers=headers, data=form_data)

        #собираем все куки
        all_cookies = {}
        for resp in response.history:
            for cookie in resp.cookies:
                all_cookies[cookie.name] = cookie.value

        # собираем нужные для API куки
        self.auth_cookies = {"mc": all_cookies["mc"],
                             "sdcs": all_cookies["sdcs"]}

        # ещё нужен csrf токен
        # eго можно получить в куках ответа на этот запрос
        url = "https://target.my.com/csrf/"

        response = requests.request("GET", url, cookies=self.auth_cookies)

        self.auth_cookies["csrftoken"] = response.cookies.get("csrftoken")

        all_cookies.update(self.auth_cookies)
        return all_cookies

    def create_segment(self, name, segment_params: dict = None):
        location = "api/v2/remarketing/segments.json?"

        if segment_params is None:
            segment_params = {"name": name,
                              "pass_condition": 1,
                              "relations": [{
                                  "object_type": "remarketing_player",
                                  "params": {
                                      "type": "positive",
                                      "left": 365,
                                      "right": 0}}]}

        response = self._request(
            "POST", location, data=json.dumps(segment_params))

        return json.loads(response.text.encode('utf16'))

    def delete_segment(self, id):
        location = f"api/v2/remarketing/segments/{str(id)}.json"

        response = self._request("DELETE", location)

        if response.status_code == 204:
            #No content, delete successfull
            return True

        return json.loads(response.text.encode('utf16'))

    def get_all_segments(self):
        location = "api/v2/remarketing/segments.json?"

        response = self._request("GET", location)

        return json.loads(response.text.encode('utf16'))

    def get_segment(self, id):
        location = f"api/v2/remarketing/segments/{str(id)}.json"

        response = self._request("GET", location)

        return json.loads(response.text.encode('utf16'))
