FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/docker/compose --branch "${VERSION}" --depth 1

ADD docker-compose.patch /

WORKDIR /compose
RUN git apply ../docker-compose.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd

ENTRYPOINT ["cmd", "_carapace", "spec"]
