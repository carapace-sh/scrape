FROM rust
ARG VERSION

RUN git clone https://github.com/Schniz/fnm --branch "${VERSION}" --depth 1

ADD fnm.patch /

WORKDIR /fnm
RUN git apply ../fnm.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/fnm"]