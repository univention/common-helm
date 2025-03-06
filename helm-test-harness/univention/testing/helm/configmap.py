import pytest

from univention.testing.helm.base import Labels

class ConfigMap(Labels): ...


# TODO: Find a better place for this
def resolve(key_string: str, value) -> dict:
    keys = key_string.split('.')
    result = {}
    current = result
    for key in keys[:-1]:
        current[key] = {}
        current = current[key]
    # Set the final key to the provided value
    current[keys[-1]] = value
    return result


def test_resolve():
    values = resolve("config.logLevel", None)
    assert values == {"config": {"logLevel": None}}


class RequiredEnvVariables:
    manifest = ""

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = resolve(key, stub_value)

        configmap = helm.helm_template_file(chart_path, values, self.manifest)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_cant_be_unset(self, helm, chart_path, key, env_var, value):
        values = resolve(key, value)

        with pytest.raises(RuntimeError):
            helm.helm_template_file(chart_path, values, self.manifest)


class OptionalEnvVariables:
    manifest = ""

    def test_can_be_set(self, helm, chart_path, key, env_var):
        stub_value = "custom-stub-value"
        values = resolve(key, stub_value)

        configmap = helm.helm_template_file(chart_path, values, self.manifest)
        assert configmap['data'][env_var] == stub_value

    @pytest.mark.parametrize("value", ["", None])
    def test_can_be_unset(self, helm, chart_path, key, env_var, value):
        values = resolve(key, value)

        configmap = helm.helm_template_file(chart_path, values, self.manifest)
        with pytest.raises(KeyError):
            configmap['data'][env_var]

