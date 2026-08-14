FROM rust
ARG VERSION

RUN git clone https://github.com/asciinema/agg --branch "${VERSION}" --depth 1

ADD agg.patch /

WORKDIR /agg
RUN git apply ../agg.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/agg"]