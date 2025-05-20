# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client_udm import UdmClient


class TestUdmClientConfiguration(UdmClient):

    # TODO: Intentionally kept the prefix "client" to ensure that support for
    # mapping is sufficient. Change back and test in a different way.

    prefix_mapping = {
        "client": "udm",
        "global.client": "global.udm",
    }

    path_udm_api_url = "data.CLIENT_API_URL"
    path_udm_api_username = "data.CLIENT_API_USERNAME"
    path_volume_secret_udm = "spec.template.spec.volumes[?@.name=='secret-client']"
    secret_name = "release-name-test-nubus-common-client"
