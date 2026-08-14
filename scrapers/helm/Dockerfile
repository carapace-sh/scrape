FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/helm/helm --branch "${VERSION}" --depth 1

ADD helm.patch /

WORKDIR /helm
RUN git apply ../helm.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/helm

ENTRYPOINT ["helm", "_carapace", "spec"]