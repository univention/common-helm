#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


# Run this from a folder into which the repositories have been cloned, so that
# the paths are correct.

test_suites=(
    common-helm/tests/common
    common-helm/tests/client-config
    common-helm/tests/nubus-common
    container-ldap/tests/chart/ldap-notifier
    container-ldap/tests/chart/ldap-server
    container-udm-rest/tests/chart
    container-umc/tests/chart/umc-gateway
    container-umc/tests/chart/umc-server
    license-import/tests/chart
    provisioning/tests/chart/provisioning
    provisioning/tests/chart/udm-listener
    selfservice-listener/tests/chart
    stack-data/tests/chart
    univention-portal/frontend/tests/chart
    univention-portal/notifications-api/tests/chart
    univention-portal/portal-consumer/tests/chart
    univention-portal/portal-server/tests/chart
)

for test_suite in "${test_suites[@]}"
do
    echo "${test_suite}"
    uv --project common-helm run pytest "${test_suite}" "$@"
done
