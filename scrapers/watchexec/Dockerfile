FROM rust
ARG VERSION

RUN git clone https://github.com/watchexec/watchexec --branch "${VERSION}" --depth 1

ADD watchexec.patch /

WORKDIR /watchexec
RUN git apply ../watchexec.patch
RUN cargo add --package watchexec-cli carapace_spec_clap clap_complete
RUN cargo install --path crates/cli --root /usr

ENTRYPOINT ["/usr/bin/watchexec"]