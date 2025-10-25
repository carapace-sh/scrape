FROM rust
ARG VERSION

RUN git clone https://github.com/atuinsh/atuin --branch "${VERSION}" --depth 1

ADD atuin.patch /

WORKDIR /atuin
RUN git apply ../atuin.patch
RUN cargo add --package atuin carapace_spec_clap
RUN cargo install --path crates/atuin --root /usr

ENTRYPOINT ["/usr/bin/atuin"]
