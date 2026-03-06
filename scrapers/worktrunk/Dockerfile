FROM rust
ARG VERSION

RUN git clone https://github.com/max-sixty/worktrunk --branch "${VERSION}" --depth 1

ADD worktrunk.patch /

WORKDIR /worktrunk
RUN git apply ../worktrunk.patch
RUN cargo add --package worktrunk carapace_spec_clap
RUN cargo install --path . --root /usr --locked

ENTRYPOINT ["/usr/bin/wt"]
