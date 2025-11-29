FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/jetify-com/devbox --branch "${VERSION}" --depth 1

ADD devbox.patch /

WORKDIR /devbox
RUN git apply ../devbox.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/devbox

ENTRYPOINT ["devbox", "_carapace", "spec"]
