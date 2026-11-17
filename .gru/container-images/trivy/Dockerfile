FROM ${GRU_BASE_IMAGE}

ARG TRIVY_VERSION=0.50.1

RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
    | sh -s -- -b /usr/local/bin "v${TRIVY_VERSION}"
