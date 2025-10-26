FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/kubernetes/kubernetes --branch "${VERSION}" --depth 1

ADD kubeadm.patch /

WORKDIR /kubernetes
RUN git apply ../kubeadm.patch
RUN go get github.com/carapace-sh/carapace
RUN go work vendor
RUN GOBIN=/usr/bin/ go install ./cmd/kubeadm

ENTRYPOINT ["kubeadm", "_carapace", "spec"]
