FROM rust
ARG VERSION

RUN git clone https://github.com/astral-sh/ruff --branch "${VERSION}" --depth 1

ADD ruff.patch /

WORKDIR /ruff
RUN git apply ../ruff.patch
RUN cargo add --package ruff carapace_spec_clap clap_complete
ENV CARGO_PROFILE_RELEASE_LTO=false
RUN cargo install --path crates/ruff --root /usr

ENTRYPOINT ["/usr/bin/ruff"]
