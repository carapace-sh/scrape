FROM golang
ARG VERSION

RUN git clone https://github.com/gravitational/teleport --branch "${VERSION}" --depth 1 /teleport

ADD tsh.patch /

WORKDIR /teleport
RUN git apply /tsh.patch
RUN go get github.com/carapace-sh/carapace-spec-kingpin
RUN GOBIN=/usr/bin/ go install ./tool/tsh

ENTRYPOINT ["tsh", "_carapace", "spec"]