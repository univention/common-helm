# SPDX-FileCopyrightText: 2024 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only

import jsonpath


def findone(data, path):
    return jsonpath.match(path, data).obj


def findall(data, path):
    return jsonpath.match(path, data).obj


def get_containers_of_job(helm, result):
    manifest = helm.get_resource(result, kind="Job")
    return get_containers(manifest)


def get_containers_of_deployment(helm, result):
    manifest = helm.get_resource(result, kind="Deployment")
    return get_containers(manifest)


def get_containers(manifest):
    try:
        init_containers = findall(manifest, "spec.template.spec.initContainers")
    except AttributeError:
        init_containers = []
    containers = findall(manifest, "spec.template.spec.containers")
    return init_containers + containers


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


