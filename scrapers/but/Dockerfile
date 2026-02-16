FROM rust
ARG VERSION

RUN apt-get update && apt-get install -y libdbus-1-dev pkg-config

RUN git clone https://github.com/gitbutlerapp/gitbutler --branch "${VERSION}" --depth 1

ADD but.patch /

WORKDIR /gitbutler
RUN git apply ../but.patch
RUN cargo add --package but carapace_spec_clap clap_complete
RUN cargo install --path ./crates/but --root /usr --locked

ENTRYPOINT ["/usr/bin/but"]
