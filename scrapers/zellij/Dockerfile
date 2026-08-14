FROM rust
ARG VERSION

RUN git clone https://github.com/zellij-org/zellij --branch "${VERSION}" --depth 1

ADD zellij.patch /

WORKDIR /zellij
RUN git apply ../zellij.patch
RUN cargo add --package zellij carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr --locked

ENTRYPOINT ["/usr/bin/zellij"]
