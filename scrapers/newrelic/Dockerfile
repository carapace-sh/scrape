FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/newrelic/newrelic-cli --branch "${VERSION}" --depth 1

ADD newrelic.patch /

WORKDIR /newrelic-cli
RUN git apply ../newrelic.patch
RUN go get github.com/carapace-sh/carapace
RUN go mod tidy
RUN GOBIN=/usr/bin/ go install ./cmd/newrelic

ENTRYPOINT ["newrelic", "_carapace", "spec"]