FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/anchore/syft --branch "${VERSION}" --depth 1

ADD syft.patch /

WORKDIR /syft
RUN git apply ../syft.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/syft

ENTRYPOINT ["syft", "_carapace", "spec"]