# Changelog

## [0.18.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.17.0...v0.18.0) (2025-06-04)


### Features

* **helm-test-harness:** make the release name configurable when templating charts ([600ce31](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/600ce318e92ce8f0d164927e8a4b35b2bb303773))
* **helm-test-harness:** Test Annotations ([a1e259c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a1e259c19a9e2af5301ea08f632ca21bf0dc4690)), closes [univention/dev/internal/team-nubus#1173](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1173)
* **helm-test-harness:** Test env variables with a default value in the helm template. With e.g. the coalesce or default functions ([4792cd9](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/4792cd97fc2658754fe850bd1c493c9da09255b9)), closes [univention/dev/internal/team-nubus#1173](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1173)
* **helm-test-harness:** Test harness for ServiceAccount manifests ([6d68a83](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/6d68a83718ed8307f5b039c3d8b6325e8e0ee23e)), closes [univention/dev/internal/team-nubus#1173](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1173)

## [0.17.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.16.0...v0.17.0) (2025-05-23)


### Features

* **helm-test-harness:** Add checks for central navigation in the owner role ([f86c3af](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/f86c3af0f280cc27e1527f3822ccb5a587521c56))
* **helm-test-harness:** Add client focused tests for object storage configuration ([3852e0e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/3852e0e2cb1f7762125bcd78a50213054076991d))
* **helm-test-harness:** Add image configuration tests from portal ([4ec103f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/4ec103f959fa1f3d05d97cf6733dcd56e78acdbe))
* **helm-test-harness:** Add pytest-subtests ([399a908](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/399a90859aa3f3f91da84723c5ef4c68299002c1))
* **helm-test-harness:** Add tests for the central navigation client ([2a2abba](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/2a2abbadca3a4f2080295c82d12b508c3837cab3))
* **helm-test-harness:** Assert on the error message in object storage client ([d0b7e4f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/d0b7e4f0d28d9566b444ac8b080e7ccd59b0f9f3))
* **helm-test-harness:** Assert on the error message in udm client ([a593bc3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a593bc3667a1ff8b15585cb4ef9c9e55285a2826))
* **helm-test-harness:** Use subtests in image configuration tests ([83eb8df](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/83eb8dfa00065026714fcf14706932c571f97141))
* **helm-test-harness:** Verify "global.secrets.keep" in client based tests ([4c7c528](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/4c7c528ac4bec7fbd1efce51fa935c582a94da3d))
* **pytest-helm:** Add fixture "chart" based on "HelmChart" class ([861fa4a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/861fa4a540846ab0e6e793d05b0ad2ee859b7b7e))
* **pytest-helm:** Add parameter "default" to "YamlMapping.findone" ([bb9c399](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/bb9c39928d3f317ced3d429110977188f8f64b5b))
* **pytest-helm:** Dump Helm's output also if the call failed ([9fd9f4d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9fd9f4dbe350fff6fa96760fa37045e11564b4b2))
* **pytest-helm:** Provide both stdout and stderr on the HelmTemplateResult ([23aecbc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/23aecbc8bb5008f7de4b4b0c24ab70fec2a9c2c9))


### Bug Fixes

* **helm-test-harness:** Adapt to catch subprocess.CalledProcessError in helm_template calls ([331a3fd](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/331a3fdbb7ac46abbd3e953a3eaca2eabd775113))
* **helm-test-harness:** Consistent naming around object storage configuration ([1f578f4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/1f578f430cfb27ac3976f3493a5407e0f121e6a4))
* **helm-test-harness:** Remove the source value in "apply_mapping" ([29c79f8](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/29c79f8911ee2a24098e8bb9991607241a30c0ed))
* **helm-test-harness:** The "accessKeyId" for S3 compatible configuration should be templated ([53ffc8d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/53ffc8ddbdfb153117a98a6374c1e6507169175f))
* **helm-test-harness:** Use "self.secret_name" to lookup the generated secret ([bedefc3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/bedefc36b30c670bc02a20f7bca80c44f7d19ca0))

## [0.16.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.15.0...v0.16.0) (2025-05-23)


### Features

* **helm-test-harness:** Add attribute "secret_key" into the test template class ([cc2c36b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/cc2c36b56748d92a4ab03447a5069b9be7561216))
* **pytest-helm:** Add KubernetesResource to represent the top level mapping ([9d431d4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9d431d404521625f823d4d31898b665d5e88d038))
* **pytest-helm:** Add new class HelmTemplateResult ([6159776](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/61597761a7179625e4c3dc3db0fa84d86b895d60))
* **pytest-helm:** Deprecate "Helm.get_resources" and "Helm.get_resource" ([185f1cc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/185f1ccc8a6ffb30483f9a2a9c4e3884f9dbfb21))
* **pytest-helm:** Document API of "findone" and "findall" including tests ([1976bb6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/1976bb63f251abeabea34517a111b4c3c0eb7010))
* **pytest-helm:** Flag "utils.findone" and "utils.findall" as deprecated ([9d2e3a8](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9d2e3a8c796ba968154a46ae3e06a4154b52d2c0))
* **pytest-helm:** Log helm command on debug level ([ba7b7df](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ba7b7dfaa1781f6c8ab4955ac2ade8114f001fe6))
* **pytest-helm:** Parse YAML maps into custom class ([e32f33c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e32f33cb795263ee7feacc22490738ada55b7fde))


### Bug Fixes

* **helm-test-harness:** Change default volume name to "secret-udm" in UDM related checks ([5bf8793](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/5bf8793638edc57ecffe10eb24aa57afcdaf9bfd))
* **helm-test-harness:** Use HelmResource.findone instead of utils.findone ([70fac57](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/70fac579354a46b170153d0320f6e579302cd557))
* **pytest-helm:** Use "findone" in "get_containers" ([96ea2f3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/96ea2f3c1ebe37974fdcd3dbdcee7f693b450f23))

## [0.15.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.14.0...v0.15.0) (2025-05-11)


### Features

* move and upgrade ucs-base-image to 0.17.3-build-2025-05-11 ([07323f2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/07323f2b06db6d4b085ecdce4744fa86211fdd22))


### Bug Fixes

* move addlicense pre-commit hook ([4684fe4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/4684fe412495ed16f6f1c62f47f06674a1461b2e))
* update common-ci to main ([3201617](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/3201617548b2bc8bef23906d7da1b1e64e90ec3e))

## [0.14.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.13.0...v0.14.0) (2025-05-09)


### Features

* Ensure that a secret has no password set by default ([5452615](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/5452615fbf29aa90dfa90a38c5fe6da95343dcc2))
* Verify that secrets in Client role are never kept ([6254865](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/625486596727d579816afd98c1da842e24f54597))


### Bug Fixes

* Add missed conftest file in pytest-helm unittests ([8b631e0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/8b631e02dc6892ae64a1d6ff0a080bab0733d870))
* Ensure that ca-certificates are present in the testrunner ([cef9385](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/cef938520ef8b714af131e89c74048742d58aeca))
* **pytest-helm:** Avoid a mutable value as a parameter default in class "Helm" ([9a55218](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9a55218bd6e25c2613b8ce4bdff671ef6f891457))
* Replace "udm" in test method name with "auth" ([294a739](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/294a7390113849a171fdc8b6c1f0fde6f4f928c3))

## [0.13.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.12.3...v0.13.0) (2025-04-29)


### Features

* Bump ucs-base-image version ([580c1e2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/580c1e2a7614cf21c17afb06013f2184543cf9e3)), closes [univention/dev/internal/team-nubus#1155](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1155)
* **nubus-common:** Migrate bitnami common from docker.io to bitnami registry ([fbc57f5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/fbc57f5d915e946b56344d05aea35e3073b344d1)), closes [univention/dev/internal/team-nubus#1131](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1131)

## [0.12.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.12.2...v0.12.3) (2025-04-22)


### Bug Fixes

* utils: findall: return all matches / secret name starts with chart name ([5365099](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/5365099e222ed0d8c2f50cc9ba5d4deffc94806f)), closes [univention/dev/internal/team-nubus#1091](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1091)

## [0.12.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.12.1...v0.12.2) (2025-04-11)


### Bug Fixes

* **testrunner:** Do not use /app mountpoint for helm-test-harness ([668475c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/668475c0b189c208bdc25122a8db73b48f30e1c6)), closes [univention/dev/internal/team-nubus#1127](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1127)

## [0.12.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.12.0...v0.12.1) (2025-04-04)


### Bug Fixes

* test-runner: add ca-certificates ([99942a5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/99942a54aadef00e30236506fa9782879234dfb8)), closes [univention/dev/internal/team-nubus#1091](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1091)

## [0.12.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.11.2...v0.12.0) (2025-04-03)


### Features

* generalized TLS secret testing ([1643958](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/16439581751a09372eb6de33a14f04b671b6f348)), closes [univention/dev/internal/team-nubus#1089](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1089)

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
