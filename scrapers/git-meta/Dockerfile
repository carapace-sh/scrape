FROM rust
ARG VERSION

RUN git clone https://github.com/git-meta/git-meta
ADD git-meta.patch /

WORKDIR /git-meta
RUN git checkout "${VERSION}"
RUN git apply ../git-meta.patch
RUN cargo add --package git-meta-cli carapace_spec_clap clap_complete
RUN cargo build --release --locked --package git-meta-cli && cp target/release/git-meta /usr/bin/git-meta

ENTRYPOINT ["/usr/bin/git-meta"]