"""
docstring
"""
import random
from random import randint
import pytest


@pytest.fixture
def t_dict(t_list_data):
    return t_list_data[0]


@pytest.fixture
def t_item():
    return (str(r := randint(0, 100)), r)


@pytest.fixture
def t_list_data():
    t_list = ["k" + str(num_key)
              for num_key in {randint(0, 100) for _ in range(10)}]
    t_dict = {}
    for item in t_list:
        t_dict[str(item)] = item
    return (t_dict, t_list)


class TestDict:

    def test_to_list(self, t_list_data):
        t_dict, t_list = t_list_data
        assert list(t_dict) == t_list

    @pytest.mark.parametrize("item", [("some string", "value"),
                                      (lambda x: x**2, "value"),
                                      (randint(0, 100), "value")])
    def test_add(self, t_dict, item):
        key, val = item
        t_dict[key] = val
        assert t_dict[key] == val

    def test_get(self, t_dict, t_item):
        key, val = t_item
        t_dict[key] = val
        assert t_dict.get(key) == val

    def test_get_absent(self, t_dict):
        absent_key = list(t_dict.keys())[0]
        t_dict.pop(absent_key)
        assert t_dict.get(absent_key) is None

    def test_del(self, t_dict):
        del_item_key = list(t_dict.keys())[0]
        del t_dict[del_item_key]
        assert del_item_key not in t_dict

    def test_del_absent(self, t_dict):
        del_item_key = list(t_dict.keys())[0]
        del t_dict[del_item_key]
        with pytest.raises(KeyError):
            del t_dict[del_item_key]
