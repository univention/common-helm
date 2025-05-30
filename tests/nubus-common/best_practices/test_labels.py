# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.best_practice.labels import Labels


class TestLabels(Labels):

    def resources_to_check(self, resources):
        for resource in resources:
            if resource["apiVersion"].startswith("local.test"):
                continue
            yield resource
