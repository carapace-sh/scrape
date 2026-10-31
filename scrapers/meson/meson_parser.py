"""Expose meson's argparse tree as a parser factory.

meson builds its command line parser in ``CommandLineParser`` and does not
expose it as a module level function, so the instance is unwrapped here.
"""

from mesonbuild.mesonmain import CommandLineParser


def get_parser():
    return CommandLineParser().parser
