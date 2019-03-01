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
