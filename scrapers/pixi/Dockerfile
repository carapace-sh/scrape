FROM rust
ARG VERSION

RUN git clone https://github.com/prefix-dev/pixi --branch "${VERSION}" --depth 1

ADD pixi.patch /

WORKDIR /pixi
RUN git apply ../pixi.patch
RUN cargo add --package pixi_cli carapace_spec_clap
RUN cargo install --path ./crates/pixi --root /usr --locked --features self_update

ENTRYPOINT ["/usr/bin/pixi"]
