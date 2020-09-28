"""
here's a docstring for module test_list.py
"""
import random
import pytest


@pytest.fixture()
def t_list():
    """return list of random length, randomly filled with integers"""
    return [random.randint(0, 10) for _ in range(random.randint(10, 100))]


@pytest.fixture(scope='module')
def empty_list():
    """return empty list"""
    return []


@pytest.fixture(scope='module')
def noncomp_list():
    """return the list of non-comparable entities"""
    return [{str(r_int:=random.randint(0, 100)): r_int} for _ in range(1, 100)]


@pytest.mark.parametrize("elem", [(r_int:=random.randint(0, 100)),
                                  str(r_int)*4,
                                  {str(r_int): r_int},
                                  lambda x: x+r_int,
                                  list(range(r_int)),
                                  None])
def test_append(t_list, elem):
    """
    appending elements with different types to list
    """
    print(type(elem))
    t_list.append(elem)
    assert t_list[-1] == elem


def test_count(t_list, empty_list):
    """
    Test count method of list type
    """
    data = get_count_data(t_list)
    assert t_list.count(data['elem']) == data['count']
    assert empty_list.count(random.randint(0, 10)) == 0


def get_count_data(t_list):
    """
    Provide value to test count() method of list type
    """
    test_elem = random.randint(0, 9)
    count = 0
    for elem in t_list:
        if elem == test_elem:
            count = count + 1
    return {'elem': test_elem, 'count': count}


class TestMax:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, t_list, empty_list, noncomp_list):
        self.t_list = t_list
        self.empty_list = empty_list
        self.noncomp_list = noncomp_list

    def test_normal(self):
        """
        Normal case: list is not empty
        and cosists of comparable emelents
        """
        max_el = self.__max_el__()
        assert max(self.t_list) == max_el

    def test_empty(self):
        """Empty case: list is empty"""
        with pytest.raises(ValueError):
            max(self.empty_list)

    def test_noncomp(self):
        """
        Non-comparable case: list is not empty
        but consists of non-comparable elements
        """
        with pytest.raises(TypeError):
            max(self.noncomp_list)

    def __max_el__(self):
        """
        Provide max element to test max() method of type list
        """
        max_elem = self.t_list[0]
        for elem in self.t_list:
            if elem > max_elem:
                max_elem = elem
        return max_elem
