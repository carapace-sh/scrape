FROM rust
ARG VERSION

RUN git clone https://github.com/wfxr/csview --branch "${VERSION}" --depth 1

ADD csview.patch /

WORKDIR /csview
RUN git apply ../csview.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/csview"]