"""
doctring for module test_string.py
"""
import random
import pytest


@pytest.fixture
def t_str():
    return rand_string()


@pytest.fixture
def str_list():
    return [rand_string() for _ in range(10)]


def join_expected_val(sep, iterable):
    result_string = ""
    for i in range(len(iterable)):
        result_string = result_string + iterable[i]
        if i == (len(iterable) - 1):
            continue
        result_string = result_string + sep
    return result_string


@pytest.fixture
def t_index_data(t_str):
    # pick up one of the string characters
    char = t_str[random.randint(0, len(t_str)-1)]
    char_index = 0
    for i in range(len(t_str)):
        if (char == t_str[i]):
            char_index = i
            break
    return (t_str, char, char_index)


@pytest.fixture
def t_count_data(t_str):
    count = 0
    char = t_str[random.randint(0, len(t_str)-1)]
    for c in t_str:
        if char == c:
            count = count + 1
    return (t_str, char, count)


def rand_string():
    s = ""
    for _ in range(10):
        s = s + chr(random.randint(ord('A'), ord('Z')))
    return s


class TestString:

    def test_join(self, t_str, str_list):
        res = t_str.join(str_list)
        exp = join_expected_val(t_str, str_list)
        assert res == exp

    @pytest.mark.parametrize('nonstring', [[0, 1, 2], None])
    def test_join_nonstring(self, t_str, nonstring):
        with pytest.raises(TypeError):
            t_str.join(nonstring)


def test_index(t_index_data):
    t_str, char, char_index = t_index_data
    assert t_str.index(char) == char_index


def test_in(t_index_data):
    t_str, char, char_index = t_index_data
    assert char in t_str


def test_count(t_count_data):
    t_str, char, count = t_count_data
    assert t_str.count(char) == count


def test_count_empty(t_str):
    assert "".count("") == 1
    assert "".count(t_str) == 0
