FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/charmbracelet/glow --branch "${VERSION}" --depth 1

ADD glow.patch /

WORKDIR /glow
RUN git apply ../glow.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["glow", "_carapace", "spec"]