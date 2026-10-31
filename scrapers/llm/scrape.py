"""Scrape llm's click command tree for carapace-spec generation."""

import json
import os
import sys

import click

from llm.cli import cli


def _choices(param):
    if isinstance(param.type, click.Choice):
        return [str(choice) for choice in param.type.choices]
    return None


def _type_name(param):
    typ = param.type
    if isinstance(typ, click.Choice):
        return 'choice'
    if isinstance(typ, click.types.IntParamType):
        return 'int'
    if isinstance(typ, click.types.FloatParamType):
        return 'float'
    if isinstance(typ, click.Path):
        return 'path'
    if isinstance(typ, click.types.BoolParamType):
        return 'bool'
    return getattr(typ, 'name', None) or type(typ).__name__.lower()


def _option(param):
    return {
        'name': param.name,
        'options': list(param.opts) + list(param.secondary_opts),
        'help': param.help or '',
        'required': bool(getattr(param, 'required', False)),
        'choices': _choices(param),
        'type': _type_name(param),
        'nargs': '+' if getattr(param, 'multiple', False) else None,
        'default': param.default if isinstance(param.default, (str, int, float, bool)) else None,
        'metavar': param.metavar if isinstance(param.metavar, str) else None,
        'is_bool': bool(getattr(param, 'is_flag', False) or getattr(param, 'count', False)),
    }


def _argument(param):
    nargs = None
    if param.nargs == -1:
        nargs = -1
    elif param.nargs != 1:
        nargs = str(param.nargs)

    return {
        'name': param.name,
        'options': [],
        'help': '',
        'required': bool(param.required),
        'choices': _choices(param),
        'type': _type_name(param),
        'nargs': str(nargs) if nargs is not None else None,
        'default': None,
        'metavar': param.metavar if isinstance(param.metavar, str) else param.name.upper(),
        'is_bool': False,
    }


def _params(command):
    arguments = []
    for param in command.params:
        if isinstance(param, click.Option):
            if any(opt in ('-h', '--help') for opt in param.opts):
                continue
            arguments.append(_option(param))
        elif isinstance(param, click.Argument):
            arguments.append(_argument(param))
    return arguments


def walk(command, path, commands, groups, parent):
    help_text = (command.help or '').strip().split('\n')[0]
    params = _params(command)

    if isinstance(command, click.Group):
        if path:
            groups.setdefault(path, {'help': help_text, 'groups': {}})
            groups[path]['help'] = help_text
            if parent:
                groups.setdefault(parent, {'help': '', 'groups': {}})
                groups[parent]['groups'][path] = {'help': help_text}
        if params or (not path):
            commands[path] = {
                'description': help_text,
                'arguments': params,
                'group': '',
            }
        for name, sub in command.commands.items():
            walk(sub, f'{path} {name}'.strip(), commands, groups, path)
    else:
        commands[path] = {
            'description': help_text,
            'arguments': params,
            'group': parent,
        }


def main():
    commands = {}
    groups = {}
    walk(cli, '', commands, groups, '')

    result = {
        'cli': {
            'name': 'llm',
            'version': os.environ.get('VERSION', ''),
        },
        'commands': commands,
        'groups': groups,
    }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
