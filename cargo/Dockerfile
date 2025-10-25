FROM rust
ARG VERSION

RUN git clone https://github.com/rust-lang/cargo --branch "${VERSION}" --depth 1

ADD cargo.patch /

WORKDIR /cargo
RUN git apply ../cargo.patch
RUN cargo add carapace_spec_clap
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/cargo"]
