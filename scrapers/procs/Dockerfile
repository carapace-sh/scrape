FROM rust
ARG VERSION

RUN git clone https://github.com/dalance/procs --branch "${VERSION}" --depth 1

ADD procs.patch /

WORKDIR /procs
RUN git apply ../procs.patch
RUN cargo add carapace_spec_clap clap_complete
RUN cargo install --path . --root /usr

ENTRYPOINT ["/usr/bin/procs"]