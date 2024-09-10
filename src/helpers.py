"""
The helpers module defines helpers used across the project
"""

from itertools import islice


def batched(iterable, n):
    """
    A generator helper function that batches the iterable
    and returns values in batches of n
    """
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch
