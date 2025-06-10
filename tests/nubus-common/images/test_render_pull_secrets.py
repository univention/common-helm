# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import load_yaml


def test_local_renders_output(chart):
    values = load_yaml(
        """
        imagePullSecrets:
          - stub-pull-secret
        """)

    result = chart.helm_template(values, template_file="templates/images/test_render_pull_secrets.yaml")
    resource = result.get_resource()
    image_pull_secrets = resource.findone("spec.template.spec.imagePullSecrets")
    assert image_pull_secrets == [{"name": "stub-pull-secret"}]


def test_global_renders_output(chart):
    values = load_yaml(
        """
        global:
          imagePullSecrets:
            - stub-pull-secret
        """)
    result = chart.helm_template(values, template_file="templates/images/test_render_pull_secrets.yaml")
    resource = result.get_resource()
    image_pull_secrets = resource.findone("spec.template.spec.imagePullSecrets")
    assert image_pull_secrets == [{"name": "stub-pull-secret"}]


def test_combines_global_and_local(chart):
    values = load_yaml(
        """
        global:
          imagePullSecrets:
            - stub-value-global

        imagePullSecrets:
          - stub-value-local
        """)
    result = chart.helm_template(values, template_file="templates/images/test_render_pull_secrets.yaml")
    resource = result.get_resource()
    image_pull_secrets = resource.findone("spec.template.spec.imagePullSecrets")
    expected_result = [
        {"name": "stub-value-global"},
        {"name": "stub-value-local"},
    ]
    assert image_pull_secrets == expected_result


def test_local_value_is_templated(chart):
    values = load_yaml(
        """
        global:
          test: global-stub-value

        imagePullSecrets:
          - "{{ .Values.global.test }}"
        """)
    result = chart.helm_template(values, template_file="templates/images/test_render_pull_secrets.yaml")
    resource = result.get_resource()
    image_pull_secrets = resource.findone("spec.template.spec.imagePullSecrets")
    assert image_pull_secrets == [{"name": "global-stub-value"}]


def test_global_value_is_templated(chart):
    values = load_yaml(
        """
        global:
          test: global-stub-value
          imagePullSecrets:
            - "{{ .Values.global.test }}"
        """)
    result = chart.helm_template(values, template_file="templates/images/test_render_pull_secrets.yaml")
    resource = result.get_resource()
    image_pull_secrets = resource.findone("spec.template.spec.imagePullSecrets")
    assert image_pull_secrets == [{"name": "global-stub-value"}]
