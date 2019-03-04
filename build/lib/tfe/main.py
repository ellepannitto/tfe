"""Welcome to thematic-fit.estimation.

This is the entry point of the application.
"""
import os

import argparse
import logging
import logging.config

import tfe.utils.config as cutils
import tfe.utils.parsing as putils
import tfe.core.extractor as extractor
import tfe.core.generator as generator
import tfe.core.evaluator as evaluator


logging.config.dictConfig(
    cutils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def _extract_needed_words(args):
    if not args.output:
        output_dirpath = os.path.dirname(args.fillers_dirpath)
    else:
        output_dirpath = args.output
    if not os.path.exists(output_dirpath):
        logger.info('Creating directory {}'.format(output_dirpath))
        os.makedirs(output_dirpath)
    else:
        logger.info('Saving to directory {}'.format(output_dirpath))

    extractor.extract_needed_words(output_dirpath, args.datasets_dirpath,
                                   args.fillers_dirpath)


def _generate_npz_spaces(args):
    if not args.output:
        output_dirpath = os.path.dirname(args.spaces_dirpath)
    else:
        output_dirpath = args.output
    if not os.path.exists(output_dirpath):
        logger.info('Creating directory {}'.format(output_dirpath))
        os.makedirs(output_dirpath)
    else:
        logger.info('Saving to directory {}'.format(output_dirpath))

    needed_words_filepath = None
    if args.needed_words:
        needed_words_filepath = args.needed_words

    generator.generate_npz_spaces(output_dirpath, args.spaces_dirpath,
                                  needed_words_filepath)


def _generate_prototypes(args):
    if not args.output:
        output_dirpath = os.path.dirname(args.space_filepath)
    else:
        output_dirpath = args.output
    if not os.path.exists(output_dirpath):
        logger.info('Creating directory {}'.format(output_dirpath))
        os.makedirs(output_dirpath)
    else:
        logger.info('Saving to directory {}'.format(output_dirpath))

    generator.generate_prototypes(output_dirpath, args.space_filepath,
                                  args.fillers_filepath, args.num_fillers,
                                  args.needed_words)


def _evaluate(args):
    if not args.output:
        output_dirpath = os.path.dirname(args.dataset_filepath)
    else:
        output_dirpath = args.output
    if not os.path.exists(output_dirpath):
        logger.info('Creating directory {}'.format(output_dirpath))
        os.makedirs(output_dirpath)
    else:
        logger.info('Saving to directory {}'.format(output_dirpath))
    evaluator.evaluate(output_dirpath, args.dataset_filepath,
                       args.prototypes_filepath, args.space_filepath)

def main():
    """Launch thematic-fit-estimation."""
    parser = argparse.ArgumentParser(prog='tfe')
    subparsers = parser.add_subparsers()

    parser_needed_words = subparsers.add_parser(
        'extract-needed-words', formatter_class=argparse.RawTextHelpFormatter,
        help='extracts a list of needed words from datasets and fillers')
    parser_needed_words.add_argument(
        '-o', '--output', help='absolute path to output directory. '
        'If not set, will default to fillers directory.')
    parser_needed_words.add_argument(
        '-d', '--datasets-dirpath', required=True, type=putils.dir,
        help='absolute path to directory containing datasets.')
    parser_needed_words.add_argument(
        '-f', '--fillers-dirpath', required=True, type=putils.dir,
        help='absolute path to directory containing fillers.')
    parser_needed_words.set_defaults(func=_extract_needed_words)

    parser_generate_npz_spaces = subparsers.add_parser(
        'generate-npz-space', formatter_class=argparse.RawTextHelpFormatter,
        help='creates npz space and index from sparse or dense matrix on txt')
    parser_generate_npz_spaces.add_argument(
        '-o', '--output', help='absolute path to output directory. If not set, '
        'will default to input directory')
    parser_generate_npz_spaces.add_argument(
        '-s', '--spaces-dirpath', required=True, type=putils.dir,
        help='absolute path to directory containing distributional spaces.')
    parser_generate_npz_spaces.add_argument(
        '-n', '--needed-words', help='absolute path to needed words file. '
        'If not set, the whole space will be saved to npz format.')
    parser_generate_npz_spaces.set_defaults(func=_generate_npz_spaces)

    parser_generate_prototypes = subparsers.add_parser(
        'generate-prototypes', formatter_class=argparse.RawTextHelpFormatter,
        help='creates prototype vectors')
    parser_generate_prototypes.add_argument(
        '-o', '--output', help='absolute path to output '
        'directory. If not set, will default to space directory')
    parser_generate_prototypes.add_argument(
        '-s', '--space-filepath', required=True, type=putils.npz,
        help='absolute path to DSM. It must be either in npz or npy format.')
    parser_generate_prototypes.add_argument(
        '-f', '--fillers-filepath', required=True, help='absolute path to '
        'fillers file.')
    parser_generate_prototypes.add_argument(
        '-n', '--num-fillers', required=True, type=int,
        help='number of considered fillers')
    parser_generate_prototypes.add_argument(
        '-w', '--needed-words', required=True, help='absolute path to needed '
        'words file.')
    parser_generate_prototypes.set_defaults(func=_generate_prototypes)

    parser_evaluate = subparsers.add_parser(
        'evaluate-correlation', formatter_class=argparse.RawTextHelpFormatter,
        help='evaluates Spearmann\'s rank correlation')
    parser_evaluate.add_argument(
        '-o', '--output', help='absolute path to output directory. If not set, '
        'will default to dataset directory')
    parser_evaluate.add_argument(
        '-d', '--dataset-filepath', required=True, type=putils.datasets,
        help='absolute filepath to dataset. Supported datasets: mcrae.txt, '
        'pado.txt, ferretti-instruments.txt, ferretti-locations.txt')
    parser_evaluate.add_argument(
        '-p', '--prototypes-filepath', required=True, help='absolute filepath to '
        'prototypes.')
    parser_evaluate.add_argument(
        '-s', '--space-filepath', required=True, type=putils.npz,
        help='absolute filepath to distributional space. '
        'This must be in npy or npz format.')
    parser_evaluate.set_defaults(func=_evaluate)

    args = parser.parse_args()
    args.func(args)
