import pytest

from univention.testing.helm.base import Base
from pytest_helm.utils import resolve

class ConfigMap(Base): ...


class RequiredEnvVariables:
    template_file = ""

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = resolve(key, stub_value)

        configmap = helm.helm_template_file(chart_path, values, self.template_file)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_cant_be_unset(self, helm, chart_path, key, env_var, value):
        values = resolve(key, value)

        with pytest.raises(RuntimeError):
            helm.helm_template_file(chart_path, values, self.template_file)


class OptionalEnvVariables:
    template_file = ""

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = resolve(key, stub_value)

        configmap = helm.helm_template_file(chart_path, values, self.template_file)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_can_be_unset(self, helm, chart_path, key, env_var, value):
        values = resolve(key, value)

        configmap = helm.helm_template_file(chart_path, values, self.template_file)
        with pytest.raises(KeyError):
            configmap['data'][env_var]

