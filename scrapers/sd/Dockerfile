FROM rust
ARG VERSION

RUN git clone https://github.com/chmln/sd --branch "${VERSION}" --depth 1

ADD sd.patch /

WORKDIR /sd
RUN git apply ../sd.patch
RUN cargo add --package sd-cli carapace_spec_clap clap_complete
RUN cargo install --path sd-cli --root /usr

ENTRYPOINT ["/usr/bin/sd"]