FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/dundee/gdu --branch "${VERSION}" --depth 1

ADD gdu.patch /

WORKDIR /gdu
RUN git apply ../gdu.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/gdu

ENTRYPOINT ["gdu", "_carapace", "spec"]