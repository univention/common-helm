# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess

import pytest
from pytest_helm.utils import load_yaml

TEMPLATE = "templates/secrets/test_passwords_manage.yaml"


def with_flag(values):
    return {**load_yaml(values), "testPasswordsManage": True}


def render(chart, values):
    result = chart.helm_template(with_flag(values), template_file=TEMPLATE)
    return result.get_resource()["data"]


def test_generation_is_on_for_true(chart):
    data = render(chart, """
        global:
          secrets:
            generatePasswords: true
            masterPassword: "stub-master-password"
        """)
    assert data["generate"] == "true"
    assert data["password"] != ""


@pytest.mark.parametrize("value", ["false", '"true"', '"false"', "0", "1", "15", '""'])
def test_generation_is_off_unless_unset_or_boolean_true(chart, value):
    data = render(chart, f"""
        global:
          secrets:
            generatePasswords: {value}
        client:
          auth:
            password: "stub-password"
        """)
    assert data["generate"] == ""


@pytest.mark.parametrize(
    "secrets",
    [
        """
        masterPassword: "stub-master-password"
        """,
        """
        generatePasswords: null
        masterPassword: "stub-master-password"
        """,
    ],
    ids=["unset", "null"],
)
def test_generation_is_on_when_unset(chart, secrets):
    values = {"global": {"secrets": load_yaml(secrets)}}
    result = chart.helm_template({**values, "testPasswordsManage": True}, template_file=TEMPLATE)
    data = result.get_resource()["data"]
    assert data["generate"] == "true"
    assert data["password"] != ""


def test_generation_off_ignores_master_password(chart):
    data = render(chart, """
        global:
          secrets:
            generatePasswords: false
            masterPassword: "stub-master-password"
        client:
          auth:
            password: "stub-password"
        """)
    assert data["generate"] == ""
    assert data["password"] == "stub-password"


def test_generation_off_fails_without_provided_value(chart):
    values = with_flag("""
        global:
          secrets:
            generatePasswords: false
            masterPassword: "stub-master-password"
        client:
          auth:
            password: null
        """)
    with pytest.raises(subprocess.CalledProcessError) as error:
        chart.helm_template(values, template_file=TEMPLATE)
    stderr = error.value.stderr
    assert "client.auth.password" in stderr
    assert "stub-secret" in stderr
    assert "stub-master-password" not in stderr
