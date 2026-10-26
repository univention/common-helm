# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import subprocess

import pytest


TEMPLATE = "templates/compatibility/test_ingress_path_type.yaml"

PATH_TYPES = ["Exact", "Prefix", "ImplementationSpecific"]

OPENSHIFT_API = ["--api-versions", "security.openshift.io/v1"]


def render(chart, mode=None, helm_args=None):
    values = {"testPathTypes": PATH_TYPES}
    if mode:
        values["global"] = {"compatibility": {"openshift": {"adaptIngress": mode}}}
    result = chart.helm_template(values, template_file=TEMPLATE, helm_args=helm_args)
    return [p["pathType"] for p in result.get_resource().findone("spec.paths")]


def test_keeps_path_types_on_plain_kubernetes(chart):
    assert render(chart) == ["Exact", "Prefix", "ImplementationSpecific"]


def test_auto_turns_exact_into_prefix_on_openshift(chart):
    assert render(chart, helm_args=OPENSHIFT_API) == ["Prefix", "Prefix", "ImplementationSpecific"]


def test_force_turns_exact_into_prefix_without_openshift(chart):
    assert render(chart, mode="force") == ["Prefix", "Prefix", "ImplementationSpecific"]


def test_disabled_keeps_exact_on_openshift(chart):
    assert render(chart, mode="disabled", helm_args=OPENSHIFT_API) == ["Exact", "Prefix", "ImplementationSpecific"]


def test_independent_of_security_context_setting(chart):
    values = {
        "testPathTypes": PATH_TYPES,
        "global": {"compatibility": {"openshift": {"adaptSecurityContext": "disabled"}}},
    }
    result = chart.helm_template(values, template_file=TEMPLATE, helm_args=OPENSHIFT_API)
    assert result.get_resource().findone("spec.paths")[0]["pathType"] == "Prefix"


def test_invalid_mode_fails(chart):
    with pytest.raises(subprocess.CalledProcessError) as error:
        render(chart, mode="sometimes")
    assert "global.compatibility.openshift.adaptIngress must be one of" in error.value.stderr
