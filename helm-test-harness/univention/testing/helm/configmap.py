# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest

from univention.testing.helm.base import Annotations, Base, Labels, Namespace
from pytest_helm.utils import add_jsonpath_prefix


class ConfigMap(Labels, Namespace, Annotations):
    ...


class RequiredEnvVariables(Base):

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = add_jsonpath_prefix(key, stub_value)

        configmap = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_cant_be_unset(self, helm, chart_path, key, env_var, value):
        values = add_jsonpath_prefix(key, value)

        with pytest.raises(subprocess.CalledProcessError):
            self.helm_template_file(helm, chart_path, values, self.template_file)


class OptionalEnvVariables(Base):

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = add_jsonpath_prefix(key, stub_value)

        configmap = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_can_be_unset(self, helm, chart_path, key, env_var, value):
        values = add_jsonpath_prefix(key, value)

        configmap = self.helm_template_file(helm, chart_path, values, self.template_file)
        with pytest.raises(KeyError):
            configmap['data'][env_var]


class DefaultEnvVariables(Base):

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = add_jsonpath_prefix(key, stub_value)

        configmap = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_can_be_unset(self, helm, chart_path, key, env_var, value):
        values = add_jsonpath_prefix(key, value)

        configmap = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert configmap['data'][env_var], "Config map key: {env_var} has no default value."
