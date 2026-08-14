FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/dlvhdr/gh-dash --branch "${VERSION}" --depth 1

ADD gh-dash.patch /

WORKDIR /gh-dash
RUN git apply ../gh-dash.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["gh-dash", "_carapace", "spec"]