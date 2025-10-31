FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/go-task/task --branch "${VERSION}" --depth 1

ADD task.patch /

WORKDIR /task
RUN git apply ../task.patch
RUN go get github.com/carapace-sh/carapace github.com/spf13/cobra
RUN GOBIN=/usr/bin/ go install ./cmd/task

ENTRYPOINT ["task", "_carapace", "spec"]
