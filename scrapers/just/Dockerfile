FROM rust
ARG VERSION

RUN git clone https://github.com/casey/just --branch "${VERSION}" --depth 1

ADD just.patch /

WORKDIR /just
RUN git apply ../just.patch
RUN cargo add carapace_spec_clap
RUN cargo install --path .  --root /usr

ENTRYPOINT ["/usr/bin/just"]
