FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/go-delve/delve --branch "${VERSION}" --depth 1

ADD dlv.patch /

WORKDIR /delve
RUN git apply ../dlv.patch
RUN go get github.com/carapace-sh/carapace
RUN go mod vendor
RUN GOBIN=/usr/bin/ go install ./cmd/dlv

ENTRYPOINT ["dlv", "_carapace", "spec"]