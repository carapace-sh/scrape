FROM rust

RUN git clone https://github.com/rust-lang/cargo --branch 0.91.0 --depth 1

ADD cargo.patch /

WORKDIR /cargo
RUN git apply ../cargo.patch
RUN cargo add carapace_spec_clap
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/cargo"]
