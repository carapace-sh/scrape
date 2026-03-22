FROM rust
ARG VERSION

RUN git clone https://github.com/sharkdp/hyperfine --branch "${VERSION}" --depth 1

ADD hyperfine.patch /

WORKDIR /hyperfine
RUN git apply ../hyperfine.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr --locked

ENTRYPOINT ["/usr/bin/hyperfine"]
