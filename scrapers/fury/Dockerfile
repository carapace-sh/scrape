FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/gemfury/cli --branch "${VERSION}" --depth 1

ADD fury.patch /

WORKDIR /cli
RUN git apply ../fury.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/fury

ENTRYPOINT ["fury", "_carapace", "spec"]