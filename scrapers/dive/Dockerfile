FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/wagoodman/dive --branch "${VERSION}" --depth 1

ADD dive.patch /

WORKDIR /dive
RUN git apply ../dive.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["dive", "_carapace", "spec"]