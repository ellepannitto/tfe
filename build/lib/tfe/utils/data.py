"""Data utils."""

import os
import logging
import collections
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
    input_filename = space_filepath.strip('.npz').strip('.npy')+'{}.vocab'.format(ext)

    ret = {}
    with open(input_filename) as input_stream:
        for line in input_stream:
            linesplit = line.strip().split('\t')
            ret[linesplit[1]] = int(linesplit[0])

    return ret


def load_dense_model(space_filepath):
    return np.load(space_filepath)


def _load_mcrae(dataset_filepath):
    dataset = collections.defaultdict(list)
    with open(dataset_filepath) as fin:
        for line in fin:
            target, filler, s1, s2 = line.strip().split()
            dataset[target].append(("sbj", filler, float(s1)))
            dataset[target].append(("obj", filler, float(s2)))
    return dataset


def _load_pado(dataset_filepath):
    dataset = collections.defaultdict(list)
    with open(dataset_filepath) as fin:
        for line in fin:
            target, filler, rel, score = line.strip().split()
            dataset[target].append((rel, filler, float(score)))
    return dataset

def _load_ferretti_loc(dataset_filepath):
    dataset = collections.defaultdict(list)
    with open(dataset_filepath) as fin:
        for line in fin:
            target, filler, s1 = line.strip().split()
            dataset[target].append(("loc", filler, float(s1)))
    return dataset

def _load_ferretti_inst(dataset_filepath):
    dataset = collections.defaultdict(list)
    with open(dataset_filepath) as fin:
        for line in fin:
            target, filler, s1 = line.strip().split()
            dataset[target].append(("with", filler, float(s1)))
    return dataset


def load_dataset(dataset_filepath):
    basename = os.path.basename(dataset_filepath)

    if basename == 'pado.txt':
        return _load_pado(dataset_filepath)
    if basename == 'mcrae2.txt':
        return _load_mcrae(dataset_filepath)
    if basename == 'ferretti-locations.txt':
        return _load_ferretti_loc(dataset_filepath)
    if basename == 'ferretti-instruments.txt':
        return _load_ferretti_inst(dataset_filepath)
