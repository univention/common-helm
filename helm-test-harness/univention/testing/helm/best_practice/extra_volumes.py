# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from collections.abc import Iterator

from pytest_helm.models import HelmTemplateResult, KubernetesResource, YamlMapping
from pytest_helm.utils import get_containers

from .base import BestPracticeBase

VOLUME_NAME = "custom-data"


class ExtraVolumes(BestPracticeBase):
    """
    Checks the `extraVolumes` and `extraVolumeMounts` behavior expected for all
    workloads of a chart.
    """

    kinds = ("Deployment", "StatefulSet", "Job", "CronJob")
    """
    Which resource kinds to verify.
    """

    containers_without_extra_volume_mounts: tuple[str, ...] = ()
    """
    Names of containers which are not expected to receive the `extraVolumeMounts`.

    Init containers which only wait for a dependency or shuffle files around
    have no use for a customization volume. Every name listed here has to show
    up in the rendered chart, so that the list cannot go stale unnoticed.
    """

    def test_extra_volumes_are_added_to_the_pod(self, chart, subtests):
        values = self._load_and_map(
            f"""
            extraVolumes:
              - name: "{VOLUME_NAME}"
                configMap:
                  name: "stub-customization"
            """)
        result = chart.helm_template(values)
        for workload in self._workloads_to_check(result):
            with subtests.test(**where(workload)):
                volumes = volumes_by_name(workload)
                assert VOLUME_NAME in volumes
                assert volumes[VOLUME_NAME]["configMap"]["name"] == "stub-customization"

    def test_extra_volume_mounts_are_added_to_the_supported_containers(self, chart, subtests):
        values = self._load_and_map(
            f"""
            extraVolumeMounts:
              - name: "{VOLUME_NAME}"
                mountPath: "/custom-data"
                readOnly: true
            """)
        excluded = set(self.containers_without_extra_volume_mounts)
        result = chart.helm_template(values)
        rendered = set()
        for workload, container in self._containers_to_check(result):
            name = container["name"]
            rendered.add(name)
            with subtests.test(**where(workload, container)):
                mounts = mount_paths(container)
                if name in excluded:
                    assert VOLUME_NAME not in mounts
                else:
                    assert VOLUME_NAME in mounts
                    assert mounts[VOLUME_NAME] == ["/custom-data"]

        stale = sorted(excluded - rendered)
        assert not stale, (
            f"Containers listed in `containers_without_extra_volume_mounts` are not "
            f"rendered by the chart: {stale}"
        )

    def test_extra_volumes_and_mounts_are_templated(self, chart, subtests):
        values = self._load_and_map(
            f"""
            extraVolumes:
              - name: "{VOLUME_NAME}"
                configMap:
                  name: '{{{{ .Release.Name }}}}-customization'

            extraVolumeMounts:
              - name: "{VOLUME_NAME}"
                mountPath: '/custom-data/{{{{ .Release.Name }}}}'
            """)
        result = chart.helm_template(values)
        for workload in self._workloads_to_check(result):
            with subtests.test(**where(workload)):
                volumes = volumes_by_name(workload)
                assert VOLUME_NAME in volumes
                assert volumes[VOLUME_NAME]["configMap"]["name"] == "release-name-customization"

        for workload, container in self._containers_to_check(result):
            if container["name"] in self.containers_without_extra_volume_mounts:
                continue
            with subtests.test(**where(workload, container)):
                mounts = mount_paths(container)
                assert VOLUME_NAME in mounts
                assert mounts[VOLUME_NAME] == ["/custom-data/release-name"]

    def test_extra_volumes_and_mounts_are_empty_by_default(self, chart, subtests):
        """An unset value must not leave a stray null entry behind."""
        result = chart.helm_template(self.adjust_values({}))
        for workload in self._workloads_to_check(result):
            with subtests.test(**where(workload)):
                assert all(workload.findall("..spec.template.spec.volumes[*]"))
                assert all(workload.findall("..volumeMounts[*]"))

    def _workloads_to_check(self, result: HelmTemplateResult) -> Iterator[KubernetesResource]:
        for kind in self.kinds:
            yield from self.resources_to_check(result.get_resources(kind=kind))

    def _containers_to_check(
        self,
        result: HelmTemplateResult,
    ) -> Iterator[tuple[KubernetesResource, YamlMapping]]:
        for workload in self._workloads_to_check(result):
            for container in get_containers(workload):
                yield workload, container


def where(workload: KubernetesResource, container: YamlMapping | None = None) -> dict:
    """
    Identify a workload, and optionally one of its containers, for `subtests.test`.

    These keyword arguments label a failing subtest, which is why the assertions
    themselves do not have to repeat the location.
    """
    identity = {"kind": workload["kind"], "name": workload["metadata"]["name"]}
    if container is not None:
        identity["container"] = container["name"]
    return identity


def volumes_by_name(workload: KubernetesResource) -> dict[str, YamlMapping]:
    """Return the `volumes` of a workload, keyed by volume name."""
    volumes = workload.findall("..spec.template.spec.volumes[*]")
    return {volume["name"]: volume for volume in volumes}


def mount_paths(container: YamlMapping) -> dict[str, list[str]]:
    """
    Return the mount paths of a container, keyed by volume name.

    A container may mount the same volume at more than one path, which is why
    the values are lists.
    """
    paths: dict[str, list[str]] = {}
    for mount in container.findall("volumeMounts[*]"):
        paths.setdefault(mount["name"], []).append(mount.get("mountPath"))
    return paths
