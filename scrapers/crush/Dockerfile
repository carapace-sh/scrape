FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/charmbracelet/crush --branch "${VERSION}" --depth 1

ADD crush.patch /

WORKDIR /crush
RUN git apply ../crush.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["crush", "_carapace", "spec"]
