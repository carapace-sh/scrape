FROM rust
ARG VERSION

RUN git clone https://github.com/sharkdp/fd --branch "${VERSION}" --depth 1

ADD fd.patch /

WORKDIR /fd
RUN git apply ../fd.patch
RUN cargo add carapace_spec_clap
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/fd"]