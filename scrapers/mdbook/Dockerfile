FROM rust
ARG VERSION

RUN git clone https://github.com/rust-lang/mdbook --branch "${VERSION}" --depth 1

ADD mdbook.patch /

WORKDIR /mdbook
RUN git apply ../mdbook.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/mdbook"]
