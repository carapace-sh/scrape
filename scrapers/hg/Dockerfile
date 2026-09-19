FROM golang:1.24 AS converter
RUN GOBIN=/usr/bin go install github.com/carapace-sh/carapace-spec-argparse/cmd/carapace-spec-argparse@latest

FROM python:3.12-slim
ARG VERSION

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*

# Mercurial has no Git mirror: fetch the official release tarball instead.
RUN python -c "import urllib.request; urllib.request.urlretrieve('https://www.mercurial-scm.org/release/mercurial-${VERSION}.tar.gz', '/tmp/hg.tar.gz')" \
  && mkdir -p /src && tar -xzf /tmp/hg.tar.gz -C /src
RUN pip install --no-cache-dir /src/mercurial-${VERSION}

COPY --from=converter /usr/bin/carapace-spec-argparse /usr/bin/carapace-spec-argparse
ADD scrape.py /scrape.py

# Produce JSON from the live command table, then emit carapace-spec YAML on
# stdout (the workflow captures stdout).
RUN printf '#!/bin/sh\nset -e\npython /scrape.py > /tmp/hg.json\ncarapace-spec-argparse --stdout /tmp/hg.json\n' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
