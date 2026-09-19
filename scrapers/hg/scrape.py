"""Scrape mercurial (hg) for carapace-spec generation.

Mercurial uses its own command table (mercurial.commands.table) and
option format (fancyopts tuples), not argparse. This script introspects
the live command table and global option list and builds the flat JSON
schema expected by carapace-spec-argparse.
"""

import json
import sys

from mercurial import commands, debugcommands


def _decode(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value


def _opt_to_argument(opt):
    """Convert a fancyopts tuple to a carapace-spec-argparse argument.

    Tuple layout: (shortopts, longopts, default, description[, metavar]).
    A default of None or a bool marks a boolean flag; a list default marks
    a repeatable option; bytes/int defaults take a single value.
    """
    short = _decode(opt[0])
    long = _decode(opt[1])
    default = opt[2]
    help = _decode(opt[3])
    metavar = _decode(opt[4]) if len(opt) > 4 else None

    options = []
    if long:
        options.append(f"--{long}")
    if short:
        options.append(f"-{short}")

    if isinstance(default, bool) or default is None:
        is_bool = True
        type_name = "bool"
    else:
        is_bool = False
        if isinstance(default, bytes):
            type_name = "string"
        elif isinstance(default, int):
            type_name = "int"
        else:
            type_name = "string"

    serialized_default = None
    if isinstance(default, bytes):
        serialized_default = _decode(default)
    elif isinstance(default, (int, bool)) and not isinstance(default, bool):
        serialized_default = default
    elif isinstance(default, bool):
        serialized_default = default

    return {
        "name": long.replace("-", "_"),
        "options": options,
        "help": help,
        "required": False,
        "choices": None,
        "type": type_name,
        "nargs": "+" if isinstance(default, list) else None,
        "default": serialized_default,
        "metavar": metavar,
        "is_bool": is_bool,
    }


def _opts_to_arguments(opts):
    return [_opt_to_argument(o) for o in opts]


def _command_description(func, synopsis):
    doc = (func.__doc__ or "").strip()
    first_line = doc.splitlines()[0] if doc else ""
    syn = _decode(synopsis) if synopsis else ""
    if syn and not syn.startswith("["):
        return syn
    return first_line or syn


def main():
    result = {
        "cli": {"name": "hg", "version": ""},
        "commands": {
            "": {
                "description": "Mercurial distributed SCM",
                "arguments": _opts_to_arguments(commands.globalopts),
                "group": "",
            }
        },
        "groups": {},
    }

    for name, entry in sorted(commands.table.items()):
        primary = _decode(name).split("|")[0]
        func, opts = entry[0], entry[1]
        synopsis = entry[2] if len(entry) > 2 else None
        result["commands"][primary] = {
            "description": _command_description(func, synopsis),
            "arguments": _opts_to_arguments(opts),
            "group": "",
        }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
