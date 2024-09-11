from konnsearch.helpers import batched


def test_batched():
    result = batched(range(1, 10), 4)
    assert list(result) == [(1, 2, 3, 4), (5, 6, 7, 8), (9,)]
