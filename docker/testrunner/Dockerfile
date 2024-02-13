
# SPDX-FileCopyrightText: 2024 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

ARG DOCKER_PROXY
ARG PYTHON_TAG=3.11

FROM ${DOCKER_PROXY}python:${PYTHON_TAG}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /testrunner

COPY sum.txt ./

ENV DESIRED_VERSION=v3.13.1

RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/${DESIRED_VERSION}/scripts/get-helm-3 \
    && sha256sum get_helm.sh \
    && sha256sum -c sum.txt \
    && chmod 700 get_helm.sh \
    && ./get_helm.sh

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv==2023.6.18 \
    && pipenv sync --dev --system \
    && rm -r ~/.cache

WORKDIR /app

CMD [ "pytest" ]
