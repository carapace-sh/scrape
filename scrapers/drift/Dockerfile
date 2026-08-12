FROM rust
ARG VERSION

RUN git clone https://github.com/aymanbagabas/drift --branch "${VERSION}" --depth 1

ADD drift.patch /

WORKDIR /drift
RUN git apply ../drift.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/drift"]