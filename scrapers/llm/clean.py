"""Drop the empty top-level command emitted for the argparse root parser.

carapace-spec-argparse adds a ``- name: ""`` entry to the command list even
though the root flags are already lifted to the top-level spec. Keeping it
produces a phantom subcommand during code generation, so the entry is removed
from the generated YAML.
"""

import sys

SKIP_START = '    - name: ""'


def main():
    lines = sys.stdin.read().split('\n')
    out = []
    skipping = False

    for line in lines:
        if line == SKIP_START:
            skipping = True
            continue

        if skipping:
            if line.startswith('    - name: ') or (line and not line.startswith(' ')):
                skipping = False
            else:
                continue

        out.append(line)

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()
