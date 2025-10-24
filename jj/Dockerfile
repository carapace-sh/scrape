FROM rust

RUN git clone https://github.com/jj-vcs/jj --branch v0.34.0 --depth 1

ADD jj.patch /

WORKDIR /jj
RUN git apply ../jj.patch
RUN cargo add --package jj-cli carapace_spec_clap
RUN cargo install --path cli --root /usr

ENTRYPOINT ["jj"]
