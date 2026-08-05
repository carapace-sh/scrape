FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/k3d-io/k3d --branch "${VERSION}" --depth 1

ADD k3d.patch /

WORKDIR /k3d
RUN git apply ../k3d.patch
RUN go get github.com/carapace-sh/carapace
RUN GOWORK=off GOBIN=/usr/bin/ go install .

ENTRYPOINT ["k3d", "_carapace", "spec"]
