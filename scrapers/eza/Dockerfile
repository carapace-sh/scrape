FROM rust
ARG VERSION

RUN git clone https://github.com/eza-community/eza --branch "${VERSION}" --depth 1

ADD eza.patch /

WORKDIR /eza
RUN git apply ../eza.patch
RUN cargo add carapace_spec_clap clap_complete
RUN sed -i 's/palette = { version = "=0.7.5"/palette = { version = "0.7.7"/' Cargo.toml
RUN cargo build --release && cp target/release/eza /usr/bin/eza

ENTRYPOINT ["/usr/bin/eza"]