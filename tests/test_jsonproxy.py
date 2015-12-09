import pytest

from mtgjson.jsonproxy import JSONProxy


@pytest.fixture
def data():
    return {'foo': 'bar', 'int': 42, 'boolean': True, 'sublist': [1, 2, 3], }


@pytest.fixture
def prox(data):
    return JSONProxy(data)


def test_getattr_works(prox):
    assert prox.foo == 'bar'
    assert prox.int == 42
    assert prox.boolean
    assert prox.sublist == [1, 2, 3]


def test_setting_attributes(prox):
    prox.baz = 'baz'

    assert prox.baz == 'baz'


def test_overriding_attribute(prox):
    prox.int = -1

    assert prox.int == -1

    del prox.int

    assert prox.int == 42


def test_missing_attributes(prox):
    with pytest.raises(AttributeError):
        prox.not_set


def test_raw_retrieval(prox, data):
    assert prox._get_raw_data() == data
