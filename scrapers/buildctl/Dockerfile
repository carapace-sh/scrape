FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/moby/buildkit --branch "${VERSION}" --depth 1

ADD buildctl.patch /
WORKDIR /buildkit
RUN git apply ../buildctl.patch
RUN go get github.com/carapace-sh/carapace-spec-urfavecli
RUN go mod tidy 2>/dev/null; go mod tidy
RUN go mod vendor
RUN GOBIN=/usr/bin/ go install ./cmd/buildctl

ENTRYPOINT ["buildctl", "_carapace", "spec"]