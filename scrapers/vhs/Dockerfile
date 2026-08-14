FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/charmbracelet/vhs --branch "${VERSION}" --depth 1

ADD vhs.patch /

WORKDIR /vhs
RUN git apply ../vhs.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["vhs", "_carapace", "spec"]