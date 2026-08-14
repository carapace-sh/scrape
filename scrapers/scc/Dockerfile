FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/boyter/scc --branch "${VERSION}" --depth 1

ADD scc.patch /

WORKDIR /scc
RUN git apply ../scc.patch
RUN go get github.com/carapace-sh/carapace
RUN go mod vendor
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["scc", "_carapace", "spec"]