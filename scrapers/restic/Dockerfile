FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/restic/restic --branch "${VERSION}" --depth 1

ADD restic.patch /

WORKDIR /restic
RUN git apply ../restic.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/restic

ENTRYPOINT ["restic", "_carapace", "spec"]