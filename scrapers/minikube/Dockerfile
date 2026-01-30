FROM golang
ARG VERSION

RUN apt-get update && apt-get install -y libvirt-dev

WORKDIR /
RUN git clone https://github.com/kubernetes/minikube --branch "${VERSION}" --depth 1

ADD minikube.patch /

WORKDIR /minikube
RUN git apply ../minikube.patch
RUN go get github.com/carapace-sh/carapace
RUN GOBIN=/usr/bin/ go install ./cmd/minikube

ENTRYPOINT ["minikube", "_carapace", "spec"]
