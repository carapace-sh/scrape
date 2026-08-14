FROM rust
ARG VERSION

RUN git clone https://github.com/dandavison/delta --branch "${VERSION}" --depth 1

ADD delta.patch /

WORKDIR /delta
RUN git apply ../delta.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/delta"]