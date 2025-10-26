FROM rust
ARG VERSION

RUN git clone https://github.com/jdx/mise --branch "${VERSION}" --depth 1

ADD mise.patch /

WORKDIR /mise
RUN git apply ../mise.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/mise"]
