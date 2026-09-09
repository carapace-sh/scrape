"""Scrape eopkg (optparse-based) for carapace-spec generation.

eopkg keeps a flat registry of command classes (pisi.cli.command.Command,
populated by the `autocommand` metaclass when the command modules are
imported). Each command class builds its own optparse.OptionParser via
`setup_options()` plus shared options from `commonopts()`. This script
instantiates each parser without running the command and emits the flat
JSON schema expected by carapace-spec-argparse.
"""
import json
import os
import sys

import optparse


def _serialize_default(default):
    if default is None:
        return None
    if isinstance(default, (str, int, float, bool)):
        return default
    return str(default)


def _parse_option(option):
    options = option._short_opts + option._long_opts

    is_bool = option.action in ("store_true", "store_false", "store_const", "count")

    opt_type = option.type
    if opt_type is None:
        opt_type = "string" if not is_bool else None

    choices = None
    if opt_type == "choice" and option.choices:
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
        "default": _serialize_default(option.default),
        "metavar": option.metavar,
        "is_bool": is_bool,
    }


def _parser_options(parser):
    arguments = []
    for option in parser.option_list:
        if option.action in ("help", "version") or option.help == optparse.SUPPRESS_HELP:
            continue
        arguments.append(_parse_option(option))
    for group in parser.option_groups:
        for option in group.option_list:
            if option.action in ("help", "version") or option.help == optparse.SUPPRESS_HELP:
                continue
            arguments.append(_parse_option(option))
    return arguments


def _command_parser(cls):
    """Build the option parser of a command class without running it."""
    instance = cls.__new__(cls)
    instance.parser = optparse.OptionParser(usage=cls.__doc__ or "", version="eopkg")
    try:
        instance.setup_options()
    except Exception as e:
        sys.stderr.write("warning: setup_options failed for %s: %s\n" % (cls.__name__, e))
    instance.commonopts()
    return instance.parser


def _dedupe(arguments):
    seen = set()
    result = []
    for arg in arguments:
        key = tuple(sorted(arg["options"]))
        if key in seen:
            continue
        seen.add(key)
        result.append(arg)
    return result


def main():
    version = os.environ.get("VERSION", "")
    cli_name = os.environ.get("CLI_NAME", "eopkg")

    import pisi.cli.pisicli  # noqa: F401 - imports and registers all commands
    import pisi.cli.command as command

    classes = {}
    for name, cls in command.Command.cmd_dict.items():
        classes.setdefault(cls, []).append(name)

    commands = {
        "": {
            "description": "eopkg is the package management system of Solus Operating System",
            "arguments": [],
            "group": "",
        }
    }

    for cls, names in classes.items():
        try:
            parser = _command_parser(cls)
            arguments = _dedupe(_parser_options(parser))
        except Exception as e:
            sys.stderr.write("warning: failed to scrape %s: %s\n" % (cls.__name__, e))
            continue

        description = " ".join((cls.__doc__ or "").split())
        for name in names:
            commands[name] = {
                "description": description,
                "arguments": arguments,
                "group": "",
            }

    result = {
        "cli": {"name": cli_name, "version": version},
        "commands": commands,
        "groups": {},
    }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
