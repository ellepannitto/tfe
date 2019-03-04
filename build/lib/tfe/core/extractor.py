import logging
import os

import tfe.utils.files as futils

logger = logging.getLogger(__name__)

__all__ = ('extract_needed_words')


def extract_needed_words(output_dirpath, datasets_dirpath, fillers_dirpath):

    output_filepath = futils.get_needed_words_file(output_dirpath)
    dataset_words = set()
    needed_words = set()
    for fname in os.listdir(datasets_dirpath):
        with open(os.path.join(datasets_dirpath, fname), encoding='utf-8') as input_stream:
            for line in input_stream:
                linesplit = line.split('\t')
                dataset_words.add(linesplit[0].strip())
                dataset_words.add(linesplit[1].strip())

    for fname in os.listdir(fillers_dirpath):
        if fname.endswith('plain.txt'):
            idx = 1
        elif fname.endswith('deps.txt'):
            idx = 2

        with open(os.path.join(fillers_dirpath, fname), encoding='utf-8') as input_stream:
            for line in input_stream:
                linesplit = line.strip().split()
                if linesplit[0] in dataset_words:
                    needed_words.add(linesplit[0])
                    if idx == 1:
                        needed_words.add(linesplit[idx].strip())
                    elif linesplit[idx] in ['sbj', 'obj', 'loc', 'with']:
                        needed_words.add(linesplit[idx].strip())

    with open(output_filepath, 'w', encoding='utf-8') as output_stream:
        print('\n'.join(needed_words), file=output_stream)
        print('\n'.join(dataset_words), file=output_stream)

    return dataset_words, needed_words
