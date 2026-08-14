FROM rust
ARG VERSION

RUN git clone https://github.com/sharkdp/vivid --branch "${VERSION}" --depth 1

ADD vivid.patch /

WORKDIR /vivid
RUN git apply ../vivid.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/vivid"]