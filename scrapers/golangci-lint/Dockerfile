FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/golangci/golangci-lint --branch "${VERSION}" --depth 1

ADD golangci-lint.patch /

WORKDIR /golangci-lint
RUN git apply ../golangci-lint.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/golangci-lint

ENTRYPOINT ["golangci-lint", "_carapace", "spec"]
