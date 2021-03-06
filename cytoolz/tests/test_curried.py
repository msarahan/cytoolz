import cytoolz
import cytoolz.curried
from cytoolz.curried import (take, first, second, sorted, merge_with, reduce,
                           merge, operator as cop)
from collections import defaultdict
from operator import add


def test_take():
    assert list(take(2)([1, 2, 3])) == [1, 2]


def test_first():
    assert first is cytoolz.itertoolz.first


def test_merge():
    assert merge(factory=lambda: defaultdict(int))({1: 1}) == {1: 1}
    assert merge({1: 1}) == {1: 1}
    assert merge({1: 1}, factory=lambda: defaultdict(int)) == {1: 1}


def test_merge_with():
    assert merge_with(sum)({1: 1}, {1: 2}) == {1: 3}


def test_merge_with_list():
    assert merge_with(sum, [{'a': 1}, {'a': 2}]) == {'a': 3}


def test_sorted():
    assert sorted(key=second)([(1, 2), (2, 1)]) == [(2, 1), (1, 2)]


def test_reduce():
    assert reduce(add)((1, 2, 3)) == 6


def test_module_name():
    assert cytoolz.curried.__name__ == 'cytoolz.curried'


def test_curried_operator():
    for k, v in vars(cop).items():
        if not callable(v):
            continue

        if not isinstance(v, cytoolz.curry):
            try:
                # Make sure it is unary
                # We cannot use isunary because it might be defined in C.
                v(1)
            except TypeError:
                raise AssertionError(
                    'cytoolz.curried.operator.%s is not curried!' % k,
                )

    # Make sure this isn't totally empty.
    assert len(set(vars(cop)) & set(['add', 'sub', 'mul'])) == 3
