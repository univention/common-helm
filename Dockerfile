# syntax=docker/dockerfile:1.9
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

# Inspired by: https://hynek.me/articles/docker-uv/

ARG UCS_BASE_IMAGE_TAG=5.3.0-build.20260903@sha256:c0c06ea1ef4aa8fea856581ecb2ed7f9fc6b355c3f0903a1be39f02a5472dfd5
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
SHELL ["/bin/bash", "-uxo", "pipefail", "-c"]

RUN apt-get --assume-yes --verbose-versions --no-install-recommends install \
      ca-certificates \
      python3.13 \
      python3.13-venv

COPY --from=ghcr.io/astral-sh/uv:0.10.1@sha256:452e02b117acd2d4eb3ba81a607bed9733b101b6c49492e352b1973463389012 /uv /usr/local/bin/uv
COPY --from=alpine/helm:4.1.1@sha256:b5c85b997d83e89d9e8ff9215a14b03864274143981af45eb3fe729cdf782c73 /usr/bin/helm /usr/local/bin/helm

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
