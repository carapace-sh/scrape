"""Scrape black (click-based) for carapace-spec generation."""
import json
import os
import sys

import click


def _get_choices(param_type):
    """Extract choices from a click type if it has them."""
    if hasattr(param_type, 'choices') and param_type.choices:
        return [str(c) for c in param_type.choices]
    return None


def _get_type_name(param_type):
    """Get a string name for a click type."""
    if param_type is None:
        return None
    if isinstance(param_type, click.Choice):
        return 'choice'
    if isinstance(param_type, click.types.IntParamType):
        return 'int'
    if isinstance(param_type, click.types.FloatParamType):
        return 'float'
    if isinstance(param_type, click.Path):
        return 'path'
    if isinstance(param_type, click.types.BoolParamType):
        return 'bool'
    if hasattr(param_type, 'name'):
        return param_type.name
    return type(param_type).__name__.lower()


def _serialize_default(default):
    """Serialize a default value to JSON-safe types."""
    if default is None:
        return None
    if isinstance(default, (str, int, float, bool)):
        return default
    try:
        return str(default) if default is not None else None
    except (TypeError, ValueError):
        return None


def _parse_option(param):
    """Convert a click.Option to the carapace-spec-argparse Argument format."""
    options = list(param.opts)
    if param.secondary_opts:
        options.extend(param.secondary_opts)

    is_bool = param.is_flag or param.count

    nargs = None
    if param.multiple:
        nargs = '+'

    return {
        "name": param.name,
        "options": options if options else [],
        "help": param.help or "",
        "required": param.required,
        "choices": _get_choices(param.type),
        "type": _get_type_name(param.type),
        "nargs": nargs,
        "default": _serialize_default(param.default),
        "metavar": param.metavar if isinstance(param.metavar, str) else None,
        "is_bool": is_bool,
    }


def _parse_argument(param):
    """Convert a click.Argument to the carapace-spec-argparse Argument format."""
    nargs = None
    if param.nargs != 1:
        if param.nargs == -1:
            nargs = '*'
        else:
            nargs = str(param.nargs)

    return {
        "name": param.name,
        "options": [],
        "help": "",
        "required": param.required,
        "choices": _get_choices(param.type),
        "type": _get_type_name(param.type),
        "nargs": nargs,
        "default": _serialize_default(param.default),
        "metavar": param.metavar if isinstance(param.metavar, str) else param.name.upper(),
        "is_bool": False,
    }


def main():
    version = os.environ.get('VERSION', '')
    cli_name = os.environ.get('CLI_NAME', 'black')

    from black import main as black_main

    cmd = black_main

    arguments = []
    for param in cmd.params:
        if isinstance(param, click.Option):
            if any(opt in ('--help', '-h') for opt in param.opts):
                continue
            arguments.append(_parse_option(param))
        elif isinstance(param, click.Argument):
            arguments.append(_parse_argument(param))

    result = {
        "cli": {"name": cli_name, "version": version},
        "commands": {
            "": {
                "description": cmd.help or "",
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