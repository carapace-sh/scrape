FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/twpayne/chezmoi --branch "${VERSION}" --depth 1

ADD chezmoi.patch /

WORKDIR /chezmoi
RUN git apply ../chezmoi.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["chezmoi", "_carapace", "spec"]