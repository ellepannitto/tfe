import logging
import os
import gzip
import collections
import numpy as np
from scipy import sparse

import tfe.utils.files as futils
import tfe.utils.data as dutils

logger = logging.getLogger(__name__)

__all__ = ('generate_npz_spaces')


def _from_dense(output_dirpath, space_filepath, needed_words):
    output_filepath_matrix = futils.get_npy_filepath(output_dirpath, space_filepath)
    output_filepath_rows = futils.get_rows_vocab(output_dirpath, space_filepath)
    row_to_idx = {}
    last_idx_row = 0
    M = []
    with gzip.open(space_filepath, 'rt', errors='ignore') as input_stream:
        for line in input_stream:
            linesplit = line.strip().split()
            row = linesplit[0][:-2]+"-"+linesplit[0][-1].lower()
            if not needed_words or row in needed_words:
                if row not in row_to_idx:
                    row_to_idx[row] = last_idx_row
                    last_idx_row += 1
                vector = np.array([float(x) for x in linesplit[1:]])
                M.append(vector)
    M = np.array(M)

    logger.info('Saving matrix to {}'.format(output_filepath_matrix))
    np.save(output_filepath_matrix, M)

    with open(output_filepath_rows, 'w', encoding='utf-8') as output_stream:
        for word, idx in row_to_idx.items():
            print('{}\t{}'.format(idx, word), file=output_stream)


def _from_sparse(output_dirpath, space_filepath, needed_words):
    output_filepath_matrix = futils.get_npz_filepath(output_dirpath, space_filepath)
    output_filepath_rows = futils.get_rows_vocab(output_dirpath, space_filepath)
    output_filepath_columns = futils.get_cols_vocab(output_dirpath, space_filepath)
    row_to_idx = {}
    last_idx_row = 0
    column_to_idx = {}
    last_idx_column = 0
    rows = []
    columns = []
    data = []
    with gzip.open(space_filepath, 'rt', errors='ignore') as input_stream:
        for line in input_stream:
            linesplit = line.strip().split('\t')
            row = linesplit[0]
            row = row[:-2]+"-"+row[-1].lower()
            column = linesplit[1]
            column = column[:-2]+'-'+column[-1].lower()

            score = float(linesplit[2])

            if not needed_words or row in needed_words:
                if row not in row_to_idx:
                    row_to_idx[row] = last_idx_row
                    last_idx_row += 1
                if column not in column_to_idx:
                    column_to_idx[column] = last_idx_column
                    last_idx_column += 1
                rows.append(row_to_idx[row])
                columns.append(column_to_idx[column])
                data.append(score)

    M = sparse.csr_matrix((data, (rows, columns)),
                          shape=(len(row_to_idx), len(column_to_idx)),
                          dtype='f')
    logger.info('Matrix info: {} non-zero entres, {} shape, {:.6f} density'
                .format(M.getnnz(), M.shape,
                        M.getnnz()*1.0/(M.shape[0]*M.shape[1])))
    logger.info('Saving matrix to {}.npz'.format(output_filepath_matrix))
    sparse.save_npz(output_filepath_matrix, M)

    with open(output_filepath_rows, 'w', encoding='utf-8') as output_stream:
        for word, idx in row_to_idx.items():
            print('{}\t{}'.format(idx, word), file=output_stream)

    with open(output_filepath_columns, 'w', encoding='utf-8') as output_stream:
        for word, idx in column_to_idx.items():
            print('{}\t{}'.format(idx, word), file=output_stream)



def generate_npz_spaces(output_dirpath, spaces_dirpath, needed_words_filepath):
    needed_words = set()
    if needed_words_filepath:
        needed_words = dutils.load_wordlist(needed_words_filepath)
    for fname in os.listdir(spaces_dirpath):
        logger.info('processing file {}'.format(fname))
        if fname.endswith('sparse.gz'):
            _from_sparse(output_dirpath, os.path.join(spaces_dirpath, fname),
                         needed_words)

        if fname.endswith('dense.gz'):
            _from_dense(output_dirpath, os.path.join(spaces_dirpath, fname),
                        needed_words)


def _load_deps(fname, needed_words):
    fillersdict = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(fname) as input_stream:
        for line in input_stream:
            target, rel, filler, score = line.strip().split()
            if target in needed_words:
                fillersdict[target][rel].append((filler, float(score)))

    for target in fillersdict:
        for rel in fillersdict[target]:
            fillersdict[target][rel] = \
                sorted(fillersdict[target][rel], key=lambda x: x[1], reverse=True)
    return fillersdict


def _load_plain(fname, needed_words):
    fillersdict = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(fname) as input_stream:
        for line in input_stream:
            target, filler, score = line.strip().split()
            if target in needed_words:
                fillersdict[target]["sbj"].append((filler, float(score)))
                fillersdict[target]["obj"].append((filler, float(score)))
                fillersdict[target]["loc"].append((filler, float(score)))
                fillersdict[target]["with"].append((filler, float(score)))
    for target in fillersdict:
        for rel in fillersdict[target]:
            fillersdict[target][rel] = \
                sorted(fillersdict[target][rel], key=lambda x: x[1], reverse=True)
    return fillersdict


def _generate_prototypes_sparse(output_dirpath, space_filepath,
                                fillers_filepath, fillers_number,
                                needed_words_filepath):

    output_prototypes_filepath = \
        futils.get_prototype_filepath(output_dirpath, space_filepath,
                                      fillers_filepath, fillers_number)
    output_prototypes_vocab_filepath = \
        futils.get_prototype_vocab_filepath(output_dirpath, space_filepath,
                                            fillers_filepath, fillers_number)

    needed_words = dutils.load_wordlist(needed_words_filepath)
    model = dutils.load_sparse_model(space_filepath)
    model_vocabulary_rows = dutils.load_model_vocabulary(space_filepath, ".row")

    prototypes = []
    if fillers_filepath.endswith('.plain.txt'):
        fillers = _load_plain(fillers_filepath, needed_words)

    if fillers_filepath.endswith('.deps.txt'):
        fillers = _load_deps(fillers_filepath, needed_words)
    word_to_idx = {}
    last_idx = 0
    for target in fillers:
        for rel in fillers[target]:
            temporary_centroid = np.zeros(model.shape[1])
            skipped_fillers = 0
            considered_fillers = fillers[target][rel][:fillers_number]
            for word, score in considered_fillers:
                if word in model_vocabulary_rows:
                    word_vector = model.getrow(model_vocabulary_rows[word]).todense()
                    temporary_centroid = np.sum([temporary_centroid, word_vector], axis=0)
                else:
                    skipped_fillers+=1

            proto_row = target+'/'+rel
            if not proto_row in word_to_idx:
                word_to_idx[proto_row]=last_idx
                last_idx+=1
            prototypes.append(temporary_centroid)
    prototypes = np.array(prototypes)
    np.save(output_prototypes_filepath, prototypes)

    with open(output_prototypes_vocab_filepath, 'w') as output_stream:
        for word, idx in word_to_idx.items():
            print('{}\t{}'.format(idx, word), file=output_stream)


def _generate_prototypes_dense(output_dirpath, space_filepath,
                               fillers_filepath, fillers_number,
                               needed_words_filepath):
    output_prototypes_filepath = \
        futils.get_prototype_filepath(output_dirpath, space_filepath,
                                      fillers_filepath, fillers_number)
    output_prototypes_vocab_filepath = \
        futils.get_prototype_vocab_filepath(output_dirpath, space_filepath,
                                            fillers_filepath, fillers_number)

    needed_words = dutils.load_wordlist(needed_words_filepath)
    model = dutils.load_dense_model(space_filepath)
    model_vocabulary_rows = dutils.load_model_vocabulary(space_filepath, ".row")

    prototypes = []
    if fillers_filepath.endswith('.plain.txt'):
        fillers = _load_plain(fillers_filepath, needed_words)

    if fillers_filepath.endswith('.deps.txt'):
        fillers = _load_deps(fillers_filepath, needed_words)

    word_to_idx = {}
    last_idx = 0
    for target in fillers:
        for rel in fillers[target]:
            temporary_centroid = np.zeros(model.shape[1])
            skipped_fillers = 0
            considered_fillers = fillers[target][rel][:fillers_number]
            for word, score in considered_fillers:
                if word in model_vocabulary_rows:
                    word_vector = model[model_vocabulary_rows[word],:]
                    temporary_centroid = np.sum([temporary_centroid, word_vector], axis=0)
                else:
                    skipped_fillers+=1

            proto_row = target+'/'+rel
            if not proto_row in word_to_idx:
                word_to_idx[proto_row]=last_idx
                last_idx+=1
            prototypes.append(temporary_centroid)
    prototypes = np.array(prototypes)
    np.save(output_prototypes_filepath, prototypes)

    with open(output_prototypes_vocab_filepath, 'w') as output_stream:
        for word, idx in word_to_idx.items():
            print('{}\t{}'.format(idx, word), file=output_stream)



def generate_prototypes(output_dirpath, space_filepath, fillers_filepath,
                        fillers_number, needed_words_filepath):

    if space_filepath.endswith('.npz'):
        _generate_prototypes_sparse(output_dirpath, space_filepath,
                                    fillers_filepath, fillers_number,
                                    needed_words_filepath)

    if space_filepath.endswith('.npy'):
        _generate_prototypes_dense(output_dirpath, space_filepath,
                                    fillers_filepath, fillers_number,
                                    needed_words_filepath)
