FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/dagger/dagger --branch "${VERSION}" --depth 1

ADD dagger.patch /

WORKDIR /dagger
RUN git apply ../dagger.patch
RUN go get github.com/carapace-sh/carapace
RUN go get google.golang.org/grpc@latest
RUN GOBIN=/usr/bin/ go install ./cmd/dagger

ENTRYPOINT ["dagger", "_carapace", "spec"]