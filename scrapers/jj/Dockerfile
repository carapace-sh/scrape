FROM rust
ARG VERSION

RUN git clone https://github.com/jj-vcs/jj --branch "${VERSION}" --depth 1

ADD jj.patch /

WORKDIR /jj
RUN git apply ../jj.patch
RUN cargo install --locked --path cli --root /usr

ENTRYPOINT ["jj"]
