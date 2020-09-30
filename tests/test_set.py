"""
module docstring
"""
import random
from random import randint
import pytest


def f(x):
    return x


@pytest.fixture
def t_set():
    r = randint(1, 10)
    return {x for x in range(r)}


@pytest.fixture
def t_remove_data(t_set):
    set_len = randint(0, len(t_set))
    elem_to_remove = 0
    for elem in t_set:
        if (set_len:= set_len-1) == 0:
            elem_to_remove = elem
            break
    return (t_set, elem_to_remove)


@pytest.fixture
def t_subset_data(t_set):
    ss_len = randint(0, len(t_set)-1)  # subset length
    sub_set = set()
    for elem in t_set:
        if(ss_len:= ss_len-1) > 0:
            sub_set.add(elem)
        else:
            break
    res = (t_set, sub_set, True)
    if(swap:= random.choice([True, False])):
        res = (sub_set, t_set, False)
    return res


class TestAdd:

    @pytest.fixture(autouse=True)
    def setup(self, t_set):
        self.t_set = t_set

    @pytest.mark.parametrize("item", [{str(r:= randint(1, 100)): r},
                                      [x**2 for x in range(r)],
                                      {x**2 for x in range(r)}])
    def test_add_unhashable(self, item):
        with pytest.raises(TypeError):
            self.t_set.add(item)

    @pytest.mark.parametrize("item", ["some string", 1, f])
    def test_add_hashable(self, item):
        self.t_set.add(item)
        assert item in self.t_set


def test_remove(t_remove_data):
    t_set, elem = t_remove_data
    t_set.remove(elem)
    assert elem not in t_set


def test_remove_absent(t_set):
    with pytest.raises(KeyError):
        t_set.remove(randint(11, 100))


def test_issubset(t_subset_data):
    t_superset, t_subset, res = t_subset_data
    assert t_subset.issubset(t_superset) == res
