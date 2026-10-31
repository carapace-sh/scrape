"""Scrape pre-commit's argparse tree for carapace-spec generation.

pre-commit builds its parser inside ``main()`` and does not expose a parser
factory, so the parser is captured by intercepting ``argparse.ArgumentParser``
construction while ``main()`` runs. Parsing is aborted as soon as the tree is
complete.
"""

import argparse
import json
import os
import sys

import pre_commit.constants
from pre_commit import main as pre_commit_main


class _Captured(Exception):
    pass


def _capture_parser():
    parser = None
    original_init = argparse.ArgumentParser.__init__
    original_parse = argparse.ArgumentParser.parse_args

    def init(self, *args, **kwargs):
        nonlocal parser
        if parser is None:
            parser = self
        original_init(self, *args, **kwargs)

    def parse_args(self, *args, **kwargs):
        raise _Captured

    argparse.ArgumentParser.__init__ = init
    argparse.ArgumentParser.parse_args = parse_args
    try:
        pre_commit_main.main(())
    except _Captured:
        pass
    finally:
        argparse.ArgumentParser.__init__ = original_init
        argparse.ArgumentParser.parse_args = original_parse

    if parser is None:
        raise RuntimeError('pre-commit parser was not constructed')
    return parser


def _is_bool(action):
    return isinstance(
        action,
        (
            argparse._StoreTrueAction,
            argparse._StoreFalseAction,
            argparse._StoreConstAction,
            argparse._CountAction,
        ),
    )


def _argument(action):
    return {
        'name': action.dest,
        'options': list(action.option_strings),
        'help': action.help or '',
        'required': bool(action.required),
        'choices': [str(c) for c in action.choices] if action.choices else None,
        'type': getattr(action.type, '__name__', None),
        'nargs': str(action.nargs) if action.nargs is not None else None,
        'default': action.default if isinstance(action.default, (str, int, float, bool)) else None,
        'metavar': action.metavar if isinstance(action.metavar, str) else None,
        'is_bool': _is_bool(action),
    }


def _walk(parser):
    flags = []
    commands = {}

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            help_lookup = {choice.dest: choice.help or '' for choice in action._choices_actions}
            for name, subparser in action.choices.items():
                result = _walk(subparser)
                result['help'] = help_lookup.get(name, '')
                commands[name] = result
        elif action.option_strings:
            if any(opt in ('-h', '--help') for opt in action.option_strings):
                continue
            flags.append(_argument(action))

    return {
        'flags': flags,
        'commands': commands,
        'description': parser.description or '',
    }


def _flatten(node, prefix, commands, groups):
    for name, sub in node.get('commands', {}).items():
        full_name = f'{prefix} {name}'.strip()

        if sub.get('commands'):
            groups.setdefault(full_name, {'help': sub.get('help', ''), 'groups': {}})
            if prefix:
                groups.setdefault(prefix, {'help': '', 'groups': {}})
                groups[prefix]['groups'][full_name] = {'help': sub.get('help', '')}
            _flatten(sub, full_name, commands, groups)
        else:
            commands[full_name] = {
                'description': sub.get('help', '') or sub.get('description', ''),
                'arguments': sub.get('flags', []),
                'group': prefix.split()[0] if prefix else '',
            }

    if prefix in commands:
        if node.get('flags'):
            commands[prefix]['arguments'] = node.get('flags', [])
    elif node.get('flags') or node.get('description'):
        commands[prefix] = {
            'description': node.get('description', ''),
            'arguments': node.get('flags', []),
            'group': prefix.split()[0] if ' ' in prefix else '',
        }


def main():
    tree = _walk(_capture_parser())
    commands = {}
    groups = {}
    _flatten(tree, '', commands, groups)

    result = {
        'cli': {
            'name': 'pre-commit',
            'version': os.environ.get('VERSION', pre_commit.constants.VERSION),
        },
        'commands': commands,
        'groups': groups,
    }

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
