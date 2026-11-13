# syntax=docker/dockerfile:1.28@sha256:bb22d9815c728170f72750f4e5b0d672e06176142e1d602c7e66c050100b7e5b
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

# Inspired by: https://hynek.me/articles/docker-uv/

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20261026@sha256:20df13170832602bed0c2cf83393eb0a31eb1864c86f86e079c6d3a9271974ab
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
SHELL ["/bin/bash", "-uxo", "pipefail", "-c"]

RUN apt-get --assume-yes --verbose-versions --no-install-recommends install \
      ca-certificates \
      python3.13 \
      python3.13-venv

COPY --from=ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /usr/local/bin/uv
COPY --from=alpine/helm:4.3.2@sha256:a3b9d617c0c30a6c488cebb429c4ba83995a26dc2184599af5fd408a361b2e67 /usr/bin/helm /usr/local/bin/helm

ENV UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  UV_PYTHON_DOWNLOADS=never \
  UV_PYTHON=python3.13 \
  PYTHONUNBUFFERED=1 \
  PATH=/opt/helm-test-harness/.venv/bin:$PATH

COPY ./pytest-helm /opt/pytest-helm
COPY ./helm-test-harness/uv.lock \
  ./helm-test-harness/pyproject.toml \
  /opt/helm-test-harness/

WORKDIR /opt/helm-test-harness
RUN --mount=type=cache,target=/root/.cache \
  uv sync \
  --locked \
  --no-dev \
  --no-install-project && \
  uv export -o ./requirements.txt

# copy source code
COPY ./helm-test-harness/univention /opt/helm-test-harness/univention

RUN uv sync --locked --no-dev --no-editable

RUN \
  .venv/bin/python3.13 -V && \
  .venv/bin/python3.13 -m site && \
  .venv/bin/python3.13 -c 'import univention.testing.helm'

RUN mkdir /app
WORKDIR /app

CMD ["pytest"]
