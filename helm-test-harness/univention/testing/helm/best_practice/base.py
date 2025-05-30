# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from collections.abc import Iterable

from pytest_helm.models import HelmTemplateResult
from pytest_helm.utils import load_yaml


class BestPracticeBase:
    """
    Common API for the best practice test library classes.
    """

    def _load_and_map(self, values_yaml: str):
        """
        Parse `values` from YAML and apply mapping of the values structure.
        """
        return self.adjust_values(load_yaml(values_yaml))

    def adjust_values(self, values: dict):
        """
        Intended to be overwritten in subclasses to adjust the values
        structure for the chart under test.
        """
        return values

    def resources_to_check(self, resources: HelmTemplateResult) -> Iterable[HelmTemplateResult]:
        """
        Allows to filter resources in subclasses.
        """
        return resources
