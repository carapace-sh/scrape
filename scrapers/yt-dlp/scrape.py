"""Scrape yt-dlp (optparse-based) for carapace-spec generation."""
import json
import os
import sys


def _parse_option(option):
    """Convert an optparse.Option to the carapace-spec-argparse Argument format."""
    options = option._short_opts + option._long_opts

    is_bool = option.action in ('store_true', 'store_false', 'store_const', 'count')

    opt_type = option.type
    if opt_type is None:
        opt_type = 'string' if not is_bool else None

    choices = None
    if opt_type == 'choice' and option.choices:
        choices = list(option.choices)

    nargs = None
    if option.nargs and option.nargs > 1:
        nargs = str(option.nargs)

    return {
        "name": option.dest,
        "options": options,
        "help": option.help or "",
        "required": False,
        "choices": choices,
        "type": opt_type,
        "nargs": nargs,
        "default": list(option.default) if isinstance(option.default, set) else option.default,
        "metavar": option.metavar,
        "is_bool": is_bool,
    }


def main():
    version = os.environ.get('VERSION', '')
    cli_name = os.environ.get('CLI_NAME', 'yt-dlp')

    from yt_dlp.options import create_parser
    parser = create_parser()

    arguments = []

    for option in parser.option_list:
        if option.action in ('help', 'version'):
            continue
        arguments.append(_parse_option(option))

    for group in parser.option_groups:
        for option in group.option_list:
            if option.action in ('help', 'version'):
                continue
            arguments.append(_parse_option(option))

    result = {
        "cli": {"name": cli_name, "version": version},
        "commands": {
            "": {
                "description": "A feature-rich command-line audio/video downloader",
                "arguments": arguments,
                "group": "",
            }
        },
        "groups": {},
    }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())