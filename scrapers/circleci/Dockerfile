FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/CircleCI-Public/circleci-cli --branch "${VERSION}" --depth 1

ADD circleci.patch /

WORKDIR /circleci-cli
RUN git apply ../circleci.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/circleci

ENTRYPOINT ["circleci", "_carapace", "spec"]