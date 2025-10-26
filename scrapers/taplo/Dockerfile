FROM rust
ARG VERSION

RUN git clone https://github.com/tamasfe/taplo --branch "${VERSION}" --depth 1

ADD taplo.patch /

WORKDIR /taplo
RUN git apply ../taplo.patch
RUN cargo add carapace_spec_clap clap_complete --package taplo-cli
RUN cargo install --path crates/taplo-cli --root /usr

ENTRYPOINT ["/usr/bin/taplo"]
