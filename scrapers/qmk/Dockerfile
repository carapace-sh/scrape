FROM golang:1.24 AS converter
RUN GOBIN=/usr/bin go install github.com/carapace-sh/carapace-spec-argparse/cmd/carapace-spec-argparse@latest

FROM python:3.12-slim
ARG VERSION

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /src
RUN git clone https://github.com/qmk/qmk_cli --branch "${VERSION}" --depth 1
RUN pip install --no-cache-dir /src/qmk_cli

# Clone qmk_firmware for firmware subcommands
RUN git clone https://github.com/qmk/qmk_firmware --depth 1 /qmk_firmware

COPY --from=converter /usr/bin/carapace-spec-argparse /usr/bin/carapace-spec-argparse
ADD scrape.py /scrape.py

ENV VERSION=${VERSION}
ENV CLI_NAME=qmk
ENV QMK_HOME=/qmk_firmware
ENV ORIG_CWD=/src

RUN printf '#!/bin/sh\nset -e\npython /scrape.py > /tmp/qmk.json\ncarapace-spec-argparse --stdout /tmp/qmk.json\n' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]