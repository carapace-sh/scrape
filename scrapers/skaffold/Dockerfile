FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/GoogleContainerTools/skaffold --branch "${VERSION}" --depth 1

ADD skaffold.patch /

WORKDIR /skaffold
RUN git apply ../skaffold.patch
RUN go get github.com/carapace-sh/carapace
RUN go mod vendor
RUN GOBIN=/usr/bin/ go install ./cmd/skaffold

ENTRYPOINT ["skaffold", "_carapace", "spec"]
