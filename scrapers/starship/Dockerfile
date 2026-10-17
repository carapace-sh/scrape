FROM rust
ARG VERSION

RUN git clone https://github.com/starship/starship --branch "${VERSION}" --depth 1

ADD starship.patch /

WORKDIR /starship
RUN git apply ../starship.patch
RUN cargo add carapace_spec_clap
RUN cargo build --release && cp target/release/starship /usr/bin/starship

ENTRYPOINT ["/usr/bin/starship"]
