FROM rust
ARG VERSION

RUN git clone https://github.com/solana-foundation/anchor --branch "${VERSION}" --depth 1

ADD anchor.patch /

WORKDIR /anchor
RUN git apply ../anchor.patch
RUN cargo add --package anchor-cli carapace_spec_clap clap_complete
RUN cargo install --path cli --root /usr --locked

ENTRYPOINT ["/usr/bin/anchor"]
