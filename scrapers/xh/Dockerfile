FROM rust
ARG VERSION

RUN git clone https://github.com/ducaale/xh --branch "${VERSION}" --depth 1

ADD xh.patch /

WORKDIR /xh
RUN git apply ../xh.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/xh"]