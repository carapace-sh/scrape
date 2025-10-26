FROM rust
ARG VERSION

RUN git clone https://github.com/ajeetdsouza/zoxide --branch "${VERSION}" --depth 1

ADD zoxide.patch /

WORKDIR /zoxide
RUN git apply ../zoxide.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/zoxide"]
