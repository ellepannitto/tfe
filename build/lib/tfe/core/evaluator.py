import logging
import os
from scipy import stats
from scipy.spatial.distance import cosine

import tfe.utils.files as futils
import tfe.utils.data as dutils

logger = logging.getLogger(__name__)

__all__ = ('evaluate')


def _evaluate_sparse(output_dirpath, dataset_filepath, prototype_filepath,
                     model_filepath):
    output_filepath = futils.get_evalutation_output(output_dirpath,
                                                    dataset_filepath,
                                                    prototype_filepath)

    model = dutils.load_sparse_model(model_filepath)
    model_vocabulary_rows = dutils.load_model_vocabulary(model_filepath, '.row')
    dataset = dutils.load_dataset(dataset_filepath)
    prototypes = dutils.load_dense_model(prototype_filepath)
    prototypes_vocabulary = dutils.load_model_vocabulary(prototype_filepath, '')

    true_scores = []
    predict_scores = []
    for target in dataset:
        for rel, filler, score in dataset[target]:
            proto_row = target+'/'+rel
            if filler in model_vocabulary_rows:
                if proto_row in prototypes_vocabulary:
                    filler_v = model.getrow(model_vocabulary_rows[filler]).todense()
                    cosine_score = 1-cosine(filler_v, prototypes[prototypes_vocabulary[proto_row], :])

                    true_scores.append(score)
                    predict_scores.append(cosine_score)
                else:
                    logger.info('Target {} + rel {} not in prototypes'.format(target, rel))
            else:
                logger.info('Filler {} not in model'.format(filler))
    correlation = stats.spearmanr(true_scores, predict_scores)[0]

    logger.info('Correlation: {}'.format(correlation))

    with open(output_filepath, 'w') as output_stream:
        print('Correlation: {}'.format(correlation), file=output_stream)

def _evaluate_dense(output_dirpath, dataset_filepath, prototype_filepath,
                    model_filepath):

    output_filepath = futils.get_evalutation_output(output_dirpath,
                                                    dataset_filepath,
                                                    prototype_filepath)

    model = dutils.load_dense_model(model_filepath)
    model_vocabulary_rows = dutils.load_model_vocabulary(model_filepath, '.row')
    dataset = dutils.load_dataset(dataset_filepath)
    prototypes = dutils.load_dense_model(prototype_filepath)
    prototypes_vocabulary = dutils.load_model_vocabulary(prototype_filepath, '')


    true_scores = []
    predict_scores = []
    for target in dataset:
        for rel, filler, score in dataset[target]:
            proto_row = target+'/'+rel
            if filler in model_vocabulary_rows:
                if proto_row in prototypes_vocabulary:
                    filler_v = model[model_vocabulary_rows[filler], :]
                    cosine_score = 1-cosine(filler_v, prototypes[prototypes_vocabulary[proto_row], :])

                    true_scores.append(score)
                    predict_scores.append(cosine_score)
                else:
                    logger.info('Target {} + rel {} not in prototypes'.format(target, rel))
            else:
                logger.info('Filler {} not in model'.format(filler))
    correlation = stats.spearmanr(true_scores, predict_scores)[0]

    logger.info('Correlation: {}'.format(correlation))

    with open(output_filepath, 'w') as output_stream:
        print('Correlation: {}'.format(correlation), file=output_stream)


def evaluate(output_dirpath, dataset_filepath, prototype_filepath,
             model_filepath):

    if model_filepath.endswith('.npz'):
        _evaluate_sparse(output_dirpath, dataset_filepath, prototype_filepath,
                         model_filepath)
    if model_filepath.endswith('.npy'):
        _evaluate_dense(output_dirpath, dataset_filepath, prototype_filepath,
                        model_filepath)
