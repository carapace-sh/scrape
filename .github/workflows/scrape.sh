#!/bin/bash
set -e
set -o pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: scrape.sh COMMAND" >/dev/stderr
  exit 1
fi

lines=$(grep "^    \"$1\":.*#.*" package.json | sed 's/^ \+"\([^:]\+\)": "[^#]\+#\([^"]\+\).*/\1 \2/')
mapfile -t lines <<< "${lines}"

for line in "${lines[@]}"; do
  read command version <<< "$line"
  if [ ! -f "gh-pages/${command}/${version}.yaml" ]; then
    docker compose build "${command}"
    out="$(docker compose run --quiet --remove-orphans "${command}")"
    mkdir -p "gh-pages/${command}/"
    echo "${out}" > "gh-pages/${command}/${version}.yaml"
  else
    echo "gh-pages/${command}/${version}.yaml already exists" >/dev/stderr
  fi
done
