"""Welcome to thematic-fit.estimation.

This is the entry point of the application.
"""
import os

import argparse
import logging
import logging.config

import tfe.utils.config as cutils
import tfe.core.extractor as extractor
import tfe.core.generator as generator


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
        needed_words_filepath = args.needed_words_filepath

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
                                  args.needed_words_filepath)

def main():
    """Launch thematic-fit-estimation."""
    parser = argparse.ArgumentParser(prog='tfe')
    subparsers = parser.add_subparsers()
    parser_needed_words = subparsers.add_parser(
        'extract_needed_words', formatter_class=argparse.RawTextHelpFormatter,
        help='extracts a list of needed words from dataset')
    parser_needed_words.add_argument('-o', '--output',
                                     help='absolute path to output directory. '
                                     'If not set, will default to fillers directory.')
    parser_needed_words.add_argument('-d', '--datasets-dirpath', required=True,
                                     help='absolute path to directory containing '
                                     'datasets.')
    parser_needed_words.add_argument('-f', '--fillers-dirpath', required=True,
                                     help='absolute path to directory containing '
                                     'fillers.')
    parser_needed_words.set_defaults(func=_extract_needed_words)

    parser_generate_npz_spaces = subparsers.add_parser(
        'generate-npz-space', formatter_class=argparse.RawTextHelpFormatter,
        help='creates npz space and index from sparse or dense matrix on txt')
    parser_generate_npz_spaces.add_argument(
        '-o', '--output', help='absolute path to output directory. If not set, '
        'will default to input directory')
    parser_generate_npz_spaces.add_argument(
        '-s', '--spaces-dirpath', required=True, help='absolute path to '
        'directory containing distributional spaces.')
    parser_generate_npz_spaces.add_argument(
        '-n', '--needed-words', help='absolute path to needed words file. '
        'If not set, the whole space will be saved to npz format.')
    parser_generate_npz_spaces.set_defaults(func=_generate_npz_spaces)

    parser_generate_prototypes = subparsers.add_parser(
        'generate-prototypes', formatter_class=argparse.RawTextHelpFormatter,
        help='creates prototype vectors')
    parser_generate_prototypes.add_argument(
        '-o', '--output', required=True, help='absolute path to output '
        'directory. If not set, will default to space directory')
    parser_generate_prototypes.add_argument(
        '-s', '--space-filepath', required=True, help='absolute path to DSM. '
        'It must be either in npz or npy format.')
    parser_generate_prototypes.add_argument(
        '-f', '--fillers-filepath', required=True, help='absolute path to DSM. '
        'It must be either in npz or npy format.')
    parser_generate_prototypes.add_argument(
        '-n', '--num-fillers', required=True, help='number of considered fillers')
    parser_generate_prototypes.add_argument(
        '-n', '--needed-words', required=True, help='absolute path to needed '
        'words file. If not set, the whole space will be saved to npz format.')
    parser_generate_prototypes.set_defaults(func=_generate_prototypes)

    # parser_count = subparsers.add_parser(
    #     'count', formatter_class=argparse.RawTextHelpFormatter,
    #     help='count words in input corpus')
    # parser_count.add_argument('-c', '--corpus', required=True,
    #                           help='an input .txt corpus to compute counts on')
    # parser_count.add_argument('-o', '--output',
    #                           help='absolute path to output directory. '
    #                                'If not set, will default to corpus dir')
    # parser_count.add_argument('-m', '--min-count', default=0, type=int,
    #                           help='omit words below this count in output'
    #                                'vocabulary')
    # parser_count.add_argument('-s', '--save', action='store_true',
    #                           help='save counts to output')
    # parser_count.set_defaults(func=_count)
    # parser_compute = subparsers.add_parser(
    #     'compute', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute entropy or pairwise cosine similarity metrics')
    # compute_sub = parser_compute.add_subparsers()
    # parser_compute_energy = compute_sub.add_parser(
    #     'energy', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute energy of .npz or .npy model')
    # parser_compute_energy.set_defaults(func=_compute_energy)
    # parser_compute_energy.add_argument(
    #     '-m', '--model', required=True,
    #     help='absolute path the .singvalues.npy or .npz file')
    # parser_compute_sentropy = compute_sub.add_parser(
    #     'sentropy', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute entropy of input singular values')
    # parser_compute_sentropy.set_defaults(func=_compute_sentropy)
    # parser_compute_sentropy.add_argument(
    #     '-m', '--model', required=True,
    #     help='absolute path the .singvalues.npy file')
    # parser_compute_lentropy = compute_sub.add_parser(
    #     'lentropy', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute language entropy from input .counts file')
    # parser_compute_lentropy.set_defaults(func=_compute_lentropy)
    # parser_compute_lentropy.add_argument(
    #     '-c', '--counts', required=True,
    #     help='input .counts counts file to compute entropy from')
    # parser_compute_cosine = compute_sub.add_parser(
    #     'cosine', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute pairwise cosine similarity between vocabulary items')
    # parser_compute_cosine.set_defaults(func=_compute_pairwise_cosines)
    # parser_compute_cosine.add_argument('-m', '--model', required=True,
    #                                    help='distributional space')
    # parser_compute_cosine.add_argument('-v', '--vocab', required=True,
    #                                    help='vocabulary mapping for dsm')
    # parser_compute_cosine.add_argument(
    #     '-o', '--output', help='absolute path to output directory. If not '
    #                            'set, will default to space dir')
    # parser_compute_cosine.add_argument('-n', '--num-threads', default=1,
    #                                    type=int, help='number of threads')
    # parser_compute_cosine.add_argument('-b', '--bin-size', default=0.1,
    #                                    type=float, help='bin size for the '
    #                                                     'distribution output')
    # parser_compute_sv_entropy = compute_sub.add_parser(
    #     'svec-entropy', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute entropy from input singular vectors matrix')
    # parser_compute_sv_entropy.set_defaults(func=_compute_singvectors_entropy)
    # parser_compute_sv_entropy.add_argument('-u', '--s-vectors', required=True,
    #                                        help='absolute path to .singvectors.npy '
    #                                        ' file')
    # parser_compute_sv_entropy.add_argument('-d', '--s-values', required=True,
    #                                        help='absolute path to .singvalues.npy '
    #                                        ' file')
    # parser_compute_sv_entropy.add_argument('-o', '--output',
    #                                        help='absolute path to output directory.'
    #                                        'If not set, will default to svectors dir.')
    # parser_compute_sv_ipr = compute_sub.add_parser(
    #     'svec-ipr', formatter_class=argparse.RawTextHelpFormatter,
    #     help='compute ipr from input singular vectors matrix')
    # parser_compute_sv_ipr.set_defaults(func=_compute_singvectors_ipr)
    # parser_compute_sv_ipr.add_argument('-u', '--s-vectors', required=True,
    #                                    help='absolute path to .singvectors.npy '
    #                                    ' file')
    # parser_compute_sv_ipr.add_argument('-d', '--s-values', required=True,
    #                                    help='absolute path to .singvalues.npy '
    #                                    ' file')
    # parser_compute_sv_ipr.add_argument('-o', '--output',
    #                                    help='absolute path to output directory.'
    #                                    'If not set, will default to svectors dir.')
    # parser_evaluate = subparsers.add_parser(
    #     'evaluate', formatter_class=argparse.RawTextHelpFormatter,
    #     help='evaluate a given distributional space against the MEN dataset')
    # parser_evaluate.set_defaults(func=_evaluate)
    # parser_evaluate.add_argument('-m', '--model', required=True,
    #                              help='absolute path to .npz matrix '
    #                                   'corresponding to the distributional '
    #                                   'space to evaluate')
    # parser_evaluate.add_argument('-v', '--vocab', required=True,
    #                              help='absolute path to .vocab file')
    # parser_generate = subparsers.add_parser(
    #     'generate', formatter_class=argparse.RawTextHelpFormatter,
    #     help='generate raw frequency count based model')
    # parser_generate.set_defaults(func=_generate)
    # parser_generate.add_argument('-c', '--corpus', required=True,
    #                              help='an input .txt corpus to compute \
    #                              counts on')
    # parser_generate.add_argument('-o', '--output',
    #                              help='absolute path to output directory. '
    #                              'If not set, will default to corpus dir')
    # parser_generate.add_argument('-m', '--min-count', default=0, type=int,
    #                              help='frequency threshold on vocabulary')
    # parser_generate.add_argument('-w', '--win-size', default=2, type=int,
    #                              help='size of context window')
    # parser_reduce = subparsers.add_parser(
    #     'reduce', formatter_class=argparse.RawTextHelpFormatter,
    #     help='reduce a space by composing singular vectors and values')
    # parser_reduce.set_defaults(func=_reduce)
    # parser_reduce.add_argument('-u', '--singvectors', required=True,
    #                            help='absolute path to .singvectors.npy')
    # parser_reduce.add_argument('-s', '--singvalues', required=True,
    #                            help='absolute path to .singvalues.npy')
    # parser_reduce.add_argument('-t', '--top', default=0, type=int,
    #                            help='keep all but top n highest singvalues')
    # parser_reduce.add_argument('-a', '--alpha', default=1.0,
    #                            type=restricted_alpha,
    #                            help='raise singvalues at power alpha')
    # parser_reduce.add_argument('-e', '--energy', default=100,
    #                            type=restricted_energy,
    #                            help='how much energy of the original sigma'
    #                                 'to keep')
    # parser_reduce.add_argument('-o', '--save', action='store_true',
    #                            help='whether or not to save the output '
    #                                 'reduced matrix')
    # parser_reduce.add_argument('-d', '--outputdir',
    #                            help='absolute path to output directory where'
    #                                 'to save model. If not set, will default'
    #                                 'to -u directory is -o is true')
    # parser_svd = subparsers.add_parser(
    #     'svd', formatter_class=argparse.RawTextHelpFormatter,
    #     help='apply svd to input matrix')
    # parser_svd.set_defaults(func=_svd)
    # parser_svd.add_argument('-m', '--model', required=True,
    #                         help='absolute path to .npz matrix '
    #                              'corresponding to the distributional '
    #                              'space to reduce via svd')
    # parser_svd.add_argument('-k', '--dim', default=0, type=int,
    #                         help='number of dimensions in final model')
    # parser_svd.add_argument('-c', '--compact', action='store_true',
    #                         help='whether or not to store a compact matrix')
    # parser_weigh = subparsers.add_parser(
    #     'weigh', formatter_class=argparse.RawTextHelpFormatter,
    #     help='weigh sparse matrix according to weighing function')
    # parser_weigh.set_defaults(func=_weigh)
    # parser_weigh.add_argument('-m', '--model', required=True,
    #                           help='absolute path to .npz matrix '
    #                           'corresponding to the distributional '
    #                           'space to weigh')
    # parser_weigh.add_argument('-o', '--output',
    #                           help='absolute path to output directory. '
    #                           'If not set, will default to model dir')
    # parser_weigh.add_argument('-w', '--weighing-func', choices=['ppmi'],
    #                           help='weighing function')
    # parser_remove = subparsers.add_parser(
    #     'remove', formatter_class=argparse.RawTextHelpFormatter,
    #     help='remove the mean vector')
    # parser_remove.set_defaults(func=_remove_mean)
    # parser_remove.add_argument('-m', '--model', required=True,
    #                            help='absolute path to .npy matrix')
    # parser_extract = subparsers.add_parser(
    #     'extract', formatter_class=argparse.RawTextHelpFormatter,
    #     help='extract top singular vector elements and associated statistics')
    # extract_sub = parser_extract.add_subparsers()
    # parser_extract_participants = extract_sub.add_parser(
    #     'top-participants', formatter_class=argparse.RawTextHelpFormatter,
    #     help='extract top participants for each singular vector')
    # parser_extract_participants.set_defaults(func=_extract_top_participants)
    # parser_extract_participants.add_argument('-m', '--model', required=True,
    #                                          help='absolute path to singular '
    #                                          'vectors file')
    # parser_extract_participants.add_argument(
    #     '-v', '--vocab', required=True, help='absolute path to .vocab file')
    # parser_extract_participants.add_argument(
    #     '-o', '--output', help='absolute path to output directory. If not set '
    #     'will default to matrix dir')
    # parser_extract_participants.add_argument(
    #     '-n', '--num-top-elements', default='20', type=int,
    #     help='number of elements to output. Default is 20')
    # parser_extract_participants.add_argument(
    #     '-c', '--confusion-matrix', action='store_true',
    #     help='If set, outputs confusion matrix')
    # parser_visualizer = subparsers.add_parser(
    #     'visualize', formatter_class=argparse.RawTextHelpFormatter,
    #     help='produce graphic visualization of results')
    # visualizer_sub = parser_visualizer.add_subparsers()
    # parser_visualize_heatmap = visualizer_sub.add_parser(
    #     'heatmap', formatter_class=argparse.RawTextHelpFormatter,
    #     help='produce heatmap from matrix')
    # parser_visualize_heatmap.set_defaults(func=_visualize_heatmap)
    # parser_visualize_heatmap.add_argument('-i', '--input', required=True,
    #                                       help='absolute path to input file')
    # parser_visualize_heatmap.add_argument(
    #     '-o', '--output', help='absolute path to output directory. '
    #     'If not set, will default to input dir')
    # parser_visualize_heatmap.add_argument(
    #     '-f', '--filter', help='absolute path to file storing the required '
    #     'subset of the matrix')
    # parser_visualize_singvalues = visualizer_sub.add_parser(
    #     'singular-values', formatter_class=argparse.RawTextHelpFormatter,
    #     help='visualize singular values distribution')
    # parser_visualize_singvalues.set_defaults(func=_visualize_singvalues)
    # parser_visualize_singvalues.add_argument(
    #     '-i', '--input', required=True,
    #     help='absolute path to .singvalues.npy file.')
    # parser_visualize_singvalues.add_argument(
    #     '-o', '--output', help='absolute path to output directory. '
    #     'If not set, will default to input dir')
    # parser_visualize_singvalues.add_argument(
    #     '-f', '--filter', help='absolute filepath to required subset')
    # parser_visualize_ipr = visualizer_sub.add_parser(
    #     'ipr-scatter', formatter_class=argparse.RawTextHelpFormatter,
    #     help='visualize singular values distribution')
    # parser_visualize_ipr.set_defaults(func=_visualize_ipr_scatter)
    # parser_visualize_ipr.add_argument(
    #     '-i', '--input', required=True,
    #     help='absolute path to .singvectors.ipr file.')
    # parser_visualize_ipr.add_argument(
    #     '-o', '--output', help='absolute path to output directory. '
    #     'If not set, will default to input dir')
    # parser_visualize_ipr.add_argument(
    #     '-f', '--filter', help='absolute filepath to required subset')
    # parser_visualize_boxplots = visualizer_sub.add_parser(
    #     'dim-boxplot', formatter_class=argparse.RawTextHelpFormatter,
    #     help='visualize boxplot from list of dimension files')
    # parser_visualize_boxplots.set_defaults(func=_visualize_boxplots)
    # parser_visualize_boxplots.add_argument(
    #     '-o', '--output', help='absolute path to output directory. '
    #     'If not set, will default to input dir')
    # parser_visualize_boxplots.add_argument(
    #     '-d', '--num-dimensions', required=True, type=int,
    #     help='number of dimensions of the model')
    # parser_visualize_boxplots.add_argument(
    #     '-i', '--input', nargs='+', help='list of files')
    args = parser.parse_args()
    args.func(args)
