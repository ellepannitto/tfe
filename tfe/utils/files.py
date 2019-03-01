"""Files utils."""

import os
import logging

logger = logging.getLogger(__name__)

__all__ = ('get_needed_words_file')


def get_needed_words_file(output_dirpath):
    return os.path.join(output_dirpath, 'needed_words.txt')


def get_npy_filepath(output_dirpath, space_filepath):
    basename_filepath = os.path.basename(space_filepath).strip('.gz')
    return os.path.join(output_dirpath, '{}.npy'.format(basename_filepath))


def get_npz_filepath(output_dirpath, space_filepath):
    basename_filepath = os.path.basename(space_filepath).strip('.gz')
    return os.path.join(output_dirpath, '{}.npz'.format(basename_filepath))


def get_rows_vocab(output_dirpath, space_filepath):
    basename_filepath = os.path.basename(space_filepath).strip('.gz')
    return os.path.join(output_dirpath, '{}.row.vocab'.format(basename_filepath))


def get_cols_vocab(output_dirpath, space_filepath):
    basename_filepath = os.path.basename(space_filepath).strip('.gz')
    return os.path.join(output_dirpath, '{}.col.vocab'.format(basename_filepath))


def get_prototype_filepath(output_dirpath, space_filepath, fillers_filepath,
                           fillers_number):

    space_basename = os.path.basename(space_filepath).strip('.npz').strip('.npy')
    fillers_basename = os.path.basename(fillers_filepath)

    s = 'prototypes.{}.{}.top-{}.npy'.format(space_basename, fillers_basename,
                                             fillers_number)
    out_filepath = os.path.join(output_dirpath, s)

    return out_filepath

def get_prototype_vocab_filepath(output_dirpath, space_filepath, fillers_filepath,
                           fillers_number):

    space_basename = os.path.basename(space_filepath).strip('.npz').strip('.npy')
    fillers_basename = os.path.basename(fillers_filepath)

    s = 'prototypes.{}.{}.top-{}.vocab'.format(space_basename, fillers_basename,
                                               fillers_number)
    out_filepath = os.path.join(output_dirpath, s)

    return out_filepath
