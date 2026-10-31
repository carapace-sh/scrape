FROM golang:1.24 AS converter
RUN GOBIN=/usr/bin go install github.com/carapace-sh/carapace-spec-argparse/cmd/carapace-spec-argparse@latest

FROM python:3.12-slim
ARG VERSION

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /src
RUN git clone https://github.com/pre-commit/pre-commit --branch "${VERSION}" --depth 1
RUN pip install --no-cache-dir /src/pre-commit

COPY --from=converter /usr/bin/carapace-spec-argparse /usr/bin/carapace-spec-argparse
ADD scrape.py /scrape.py
ADD clean.py /clean.py

ENV VERSION=${VERSION}

RUN printf '#!/bin/sh\nset -e\npython /scrape.py > /tmp/pre-commit.json\ncarapace-spec-argparse --stdout /tmp/pre-commit.json | python /clean.py\n' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
