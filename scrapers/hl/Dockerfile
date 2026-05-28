FROM rust
ARG VERSION

RUN git clone https://github.com/pamburus/hl --branch "${VERSION}" --depth 1

ADD hl.patch /

WORKDIR /hl
RUN git apply ../hl.patch
RUN cargo add carapace_spec_clap
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/hl"]
