FROM rust
ARG VERSION

RUN apt-get update && apt-get install -y libdbus-1-dev pkg-config

RUN git clone https://github.com/gitbutlerapp/gitbutler --branch "${VERSION}" --depth 1

ADD gitbutler-cli.patch /

WORKDIR /gitbutler
RUN git apply ../gitbutler-cli.patch
RUN cargo add --package gitbutler-cli carapace_spec_clap clap_complete
RUN cargo install --path ./crates/gitbutler-cli --root /usr

ENTRYPOINT ["/usr/bin/gitbutler-cli"]
