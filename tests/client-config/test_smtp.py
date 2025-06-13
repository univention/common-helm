# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client.smtp import Auth, SecretUsageViaVolume


class TestAuth(SecretUsageViaVolume, Auth):
    pass
