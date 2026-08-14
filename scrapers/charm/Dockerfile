FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/charmbracelet/charm --branch "${VERSION}" --depth 1

ADD charm.patch /

WORKDIR /charm
RUN git apply ../charm.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["charm", "_carapace", "spec"]