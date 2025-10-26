FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://gitlab.com/gitlab-org/cli --branch "${VERSION}" --depth 1

ADD glab.patch /

WORKDIR /cli
RUN git apply ../glab.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/glab

ENV GLAB_SEND_TELEMETRY=false
ENTRYPOINT ["glab", "_carapace", "spec"]
