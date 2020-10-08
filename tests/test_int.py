"""
docstring
"""
import random
import pytest

from random import randint


class TestInt:
    @pytest.mark.parametrize("values", [(0, 0, 1),
                                        (0, randint(0, 10), 0),
                                        (2, 2, 4),
                                        (0.1, -1, 10)])
    def test_power(self, values):
        v1, v2, v3 = values
        assert v1**v2 == v3

    @pytest.mark.parametrize("values", [(0, (r := randint(1, 10)), r),
                                        (1, 1, 2),
                                        (2, -1, 1),
                                        (0, 0, 0)])
    def test_sum(self, values):
        v1, v2, v3 = values
        assert v1 + v2 == v3

    @pytest.mark.parametrize("values", [(0, 0),
                                        (1, 1),
                                        (-1, 1)])
    def test_abs(self, values):
        v1, v2 = values
        assert abs(v1) == v2

    @pytest.mark.parametrize("values", [(0, 0),
                                        (1, -1),
                                        (-1, 1)])
    def test_negate(self, values):
        v1, v2 = values
        assert v1 == -v2

    @pytest.mark.parametrize("values", [(0, randint(-100, 100), 0),
                                        (2, 3, 6),
                                        (2, -3, -6),
                                        (-3, 2, -6),
                                        (-3, -2, 6)])
    def test_prod(self, values):
        v1, v2, v3 = values
        assert v1 * v2 == v3

    @pytest.mark.parametrize("values", [(0, 0, 0),
                                        (0, 1, -1),
                                        (0, (r1 := randint(1, 100)), -r1),
                                        (0, -(r2 := randint(1, 100)), r2),
                                        (2, 1, 1),
                                        (-1, -2, 1)])
    def test_diff(self, values):
        v1, v2, v3 = values
        assert v1 - v2 == v3
