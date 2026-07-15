FROM rust
ARG VERSION

RUN apt-get update && apt-get install -y --no-install-recommends \
        xz-utils ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ziglang.org/download/0.15.2/zig-x86_64-linux-0.15.2.tar.xz -o /tmp/zig.tar.xz \
    && tar -xf /tmp/zig.tar.xz -C /opt \
    && ln -s /opt/zig-x86_64-linux-0.15.2/zig /usr/local/bin/zig \
    && rm /tmp/zig.tar.xz

RUN git clone https://github.com/ogulcancelik/herdr --branch "${VERSION}" --depth 1

ADD herdr.patch /

WORKDIR /herdr
RUN git apply ../herdr.patch
RUN cargo add carapace_spec_clap
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/herdr"]
