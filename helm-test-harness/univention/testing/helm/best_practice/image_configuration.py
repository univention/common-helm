# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from pytest_helm.utils import get_containers
import pytest

from .base import BestPracticeBase


class ImageConfiguration(BestPracticeBase):
    """
    Expected container image configuration behavior.

    TODO: The check of an image configuration has to be done per container per
    workload object.

    Every container may have a different image and configuration segment in the
    values structure. This means there has to be a configurable mapping which
    maps "kind/name: map" and inside it maps "container-name: values-prefix".

    The approach taken should be to template the chart to gather the list of
    containers and then generate test cases based on this result. Every test
    case would then map values and run the check.
    """

    kinds = ("Deployment", "Job", "CronJob", "StatefulSet")
    """
    Which resource kinds to verify.
    """

    def test_global_registry_is_used_as_default(self, chart, subtests):
        values = self._load_and_map(
            """
            global:
              imageRegistry: "stub-global-registry"
            """)
        result = chart.helm_template(values)
        expected_registry = "stub-global-registry"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_registry(containers, expected_registry)

    def test_image_registry_overrides_global_default_registry(self, chart, subtests):
        values = self._load_and_map(
            """
            global:
              imageRegistry: "stub-global-registry"

            image:
              registry: "stub-registry"
            """)
        result = chart.helm_template(values)
        expected_registry = "stub-registry"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_registry(containers, expected_registry)

    def test_global_pull_policy_is_used(self, chart, subtests):
        values = self._load_and_map(
            """
            global:
              imagePullPolicy: "stub-global-pull-policy"
            """)
        result = chart.helm_template(values)
        expected_pull_policy = "stub-global-pull-policy"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_pull_policy(containers, expected_pull_policy)

    def test_image_pull_policy_is_unset_by_default(self, chart, subtests):
        """
        Kubernetes has a good heuristic to set the pull policy default.

        See: https://kubernetes.io/docs/concepts/containers/images/#imagepullpolicy-defaulting
        """
        values = self._load_and_map("{}")
        result = chart.helm_template(values)
        expected_pull_policy = None

        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                for container in containers:
                    pull_policy = container.get("imagePullPolicy", None)
                    assert pull_policy == expected_pull_policy

    def test_image_pull_policy_overrides_global_value(self, chart, subtests):
        values = self._load_and_map(
            """
            global:
              imagePullPolicy: "stub-global-pull-policy"

            image:
              pullPolicy: "stub-pull-policy"
            """)
        result = chart.helm_template(values)
        expected_pull_policy = "stub-pull-policy"
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_use_pull_policy(containers, expected_pull_policy)

    def test_global_image_pull_secrets_can_be_provided(self, chart, subtests):
        values = self._load_and_map(
            """
            global:
              imagePullSecrets:
                - "stub-secret-a"
                - "stub-secret-b"
            """)
        result = chart.helm_template(values)
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
                image_pull_secrets = resource.findone("..spec.template.spec.imagePullSecrets", default=[])
                assert image_pull_secrets == expected_secrets

    def test_local_image_pull_secrets_can_be_provided(self, chart, subtests):
        values = self._load_and_map(
            """
            imagePullSecrets:
              - "stub-secret-a"
              - "stub-secret-b"
            """)
        result = chart.helm_template(values)
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
                image_pull_secrets = resource.findone("..spec.template.spec.imagePullSecrets", default=[])
                assert image_pull_secrets == expected_secrets

    def test_image_repository_can_be_configured(self, chart, subtests):
        values = self._load_and_map(
            """
            image:
              repository: "stub-fragment/stub-image"
            """)
        result = chart.helm_template(values)

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
    def test_image_tag_can_be_configured(self, image_tag, chart, subtests):
        values = self._load_and_map(
            f"""
            image:
              tag: "{image_tag}"
                """)
        result = chart.helm_template(values)

        expected_tag = image_tag
        for containers, resource in self._generate_containers_of_resource_kinds(result):
            with subtests.test(kind=resource["kind"], name=resource["metadata"]["name"]):
                _assert_all_images_contain(containers, expected_tag)

    def test_all_image_values_are_configured(self, chart, subtests):
        values = self._load_and_map(
            """
            image:
              registry: "stub-registry.example"
              repository: "stub-fragment/stub-repository"
              tag: "stub-tag@sha256:stub-digest"
                """)
        result = chart.helm_template(values)

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
