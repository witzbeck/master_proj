from pytest import fixture

from model.features import Features


@fixture(scope="module")
def features():
    return Features()
