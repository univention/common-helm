# Changelog

## [0.11.2](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.11.1...v0.11.2) (2025-04-02)


### Bug Fixes

* Make deployment test more robust ([cd81e6f](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/cd81e6f616c60342fa9767fe9760b7c1b63b6cfb)), closes [univention/dev/internal/team-nubus#1096](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1096)

## [0.11.1](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.11.0...v0.11.1) (2025-04-02)


### Bug Fixes

* fixup docker build on main ([9f63421](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/9f63421f2f544ff33141db9bf8919e550def698d))
* install univention module ([55e308b](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/55e308bb151cff99f756978275daeb02a81de2a0))

## [0.11.0](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.10.0...v0.11.0) (2025-03-31)


### Features

* add TLS/dhparam volume secret tests ([c14e4a0](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/c14e4a0e9fecd36ad2eeb47a28ceb4bf02002598)), closes [univention/dev/internal/team-nubus#943](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/943)
* run commit hooks from pipeline ([641328e](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/641328ec5f197eda258e0bfd95613877b3592137)), closes [univention/dev/internal/team-nubus#943](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/943)

## [0.10.0](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.9.1...v0.10.0) (2025-03-28)


### Features

* enable unit tests for envVarSecrets in init-containers ([ddc2f90](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/ddc2f90ad4960e73b523d50ef8b7299ef7ed34ee)), closes [univention/dev/internal/team-nubus#943](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/943)

## [0.9.1](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.9.0...v0.9.1) (2025-03-20)


### Bug Fixes

* **helm-unittest:** fix wrong import ([7718dfe](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/7718dfed7e5ed6f23f93f8c8a8499b14b2505442))

## [0.9.0](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.8.0...v0.9.0) (2025-03-18)


### Features

* Add option "--helm-debug" to make the verbose output an opt-in ([89a7827](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/89a78277ef8086cf536e9f5546a3f91346e7c599))
* Add option "--values" so that additional value files can be specified ([14c7125](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/14c7125027386ec5b26a1fdca3feac04c4bc5e56))
* Allow to customize the values file list as a fixture ([b2fc398](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/b2fc3984c0526689c3e925283f539198d45078f9))
* **helm-unittest:** Added separate pyproject.toml for helm test harness library ([7806530](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/7806530198a5758b46163695a3e326def2896693)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** Base class for configmap tests. Covering labels and required / optional env variables ([0a1579b](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/0a1579bb0182c64892b7dc229871748b4903d8d6)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** Base class for secret tests. Can be easily subclassed in helm tests with TestCustomSecret(Secret) ([3df43a6](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/3df43a6d50c7a362deba9d296c08f61f1e471a92)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** Basic deployment and container linting ([4bca4ff](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/4bca4ff006e5eea416c5310b25dfec38aac37bc9)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)


### Bug Fixes

* Add docstring for fixture "helm" ([d35f5f3](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/d35f5f3bcbd19782fe6afe1d6baa2b585ba4672e))
* Ensure that "get_resource" can be used multiple times on the same result ([9954dfc](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/9954dfc32c92f99e0101dd30420240c92eb947cc))
* **helm-unittest:** Adapt testrunner container ([2f49b8c](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/2f49b8c403d4c9f84a58524de504426509a5c411))
* **helm-unittest:** Add metapackage for languageservers ([9dabb2a](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/9dabb2a250fa2445a651b5ff00e00debd0b1b0fb)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** change to correct project id ([4752f99](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/4752f99eafd3c296e6814d8f5d4d0f81abb951d9))
* **helm-unittest:** Don't add standard license header to the forked pytest_helm library ([dce169e](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/dce169efe3e0a7889c7f1ee707454149b1ed2a46))
* **helm-unittest:** Fix pyprojects ([43edfb4](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/43edfb4882060573ec1c8259650ed236181e46f1))
* **helm-unittest:** Make helm library pytest fixtures discoverable ([b3a05b9](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/b3a05b93297b8d58ab7028e181f9e5e6489e6db1)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** Migrate project from pipfile to uv ([9fc8e9e](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/9fc8e9e64281e334a06fedabdc08c55a29fbf378)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** Rename test functions to reflect their generic library approach ([15fc5db](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/15fc5dbe620118d054b8e159eb3c1464451072a3)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* **helm-unittest:** Test that every manifest templates metadata.namespace with common.names.namespace ([5752e18](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/5752e1848b35043302ed13c9c4855556a176fae4)), closes [univention/dev/internal/team-nubus#1054](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1054)
* Print YAML output as string to ease readability ([7e576e8](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/7e576e8d0179c465102010ae49d0a22d3d46d4d3))
* Skip empty documents ([e775b9a](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/e775b9afcfa545320ac1bcc840928ca51d0c2828))
* Temporarily vendor the dependencies into the repo to unblock the pipeline ([1f2a559](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/1f2a559e02f6dafd7edb443d16131b5026142d9e))

## [0.8.0](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.7.0...v0.8.0) (2025-02-27)


### Features

* Add nubus-common as a library chart ([dfa95b1](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/dfa95b1f5f46d4719f3059c3dc8bfa9a3da60248))
* **common:** Flag chart as deprecated ([38b7b31](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/38b7b315d6a028cc48b0f11e191ff962f880011b))
* **nubus-common:** Add "nubus-common.secrets.passwords.manage" ([4ed675e](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/4ed675e577864811e63f2a9d1d62dd9f7e6fc970))
* **nubus-common:** Add nubus-common.names.fullnameWithRevision ([a2c707a](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/a2c707ab9fff5db1e4bcdc609c2dfb87793bad56))
* **nubus-common:** Add secrets related utility templates ([c3258f7](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/c3258f7ac199faf2c75e76e190a4f24cc93dcced))


### Bug Fixes

* Ensure empty value files result in a map ([1dbf975](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/1dbf9752612845353358cd16b692e3146f34623f))
* **nubus-common:** Correct handling of suffix in nubus-common.secrets.name ([6de20b8](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/6de20b8e56862f475f88cc48598a35f8a01a3fde))
* **nubus-common:** Update generated readme files ([6c7aaa3](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/6c7aaa35f35aac202bf0444e204ba9e1f4cddfb0))

## [0.7.0](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.6.1...v0.7.0) (2024-07-18)


### Features

* Update pytest-helm in testrunner ([0931e02](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/0931e02f593ba95c199cc43e670907f9d66dc006))
* Update testrunner dependencies ([18a9dbc](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/18a9dbcd9fe060ee3ac88343b30f71e5eb972fa4))

## [0.6.1](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/compare/v0.6.0...v0.6.1) (2024-02-16)


### Bug Fixes

* **ci:** add Helm chart signing and publishing to souvap via OCI, common-ci 1.12.x ([74cdebf](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/74cdebf68bec256c8ddba6bf80a537b39490423b))
* **deps:** add renovate.json ([a39ddd3](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/a39ddd3cb0962c41bd3cef68e769e408bd9847be))
* **deps:** update dependency univention/customers/dataport/upx/common-ci to v1.20.1 ([9894bbd](https://git.knut.univention.de/univention/customers/dataport/upx/common-helm/commit/9894bbd3479b3f0e1bf6a5291cb00e26f0c2b519))
