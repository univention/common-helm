# syntax=docker/dockerfile:1.9
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

# Inspired by: https://hynek.me/articles/docker-uv/

ARG UCS_BASE_IMAGE_TAG=0.17.3-build-2025-05-11
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python-521

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
SHELL ["/bin/bash", "-uxo", "pipefail", "-c"]

RUN apt-get --assume-yes --verbose-versions --no-install-recommends install \
      ca-certificates

COPY --from=ghcr.io/astral-sh/uv:0.5.8@sha256:0bc959d4cc56e42cbd9aa9b63374d84481ee96c32803eea30bd7f16fd99d8d56 /uv /usr/local/bin/uv
COPY --from=alpine/helm:3.17.1@sha256:e8d29e13b8218a8cb7b117a10a5210922474a74467bf70b6f3f1f7d9c1818ab0 /usr/bin/helm /usr/local/bin/helm

ENV UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  UV_PYTHON_DOWNLOADS=never \
  UV_PYTHON=python3.11 \
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
  .venv/bin/python3.11 -V && \
  .venv/bin/python3.11 -m site && \
  .venv/bin/python3.11 -c 'import univention.testing.helm'

RUN mkdir /app
WORKDIR /app

CMD ["pytest"]
