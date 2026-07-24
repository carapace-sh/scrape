"""Scrape openstackclient (cliff-based) for carapace-spec generation.

Cliff does not use argparse subparsers: it keeps a flat dict of command
name -> entry point and builds a fresh ArgumentParser per command. This
script builds the flat JSON schema expected by carapace-spec-argparse by
iterating every loaded command and walking its per-command parser.
"""

import argparse
import importlib
import importlib.metadata
import inspect
import json
import sys
from typing import Any, Dict, List, Optional


def _type_name(type_callable) -> Optional[str]:
    if type_callable is None:
        return None
    name = getattr(type_callable, "__name__", None)
    if name:
        return name
    return str(type_callable)


def _nargs_value(nargs) -> Optional[str]:
    if nargs is None:
        return None
    if isinstance(nargs, int):
        return str(nargs)
    return str(nargs)


def _is_bool_action(action) -> bool:
    if hasattr(argparse, "BooleanOptionalAction") and isinstance(
        action, argparse.BooleanOptionalAction
    ):
        return True
    if isinstance(
        action,
        (argparse._StoreTrueAction, argparse._StoreFalseAction, argparse._StoreConstAction),
    ):
        return True
    if isinstance(action, argparse._CountAction):
        return True
    return False


def _serialize_default(default) -> Optional[Any]:
    if default is None:
        return None
    if isinstance(default, (str, int, float, bool)):
        return default
    return str(default)


def _action_to_argument(action) -> Dict[str, Any]:
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


def _filter_help_flags(flags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        f for f in flags if not any(opt in ("--help", "-h") for opt in f.get("options", []))
    ]


def _parser_flags(parser) -> List[Dict[str, Any]]:
    flags: List[Dict[str, Any]] = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            continue
        if action.option_strings:
            flags.append(_action_to_argument(action))
    return _filter_help_flags(flags)


def _build_global_flags(app) -> List[Dict[str, Any]]:
    return _parser_flags(app.parser)


def _instantiate_command(app, cmd_name, cmd_class):
    kwargs: Dict[str, Any] = {}
    try:
        spec = inspect.getfullargspec(cmd_class.__init__)
        if "cmd_name" in spec.args:
            kwargs["cmd_name"] = cmd_name
    except TypeError:
        pass
    try:
        return cmd_class(app, app.options, **kwargs)
    except TypeError:
        try:
            return cmd_class(app, app.options)
        except TypeError:
            return cmd_class(app, None, **kwargs)


def _command_parser(app, cmd_name, cmd_class):
    cmd = _instantiate_command(app, cmd_name, cmd_class)
    full_name = f"{app.NAME} {cmd_name}"
    return cmd.get_parser(full_name), cmd


def _walk_command_parser(parser) -> Dict[str, Any]:
    flags: List[Dict[str, Any]] = []
    commands: Dict[str, Dict[str, Any]] = {}

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


def _discover_openstack_groups() -> List[str]:
    """Discover all entry point groups starting with 'openstack.'."""
    groups: set = set()
    for ep in importlib.metadata.entry_points():
        if ep.group.startswith("openstack."):
            groups.add(ep.group)
    return sorted(groups)


def main() -> int:
    arg_parser = argparse.ArgumentParser(
        description="Scrape openstackclient for carapace-spec generation."
    )
    arg_parser.add_argument("--cli", default="openstack", help="CLI name")
    arg_parser.add_argument("--version", default="", help="CLI version override")
    arg_parser.add_argument(
        "--import",
        dest="import_spec",
        default="openstackclient.shell:OpenStackShell",
        help="module:Class to import (default: openstackclient.shell:OpenStackShell)",
    )
    args = arg_parser.parse_args()

    module_path, class_name = args.import_spec.rsplit(":", 1)
    module = importlib.import_module(module_path)
    shell_class = getattr(module, class_name)

    app = shell_class()

    # Parse a minimal argv so self.options exists (needed by commands that
    # reference app.options in get_parser).
    app.options, _ = app.parser.parse_known_args(["--help"])

    # The CommandManager in __init__ already loaded the 'openstack.cli' group.
    # The remaining command groups (openstack.common, openstack.<service>.vN,
    # openstack.extension) are normally loaded by _load_plugins/_load_commands,
    # which require cloud config / auth setup. Instead, discover all
    # openstack.* entry point groups directly and load them — no auth needed.
    for group in _discover_openstack_groups():
        try:
            app.command_manager.add_command_group(group)
        except Exception as e:  # noqa: BLE001
            print(f"warning: failed to load command group {group}: {e}", file=sys.stderr)

    cli_name = args.cli
    version = args.version
    if not version:
        version = getattr(module, "__version__", "") or ""

    commands: Dict[str, Dict[str, Any]] = {}
    groups: Dict[str, Dict[str, Any]] = {}

    # Global flags are attached to the root command (key "").
    global_flags = _build_global_flags(app)
    commands[""] = {
        "description": "",
        "arguments": global_flags,
        "group": "",
    }

    command_manager = app.command_manager
    cmd_names = sorted(command_manager.commands.keys())

    failures: List[str] = []
    for cmd_name in cmd_names:
        ep = command_manager.commands[cmd_name]
        try:
            cmd_class = ep.load()
        except Exception as e:  # noqa: BLE001
            failures.append(f"{cmd_name}: load() failed: {e}")
            continue

        try:
            parser, _cmd = _command_parser(app, cmd_name, cmd_class)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{cmd_name}: get_parser failed: {e}")
            continue

        tree = _walk_command_parser(parser)
        if tree["commands"]:
            _flatten({"commands": {cmd_name: tree}}, "", commands, groups)
        else:
            commands[cmd_name] = {
                "description": tree["description"],
                "arguments": tree["flags"],
                "group": cmd_name.split()[0] if " " in cmd_name else "",
            }

    _ensure_groups_for_commands(commands, groups)

    for fail in failures:
        print(f"warning: skipped {fail}", file=sys.stderr)

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
