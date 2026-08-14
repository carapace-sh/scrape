FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/kcl-lang/cli --branch "${VERSION}" --depth 1

ADD kcl.patch /

WORKDIR /cli
RUN git apply ../kcl.patch
RUN go get github.com/carapace-sh/carapace
RUN go mod tidy
RUN GOBIN=/usr/bin/ go install ./cmd/kcl

ENTRYPOINT ["sh", "-c", "KCL_GEN_SPEC=1 kcl"]