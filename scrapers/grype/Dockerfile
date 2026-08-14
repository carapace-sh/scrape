FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/anchore/grype --branch "${VERSION}" --depth 1

ADD grype.patch /

WORKDIR /grype
RUN git apply ../grype.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/grype

ENTRYPOINT ["grype", "_carapace", "spec"]