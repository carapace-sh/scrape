FROM rust
ARG VERSION

RUN git clone https://github.com/EpicGames/lore --branch "${VERSION}" --depth 1

ADD lore.patch /

WORKDIR /lore
RUN git apply ../lore.patch
RUN cargo add --package lore-client carapace_spec_clap
RUN cargo install --path lore-client --root /usr

ENTRYPOINT ["/usr/bin/lore"]