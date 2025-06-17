# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client.udm import Auth, Connection, SecretViaVolume


class TestAuth(SecretViaVolume, Auth):

    # TODO: Intentionally kept the prefix "client" to ensure that support for
    # mapping is sufficient. Change back and test in a different way.

    prefix_mapping = {
        "client": "udm",
        "global.client": "global.udm",
    }

    path_username = "data.CLIENT_API_USERNAME"
    path_volume = "spec.template.spec.volumes[?@.name=='secret-client']"
    sub_path_volume_mount = "volumeMounts[?@.name=='secret-client']"
    secret_name = "release-name-test-nubus-common-client"


class TestConnection(Connection):

    prefix_mapping = {
        "client": "udm",
        "global.client": "global.udm",
    }

    path_url = "data.CLIENT_API_URL"
