FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/goreleaser/nfpm --branch "${VERSION}" --depth 1

ADD nfpm.patch /

WORKDIR /nfpm
RUN git apply ../nfpm.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/nfpm

ENTRYPOINT ["nfpm", "_carapace", "spec"]