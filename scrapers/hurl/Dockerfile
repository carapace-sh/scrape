FROM rust
ARG VERSION

RUN apt-get update && apt-get install -y libclang-dev

RUN git clone https://github.com/Orange-OpenSource/hurl --branch "${VERSION}" --depth 1

ADD hurl.patch /

WORKDIR /hurl
RUN git apply ../hurl.patch
RUN cargo add --package hurl carapace_spec_clap clap_complete
RUN cargo install --path ./packages/hurl --root /usr

ENTRYPOINT ["hurl"]
