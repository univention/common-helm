import pytest

from univention.testing.helm.base import Base
from pytest_helm.utils import add_jsonpath_prefix


class ConfigMap(Labels, Namespace): ...


class RequiredEnvVariables(Base):

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = add_jsonpath_prefix(key, stub_value)

        configmap = self.helm_template_file(helm, chart_path, values, self.template_file)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_cant_be_unset(self, helm, chart_path, key, env_var, value):
        values = add_jsonpath_prefix(key, value)

        with pytest.raises(RuntimeError):
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

