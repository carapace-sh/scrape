FROM golang
ARG VERSION

WORKDIR /
RUN git clone https://github.com/aws/aws-cli --branch "${VERSION}" --depth 1

ADD . /scrape

WORKDIR /scrape
RUN GOBIN=/usr/bin/ go install .

ENTRYPOINT ["aws", "/aws-cli/awscli/botocore/data/"]
