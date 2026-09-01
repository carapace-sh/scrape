FROM rust
ARG VERSION

RUN git clone https://github.com/pnpm/pnpm --branch "${VERSION}" --depth 1

ADD pnpm.patch /

WORKDIR /pnpm
RUN git apply ../pnpm.patch
RUN cargo add --package pnpm-cli carapace_spec_clap clap_complete
RUN cargo install --path pnpm/crates/cli --root /usr

ENTRYPOINT ["/usr/bin/pnpm"]
