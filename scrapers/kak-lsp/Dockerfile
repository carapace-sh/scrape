FROM rust
ARG VERSION

RUN git clone https://github.com/kak-lsp/kak-lsp --branch "${VERSION}" --depth 1

ADD kak-lsp.patch /

WORKDIR /kak-lsp
RUN git apply ../kak-lsp.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/kak-lsp"]