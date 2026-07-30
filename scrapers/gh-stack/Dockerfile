FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/github/gh-stack --branch "${VERSION}" --depth 1

ADD gh-stack.patch /

WORKDIR /gh-stack
RUN git apply ../gh-stack.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["gh-stack", "_carapace", "spec"]
