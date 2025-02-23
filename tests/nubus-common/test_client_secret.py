# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from lib.client_udm import UdmClient


class TestUdmClientConfiguration(UdmClient):

    # TODO: Intentionally kept the prefix "client" to ensure that support for
    # mapping is sufficient. Change back and test in a different way.

    prefix_mapping = {
        "client": "udm",
        "global.client": "global.udm",
    }

    path_udm_api_url = "data.CLIENT_API_URL"
