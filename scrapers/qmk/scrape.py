"""Scrape qmk_cli (milc/argparse-based) for carapace-spec generation.

Milc is built on top of argparse. Subcommands are registered via
@cli.subcommand() decorators which add argparse subparsers at import time.
"""
import argparse
import json
import os
import sys
import warnings


def _type_name(type_callable):
    if type_callable is None:
        return None
    name = getattr(type_callable, "__name__", None)
    if name:
        return name
    return str(type_callable)


def _nargs_value(nargs):
    if nargs is None:
        return None
    if isinstance(nargs, int):
        return str(nargs)
    return str(nargs)


def _is_bool_action(action):
    if hasattr(action, "option_strings") and not action.option_strings:
        return False
    if isinstance(
        action,
        (type(True).__class__('_StoreTrueAction', (object,), {}),
         type(True).__class__('_StoreFalseAction', (object,), {}),
         type(True).__class__('_StoreConstAction', (object,), {})),
    ):
        return True
    import argparse
    if isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction, argparse._StoreConstAction)):
        return True
    if isinstance(action, argparse._CountAction):
        return True
    return False


def _serialize_default(default):
    if default is None:
        return None
    if isinstance(default, (str, int, float, bool)):
        return default
    return str(default)


def _action_to_argument(action):
    choices = None
    if action.choices is not None:
        try:
            choices = [str(c) for c in action.choices]
        except TypeError:
            choices = None

    return {
        "name": action.dest,
        "options": list(action.option_strings),
        "help": action.help or "",
        "required": bool(action.required),
        "choices": choices,
        "type": _type_name(action.type),
        "nargs": _nargs_value(action.nargs),
        "default": _serialize_default(action.default),
        "metavar": action.metavar if isinstance(action.metavar, str) else None,
        "is_bool": _is_bool_action(action),
    }


def _filter_help_flags(flags):
    return [
        f for f in flags if not any(opt in ("--help", "-h") for opt in f.get("options", []))
    ]


def _parser_flags(parser):
    flags = []
    import argparse
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            continue
        if action.option_strings:
            flags.append(_action_to_argument(action))
    return _filter_help_flags(flags)


def _build_global_flags(parser):
    return _parser_flags(parser)


def _walk_command_parser(parser):
    flags = []
    commands = {}
    import argparse
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for choice_name in action.choices:
                subparser = action.choices[choice_name]
                sub = _walk_command_parser(subparser)
                commands[choice_name] = sub
        elif action.option_strings:
            flags.append(_action_to_argument(action))
    return {
        "flags": _filter_help_flags(flags),
        "commands": commands,
        "description": parser.description or "",
    }


def _flatten(node, prefix, commands, groups):
    for name, sub in node.get("commands", {}).items():
        full_name = f"{prefix} {name}".strip()
        sub_commands = sub.get("commands", {})

        if sub_commands:
            group_entry = groups.setdefault(
                full_name, {"help": sub.get("help", sub.get("description", "")), "groups": {}}
            )
            if prefix:
                parent_group = groups.setdefault(prefix, {"help": "", "groups": {}})
                parent_group["groups"][full_name] = {"help": sub.get("help", sub.get("description", ""))}

            _flatten(sub, full_name, commands, groups)

            if sub.get("flags"):
                commands[full_name] = {
                    "description": sub.get("help", sub.get("description", "")),
                    "arguments": sub.get("flags", []),
                    "group": prefix.split()[0] if prefix else "",
                }
        else:
            commands[full_name] = {
                "description": sub.get("help", sub.get("description", "")),
                "arguments": sub.get("flags", []),
                "group": prefix.split()[0] if prefix else "",
            }


def _ensure_groups_for_commands(commands, groups):
    for name in commands:
        parts = name.split()
        if len(parts) <= 1:
            continue
        top = parts[0]
        if top not in groups:
            groups[top] = {"help": "", "groups": {}}


def main():
    version = os.environ.get('VERSION', '')
    cli_name = os.environ.get('CLI_NAME', 'qmk')

    # Suppress warnings from qmk import
    warnings.filterwarnings("ignore")

    # Set up environment for qmk_firmware
    qmk_home = os.environ.get('QMK_HOME', '/qmk_firmware')
    if os.path.isdir(os.path.join(qmk_home, 'lib/python')):
        sys.path.insert(0, os.path.join(qmk_home, 'lib/python'))

    # Import milc and qmk_cli - this triggers module-level setup
    import milc
    import qmk_cli

    # Import core subcommands
    import qmk_cli.subcommands  # noqa: F401

    # Try to import firmware subcommands
    try:
        import qmk.cli  # noqa: F401
    except Exception:
        pass

    # Get the milc CLI's argparse parser
    # First call milc.cli() to initialize the parser
    try:
        milc.cli()
    except SystemExit:
        pass
    parser = milc.cli._milc._arg_parser

    commands = {}
    groups = {}

    tree = _walk_command_parser(parser)
    if tree["commands"]:
        _flatten({"commands": tree["commands"]}, "", commands, groups)

    _ensure_groups_for_commands(commands, groups)

    result = {
        "cli": {"name": cli_name, "version": version},
        "commands": commands,
        "groups": groups,
    }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())