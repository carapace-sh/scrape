FROM gcr.io/bazel-public/bazel:latest
ARG VERSION

RUN git clone https://github.com/bazelbuild/bazel --branch "${VERSION}" --depth 1

ADD bazel.patch /home/ubuntu

WORKDIR /home/ubuntu/bazel
RUN git apply ../bazel.patch
RUN bazel build //src/main/java/sh/carapace:gen_spec

ENTRYPOINT ["cat", "bazel-bin/src/main/java/sh/carapace/bazel.yaml"]
