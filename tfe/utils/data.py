"""Data utils."""

import os
import logging
import numpy as np
from scipy import sparse

logger = logging.getLogger(__name__)

__all__ = ('load_wordlist')


def load_wordlist(input_filepath):
    ret = set()
    with open(input_filepath) as input_stream:
        for line in input_stream:
            ret.add(line.strip())

    return ret


def load_sparse_model(space_filepath):
    return sparse.load_npz(space_filepath)


def load_model_vocabulary(space_filepath, ext):
    input_filename = space_filepath.strip('.npz').strip('.npy')+'.{}.vocab'.format(ext)

    ret = {}
    with open(input_filename) as input_stream:
        for line in input_stream:
            linesplit = line.strip().split('\t')
            ret[linesplit[1]] = int(linesplit[0])

    return ret


def load_dense_model(space_filepath):
    return np.load(space_filepath)
