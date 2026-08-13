FROM rust
ARG VERSION

RUN git clone https://github.com/sharkdp/bat --branch "${VERSION}" --depth 1

ADD bat.patch /

WORKDIR /bat
RUN git apply ../bat.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/bat"]