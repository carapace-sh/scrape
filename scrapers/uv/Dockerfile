FROM rust
ARG VERSION

RUN git clone https://github.com/astral-sh/uv --branch "${VERSION}" --depth 1

ADD uv.patch /

WORKDIR /uv
RUN git apply ../uv.patch
ENV CARGO_PROFILE_RELEASE_LTO=false
RUN cargo install --path crates/uv --root /usr

ENTRYPOINT ["/usr/bin/uv"]
