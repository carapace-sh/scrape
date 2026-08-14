FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/openfaas/faas-cli --branch "${VERSION}" --depth 1

ADD faas-cli.patch /

WORKDIR /faas-cli
RUN git apply ../faas-cli.patch
RUN go get github.com/carapace-sh/carapace
RUN go mod vendor
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["faas-cli", "_carapace", "spec"]