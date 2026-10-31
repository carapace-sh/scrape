#!/usr/bin/env python3
"""Generic Python argparse spec scraper for carapace.

Walks argparse parser trees (or Knack command tables) and outputs a JSON
schema that the Go converter (carapace-spec-argparse) turns into
carapace-spec YAML.

Usage:
    # Generic argparse introspection
    python scrape.py --method argparse --cli mycli --import "mycli.parser:get_parser"

    # Knack command_table (az, sfctl)
    python scrape.py --method knack --cli az

    # Auto-detect (default)
    python scrape.py --cli az
"""

import argparse
import importlib
import json
import sys
from typing import Any, Dict, List, Optional


def _type_name(type_callable) -> Optional[str]:
    """Stringify an argparse type callable."""
    if type_callable is None:
        return None
    name = getattr(type_callable, "__name__", None)
    if name:
        return name
    return str(type_callable)


def _nargs_value(nargs) -> Optional[str]:
    """Normalize argparse nargs to a JSON-serializable value."""
    if nargs is None:
        return None
    return str(nargs)


def _is_bool_action(action) -> bool:
    """Check if an argparse action is a boolean flag (no value)."""
    # BooleanOptionalAction (Python 3.9+) produces --flag and --no-flag,
    # neither of which takes a value
    if hasattr(argparse, "BooleanOptionalAction") and isinstance(
        action, argparse.BooleanOptionalAction
    ):
        return True
    # store_true / store_false / store_const don't consume a value
    if isinstance(
        action,
        (argparse._StoreTrueAction, argparse._StoreFalseAction, argparse._StoreConstAction),
    ):
        return True
    if isinstance(action, argparse._CountAction):
        return True
    return False


def _action_to_argument(action) -> Dict[str, Any]:
    """Convert an argparse Action to the JSON argument schema."""
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


def _serialize_default(default) -> Optional[Any]:
    """Serialize a default value to JSON-compatible form."""
    if default is None:
        return None
    if isinstance(default, (str, int, float, bool)):
        return default
    return str(default)


def _filter_help_flags(flags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove --help/-h flags (carapace adds its own)."""
    return [
        f for f in flags if not any(opt in ("--help", "-h") for opt in f.get("options", []))
    ]


def _walk_parser(parser, path: str = "") -> Dict[str, Any]:
    """Recursively walk an argparse parser, returning the command tree.

    Returns a dict with:
        - flags: list of argument dicts
        - commands: dict of subcommand_name -> recursive result
        - description: parser description
    """
    flags: List[Dict[str, Any]] = []
    commands: Dict[str, Dict[str, Any]] = {}

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            help_lookup = {ca.dest: ca.help or "" for ca in action._choices_actions}
            for name, subparser in action.choices.items():
                sub_path = f"{path} {name}".strip()
                sub_result = _walk_parser(subparser, sub_path)
                sub_result["help"] = help_lookup.get(name, "")
                commands[name] = sub_result
        elif action.option_strings:
            flags.append(_action_to_argument(action))
        # Positional arguments (no option_strings) are skipped —
        # carapace-spec handles positional completion separately

    return {
        "flags": _filter_help_flags(flags),
        "commands": commands,
        "description": parser.description or "",
    }


def scrape_argparse(parser) -> Dict[str, Any]:
    """Scrape a raw argparse parser tree.

    Args:
        parser: An argparse.ArgumentParser (or subparser) instance.

    Returns:
        The JSON schema dict with cli, commands, and groups.
    """
    tree = _walk_parser(parser)
    commands: Dict[str, Dict[str, Any]] = {}
    groups: Dict[str, Dict[str, Any]] = {}

    _flatten_commands(tree, "", commands, groups)

    return {
        "cli": {"name": "", "version": ""},
        "commands": commands,
        "groups": groups,
    }


def _flatten_commands(
    node: Dict[str, Any],
    prefix: str,
    commands: Dict[str, Dict[str, Any]],
    groups: Dict[str, Dict[str, Any]],
):
    """Flatten the recursive parser tree into flat command dict + groups."""
    for name, sub in node.get("commands", {}).items():
        full_name = f"{prefix} {name}".strip()
        sub_commands = sub.get("commands", {})

        if sub_commands:
            group_entry = groups.setdefault(
                full_name, {"help": sub.get("help", ""), "groups": {}}
            )
            group_entry["help"] = sub.get("help", group_entry["help"])

            if prefix:
                parent_group = groups.setdefault(
                    prefix, {"help": "", "groups": {}}
                )
                parent_group["groups"][full_name] = {"help": sub.get("help", "")}

            _flatten_commands(sub, full_name, commands, groups)
        else:
            commands[full_name] = {
                "description": sub.get("help", sub.get("description", "")),
                "arguments": sub.get("flags", []),
                "group": prefix.split()[0] if prefix else "",
            }

    if node.get("flags") or (not prefix and node.get("description")):
        if prefix not in commands:
            commands[prefix] = {
                "description": node.get("help", node.get("description", "")),
                "arguments": node.get("flags", []),
                "group": prefix.split()[0] if " " in prefix else "",
            }
        elif node.get("flags"):
            commands[prefix]["arguments"] = node.get("flags", [])


def _get_parser_from_import(import_spec: str):
    """Import a module and retrieve the parser factory.

    import_spec format: "module.path:function_name" or "module.path"
    The function should return an argparse.ArgumentParser.
    """
    if ":" in import_spec:
        module_path, func_name = import_spec.rsplit(":", 1)
    else:
        module_path, func_name = import_spec, "get_parser"

    module = importlib.import_module(module_path)
    func = getattr(module, func_name)
    parser = func()
    if callable(parser):
        parser = parser()
    return parser


def scrape_knack(cli_name: str = "az") -> Dict[str, Any]:
    """Scrape a Knack-based CLI using the command_table API.

    Works with Azure CLI (az), Service Fabric CLI (sfctl), and other
    CLIs built on the Knack framework.
    """
    try:
        from azure.cli.core.file_util import (
            create_invoker_and_load_cmds_and_args,
        )

        cli_ctx = _create_az_cli_ctx(cli_name)
        create_invoker_and_load_cmds_and_args(cli_ctx)
        command_table = cli_ctx.invocation.commands_loader.command_table
        command_group_specs = cli_ctx.invocation.commands_loader.command_group_specs

        return _knack_to_json(cli_name, command_table, command_group_specs)
    except Exception as e:
        print(f"Error: knack scraping failed: {e}", file=sys.stderr)
        sys.exit(1)


def _create_az_cli_ctx(cli_name: str):
    """Create an Azure CLI context for command loading."""
    from knack.cli import CLI

    return CLI(cli_name=cli_name, config_dir="/tmp/.{}".format(cli_name))


def _knack_to_json(cli_name, command_table, command_group_specs) -> Dict[str, Any]:
    """Convert Knack command_table to the JSON schema."""
    commands: Dict[str, Dict[str, Any]] = {}
    groups: Dict[str, Dict[str, Any]] = {}

    for name, cmd in command_table.items():
        arguments = []
        for arg_name, arg in sorted(cmd.arguments.items()):
            arg_def = arg.type
            options = list(arg_def.options.get("options_list", []) or [])
            if not options:
                options = ["--{}".format(arg_name.replace("_", "-"))]

            choices = None
            if arg_def.choices:
                choices = list(arg_def.choices)

            arg_type = arg_def.type
            type_name = None
            if arg_type and hasattr(arg_type, "__name__"):
                type_name = arg_type.__name__
            elif arg_type:
                type_name = str(arg_type)

            nargs_val = None
            if arg_def.nargs:
                nargs_val = str(arg_def.nargs)

            arguments.append(
                {
                    "name": arg_name,
                    "options": options,
                    "help": arg_def.help or "",
                    "required": bool(arg_def.required),
                    "choices": choices,
                    "type": type_name,
                    "nargs": nargs_val,
                    "default": _serialize_default(arg_def.default),
                    "metavar": arg_def.metavar if isinstance(arg_def.metavar, str) else None,
                    "is_bool": False,
                }
            )

        arguments = _filter_help_flags(arguments)

        group_name = name.split()[0] if " " in name else ""
        commands[name] = {
            "description": cmd.description or "",
            "arguments": arguments,
            "group": group_name,
        }

    for group_name, group_spec in (command_group_specs or {}).items():
        groups[group_name] = {
            "help": getattr(group_spec, "description", "") or "",
            "groups": {},
        }

    return {
        "cli": {"name": cli_name, "version": _get_cli_version(cli_name)},
        "commands": commands,
        "groups": groups,
    }


def _get_cli_version(cli_name: str) -> str:
    """Try to get the CLI version."""
    try:
        if cli_name == "az":
            from azure.cli.core import get_default_cli

            cli = get_default_cli()
            return cli.version

        mod = importlib.import_module(cli_name)
        return getattr(mod, "__version__", "")
    except Exception:
        return ""


def auto_detect_method(import_spec: Optional[str]) -> str:
    """Auto-detect the scraping method based on available imports."""
    try:
        import knack  # noqa: F401

        return "knack"
    except ImportError:
        pass
    return "argparse"


def main():
    arg_parser = argparse.ArgumentParser(
        description="Scrape Python argparse CLIs for carapace-spec generation."
    )
    arg_parser.add_argument("--method", default="auto", help="Scraping method: auto, argparse, or knack")
    arg_parser.add_argument("--cli", default="", help="CLI name (e.g. az, mycli)")
    arg_parser.add_argument("--import", dest="import_spec", default=None, help="Module:function to import for argparse method (e.g. mycli.parser:get_parser)")
    arg_parser.add_argument("--version", default="", help="CLI version override")
    args = arg_parser.parse_args()

    method = args.method
    if method == "auto":
        method = auto_detect_method(args.import_spec)

    if method == "argparse":
        if not args.import_spec:
            print("Error: --import is required for argparse method", file=sys.stderr)
            sys.exit(1)
        parser = _get_parser_from_import(args.import_spec)
        result = scrape_argparse(parser)
        result["cli"]["name"] = args.cli or parser.prog
        if args.version:
            result["cli"]["version"] = args.version
    elif method == "knack":
        result = scrape_knack(args.cli)
        if args.version:
            result["cli"]["version"] = args.version
    else:
        print(f"Error: unknown method '{method}'", file=sys.stderr)
        sys.exit(1)

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
