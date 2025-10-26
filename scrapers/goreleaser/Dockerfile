FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/goreleaser/goreleaser --branch "${VERSION}" --depth 1

ADD goreleaser.patch /

WORKDIR /goreleaser
RUN git apply ../goreleaser.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["goreleaser", "_carapace", "spec"]
