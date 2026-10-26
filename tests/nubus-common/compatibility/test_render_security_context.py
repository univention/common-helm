# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import subprocess

import pytest
from pytest_helm.utils import load_yaml


TEMPLATE = "templates/compatibility/test_render_security_context.yaml"

SECURITY_CONTEXT = """
testSecurityContext:
  enabled: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
"""

OPENSHIFT_API = ["--api-versions", "security.openshift.io/v1"]


def render(chart, values, helm_args=None):
    result = chart.helm_template(values, template_file=TEMPLATE, helm_args=helm_args)
    return result.get_resource().findone("spec.template.spec.securityContext")


def with_mode(mode):
    values = load_yaml(SECURITY_CONTEXT)
    values["global"] = {"compatibility": {"openshift": {"adaptSecurityContext": mode}}}
    return values


def test_keeps_ids_on_plain_kubernetes(chart):
    sc = render(chart, load_yaml(SECURITY_CONTEXT))
    assert sc == {
        "runAsUser": 1000,
        "runAsGroup": 1000,
        "fsGroup": 1000,
        "runAsNonRoot": True,
        "allowPrivilegeEscalation": False,
        "capabilities": {"drop": ["ALL"]},
    }


def test_removes_enabled_key(chart):
    sc = render(chart, load_yaml(SECURITY_CONTEXT))
    assert "enabled" not in sc


def test_auto_removes_ids_on_openshift(chart):
    sc = render(chart, load_yaml(SECURITY_CONTEXT), helm_args=OPENSHIFT_API)
    assert sc == {
        "runAsNonRoot": True,
        "allowPrivilegeEscalation": False,
        "capabilities": {"drop": ["ALL"]},
    }


def test_explicit_auto_removes_ids_on_openshift(chart):
    sc = render(chart, with_mode("auto"), helm_args=OPENSHIFT_API)
    assert not {"runAsUser", "runAsGroup", "fsGroup"} & set(sc)


def test_force_removes_ids_without_openshift(chart):
    sc = render(chart, with_mode("force"))
    assert not {"runAsUser", "runAsGroup", "fsGroup"} & set(sc)
    assert sc["runAsNonRoot"] is True


def test_disabled_keeps_ids_on_openshift(chart):
    sc = render(chart, with_mode("disabled"), helm_args=OPENSHIFT_API)
    assert sc["runAsUser"] == 1000
    assert sc["runAsGroup"] == 1000
    assert sc["fsGroup"] == 1000


def test_invalid_mode_fails(chart):
    with pytest.raises(subprocess.CalledProcessError):
        render(chart, with_mode("sometimes"))


def test_removes_empty_selinux_options_on_openshift(chart):
    values = load_yaml(SECURITY_CONTEXT)
    values["testSecurityContext"]["seLinuxOptions"] = {}
    sc = render(chart, values, helm_args=OPENSHIFT_API)
    assert "seLinuxOptions" not in sc


def test_keeps_selinux_options_with_level_on_openshift(chart):
    values = load_yaml(SECURITY_CONTEXT)
    values["testSecurityContext"]["seLinuxOptions"] = {"level": "s0:c1,c2"}
    sc = render(chart, values, helm_args=OPENSHIFT_API)
    assert sc["seLinuxOptions"] == {"level": "s0:c1,c2"}


def test_keeps_empty_selinux_options_on_plain_kubernetes(chart):
    values = load_yaml(SECURITY_CONTEXT)
    values["testSecurityContext"]["seLinuxOptions"] = {}
    sc = render(chart, values)
    assert sc["seLinuxOptions"] == {}
