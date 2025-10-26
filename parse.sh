#!/bin/sh
echo 'services:'
grep '#' package.json | sed 's/^ \+"\([^:]\+\)": "[^#]\+#\([^"]\+\).*/  \1: { build: {context: \1, args: {VERSION: \2}}}/'
