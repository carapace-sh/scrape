FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/charmbracelet/gum --branch "${VERSION}" --depth 1

ADD gum.patch /

WORKDIR /gum
RUN git apply ../gum.patch
RUN go get github.com/carapace-sh/carapace-spec-kong
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["gum", "_carapace", "spec"]
