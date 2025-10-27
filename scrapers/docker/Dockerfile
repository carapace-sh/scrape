FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/docker/cli --branch "${VERSION}" --depth 1

ADD docker.patch /

WORKDIR /cli
RUN git apply ../docker.patch
RUN cp vendor.mod go.mod
RUN cp vendor.sum go.sum
RUN go get github.com/carapace-sh/carapace
RUN go mod tidy
RUN go mod vendor
RUN GOBIN=/usr/bin/ go install ./cmd/docker

ENTRYPOINT ["docker", "_carapace", "spec"]
