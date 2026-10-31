FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/kubernetes-sigs/kind --branch "${VERSION}" --depth 1

ADD kind.patch /

WORKDIR /kind
RUN git apply ../kind.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/kind

ENTRYPOINT ["kind", "_carapace", "spec"]
