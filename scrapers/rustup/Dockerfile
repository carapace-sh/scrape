FROM rust
ARG VERSION

RUN git clone https://github.com/rust-lang/rustup --branch "${VERSION}" --depth 1

ADD rustup.patch /

WORKDIR /rustup
RUN git apply ../rustup.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr
RUN mv /usr/bin/rustup-init /usr/bin/rustup

ENTRYPOINT ["/usr/bin/rustup"]
