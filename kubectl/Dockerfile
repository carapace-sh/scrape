FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/kubernetes/kubernetes --branch "${VERSION}" --depth 1

ADD kubectl.patch /

WORKDIR /kubernetes
RUN git apply ../kubectl.patch
RUN go get github.com/carapace-sh/carapace
RUN go work vendor
RUN GOBIN=/usr/bin/ go install ./cmd/kubectl

ENTRYPOINT ["kubectl", "_carapace", "spec"]
