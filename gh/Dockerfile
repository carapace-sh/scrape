FROM golang

WORKDIR /
RUN git clone https://github.com/cli/cli --branch v2.82.1 --depth 1

ADD gh.patch /

WORKDIR /cli
RUN git apply ../gh.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/gh

ENV GH_TOKEN=none
ENTRYPOINT ["gh", "_carapace", "spec"]
