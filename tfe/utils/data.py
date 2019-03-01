"""Data utils."""

import os
import logging

logger = logging.getLogger(__name__)

__all__ = ('load_wordlist')


def load_wordlist(input_filepath):
    ret = set()
    with open(input_filepath) as input_stream:
        for line in input_filepath:
            ret.add(line.strip())

    return ret
