FROM rust
ARG VERSION

RUN git clone https://github.com/sirwart/ripsecrets --branch "${VERSION}" --depth 1

ADD ripsecrets.patch /

WORKDIR /ripsecrets
RUN git apply ../ripsecrets.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/ripsecrets"]