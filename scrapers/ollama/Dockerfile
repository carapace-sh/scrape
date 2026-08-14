FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/ollama/ollama --branch "${VERSION}" --depth 1

ADD ollama.patch /

WORKDIR /ollama
RUN git apply ../ollama.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["ollama", "_carapace", "spec"]