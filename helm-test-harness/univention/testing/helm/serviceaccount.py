# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import load_yaml

from univention.testing.helm.base import Annotations, Labels, Namespace


class ServiceAccount(Annotations, Labels, Namespace):

    def test_automount_service_account_token(self, helm, chart_path):
        values = load_yaml(
            """
            serviceAccount:
              automountServiceAccountToken: true
            """)
        serviceaccount = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert serviceaccount["automountServiceAccountToken"] is True
