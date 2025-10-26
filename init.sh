#!/bin/bash
set -e
set -o pipefail
cd $(dirname "$(readlink -f "$0")")

lines=$(grep "^    .*#.*" package.json | sed 's/^ \+"\([^:]\+\)": "[^#]\+#\([^"]\+\).*/\1 \2/')
mapfile -t lines <<< "${lines}"

(
  echo 'services:'
  for line in "${lines[@]}"; do
    read command version <<< "$line"
    echo "  ${command}: { build: {context: scrapers\/\1, args: {VERSION: ${version}}}}"
  done
) > compose.yaml

(
  echo "name: scrape"
  echo ""
  echo "on:"
  echo "  pull_request:"
  echo "  push:"
  echo ""
  echo "jobs:"
  for line in "${lines[@]}"; do
    read command version <<< "$line"
    echo "  ${command}: {uses: ./.github/workflows/scrape-template.yml, with: {command: ${command}}}"
  done
) > ./.github/workflows/scrape.yml
