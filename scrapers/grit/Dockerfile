FROM rust
ARG VERSION

RUN git clone https://github.com/gitbutlerapp/grit --branch "${VERSION}" --depth 1

ADD grit.patch /

WORKDIR /grit
RUN git apply ../grit.patch
RUN cargo add --package grit-cli clap_complete carapace_spec_clap
RUN cargo install --path grit-cli --root /usr

ENTRYPOINT ["/usr/bin/grit"]
