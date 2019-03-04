"""Argument parsing utils."""

import os
import logging
import argparse

logger = logging.getLogger(__name__)

__all__ = ()


def dir(arg):
    if os.path.isdir(arg):
        return arg
    raise argparse.ArgumentTypeError('{} is not a directory'.format(arg))


def npz(arg):
    if arg.endswith('.npy') or args.endswith('.npz'):
        return arg
    raise argparse.ArgumentTypeError('{} is not in npz or npy format'.format(arg))


def datasets(arg):
    if os.path.basename(arg) in ['mcrae.txt', 'pado.txt', 'ferretti-instruments.txt', 'ferretti-locations.txt']:
        return arg
    raise argparse.ArgumentTypeError('{} is not among supported datasets'.format(arg))
