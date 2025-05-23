# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from yaml import safe_load
from pytest_helm.utils import get_containers
import pytest


class ImageConfiguration:
    """
    Expected container image configuration behavior.
    """

    kinds = ("Deployment", "Job", "StatefulSet")
    """
    Which resource kinds to verify.
    """

    def test_global_registry_is_used_as_default(self, helm, chart_path, subtests):
        values = safe_load(
            """
            global:
              imageRegistry: "stub-global-registry"
        """,
        )
        result = helm.helm_template(chart_path, values)
        expected_registry = "stub-global-registry"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_registry(containers, expected_registry)

    def test_image_registry_overrides_global_default_registry(self, helm, chart_path, subtests):
        values = safe_load(
            """
            global:
              imageRegistry: "stub-global-registry"

            image:
              registry: "stub-registry"
        """,
        )
        result = helm.helm_template(chart_path, values)
        expected_registry = "stub-registry"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_registry(containers, expected_registry)

    def test_global_pull_policy_is_used(self, helm, chart_path, subtests):
        values = safe_load(
            """
            global:
              imagePullPolicy: "stub-global-pull-policy"
        """,
        )
        result = helm.helm_template(chart_path, values)
        expected_pull_policy = "stub-global-pull-policy"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_pull_policy(containers, expected_pull_policy)

    def test_image_pull_policy_overrides_global_value(self, helm, chart_path, subtests):
        values = safe_load(
            """
            global:
              imagePullPolicy: "stub-global-pull-policy"

            image:
              imagePullPolicy: "stub-pull-policy"
        """,
        )
        result = helm.helm_template(chart_path, values)
        expected_pull_policy = "stub-pull-policy"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_pull_policy(containers, expected_pull_policy)

    def test_image_pull_secrets_can_be_provided(self, helm, chart_path, subtests):
        values = safe_load(
            """
            global:
              imagePullSecrets:
                - "stub-secret-a"
                - "stub-secret-b"
        """,
        )
        result = helm.helm_template(chart_path, values)
        expected_secrets = [
            {
                "name": "stub-secret-a",
            },
            {
                "name": "stub-secret-b",
            },
        ]
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                image_pull_secrets = resource.findone("spec.template.spec.imagePullSecrets")
                assert image_pull_secrets == expected_secrets

    def test_image_repository_can_be_configured(self, helm, chart_path, subtests):
        values = safe_load(
            """
            image:
              repository: "stub-fragment/stub-image"
        """,
        )
        result = helm.helm_template(chart_path, values)

        expected_repository = "stub-fragment/stub-image"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_contain(containers, expected_repository)

    @pytest.mark.parametrize(
        "image_tag",
        [
            "stub_tag",
            "stub_tag@sha256:with-stub-digest-in-tag",
        ],
    )
    def test_image_tag_can_be_configured(self, image_tag, helm, chart_path, subtests):
        values = safe_load(
            f"""
            image:
              tag: "{image_tag}"
            """,
        )
        result = helm.helm_template(chart_path, values)

        expected_tag = image_tag
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_contain(containers, expected_tag)

    def test_all_image_values_are_configured(self, helm, chart_path, subtests):
        values = safe_load(
            """
            image:
              registry: "stub-registry.example"
              repository: "stub-fragment/stub-repository"
              tag: "stub-tag@sha256:stub-digest"
            """,
        )
        result = helm.helm_template(chart_path, values)

        expected_image = (
            "stub-registry.example/stub-fragment/"
            "stub-repository:stub-tag@sha256:stub-digest"
        )
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            for container in containers:
                name = container["name"]
                image = container["image"]
                with subtests.test(
                    kind=resource["kind"],
                    name=resource["metadata"]["name"],
                    container=name,
                ):
                    assert expected_image == image, f'Wrong image in container "{name}"'

    def _generate_containers_of_resource_kinds(self, result):
        for kind in self.kinds:
            resources = result.get_resources(kind=kind)
            for resource in resources:
                containers = get_containers(resource)
                yield containers, resource


def get_containers_of_deployment(result):
    return _get_containers_of("Deployment", result)


def _get_containers_of(kind, result):
    resource = result.get_resource(kind=kind)
    return get_containers(resource)


def _assert_all_images_contain(containers, expected_value):
    for container in containers:
        name = container["name"]
        image = container["image"]
        assert expected_value in image, f'Wrong image value in container "{name}"'


def _assert_all_images_use_registry(containers, expected_registry):
    for container in containers:
        image = container["image"]
        name = container["name"]
        assert image.startswith(expected_registry + "/"), f'Wrong registry in container "{name}"'


def _assert_all_images_use_pull_policy(containers, expected_pull_policy):
    for container in containers:
        pull_policy = container["imagePullPolicy"]
        name = container["name"]
        assert (
            pull_policy == expected_pull_policy
        ), f'Wrong imagePullPolicy in container "{name}"'
