# Changelog

## [0.28.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.28.1...v0.28.2) (2025-10-15)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.11 ([a18cddb](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a18cddb11bfe223fa82cd853e403d297a31ea278)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.28.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.28.0...v0.28.1) (2025-10-14)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20251009 ([a2a4629](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a2a46299cbf464c870887cee2eeece257df4be18)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.28.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.27.0...v0.28.0) (2025-10-13)


### Features

* **nubus-common:** template keymapping ([a4e5f3b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a4e5f3b7a16347a576c970c50f7ca8284339a99d)), closes [univention/dev/internal/team-nubus#1441](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1441)


### Bug Fixes

* **common:** remove obsolete common library chart ([cebc56b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/cebc56b04275f6c81c3e14dd6f66e4c7fda63867)), closes [univention/dev/internal/team-nubus#1441](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1441)

## [0.27.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.26.3...v0.27.0) (2025-09-29)


### Features

* **helm-test-harness:** Consolidate client-specific test harnesses into a few flavor-specific harnesses ([3d04ca4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/3d04ca48ceedee2eabee272bf92cae385e9d820f)), closes [univention/dev/internal/team-nubus#1399](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1399)


### Bug Fixes

* Add pytest-xdist to optionally run helm unittests in parallel ([a9012dd](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a9012dd93e245d105ed258d67716ba918ab9b2c6)), closes [univention/dev/internal/team-nubus#1399](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1399)
* **helm-test-harness:** secrets: enhance robustness against shape of linter values ([2e633ac](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/2e633ac1c0d4703ac799e2926f67e32b1ab1e66d)), closes [univention/dev/internal/team-nubus#1398](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1398)
* **helm-test-harness:** Unset global.secrets.masterPassword before testing random password generation ([ef19dfb](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ef19dfbebf8b72713bc68829b64de6f0f30e7855)), closes [univention/dev/internal/team-nubus#1399](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1399)
* **helm-test-harness:** use secret_default_key in value template ([174506e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/174506ed1085b9a2486766e369e2cd5a8ed70a3e)), closes [univention/dev/internal/team-nubus#1398](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1398)
* **pytest-helm:** Gracefully handle mapping null values ([284822a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/284822abab77be55854300251805a2ce8ceca932)), closes [univention/dev/internal/team-nubus#1399](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1399)

## [0.26.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.26.2...v0.26.3) (2025-09-28)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.9 ([5cd7f5f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/5cd7f5f2330881b0414156fa671afc46c62d9346)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.26.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.26.1...v0.26.2) (2025-09-27)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250925 ([7992bf9](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/7992bf95c3e470aa5eb68afccbab3230062e9407)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.26.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.26.0...v0.26.1) (2025-09-25)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.8 ([f3e0497](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/f3e0497da716187eaac6edc755f9de1275b805ee)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.26.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.25.1...v0.26.0) (2025-09-24)


### Features

* add kyverno-test-pre-commit reference ([f9a5a89](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/f9a5a89710791a4fa4fe17dfa26640ccdbab77f8)), closes [univention/dev/internal/team-nubus#1426](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1426)

## [0.25.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.25.0...v0.25.1) (2025-09-24)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250923 ([7f32843](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/7f32843f1111d6fb6c79146386473fdbcd9ed27c)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.25.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.9...v0.25.0) (2025-09-17)


### Features

* **helm-test-harness:** Add a generic secret test harness to test one-time configurations like the OIDC Client secret in UMC ([1cd3bf4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/1cd3bf4614b7df4189681a11dc6a11436cb24c35)), closes [univention/dev/internal/team-nubus#1435](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1435)

## [0.24.9](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.8...v0.24.9) (2025-09-16)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.7 ([83f3190](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/83f31907787a4b4b9978d102bc4a2e4380320e0a)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.8](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.7...v0.24.8) (2025-09-16)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250911 ([b6e77b5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/b6e77b508868bec5d684e7c464efc4ee6545272a)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.6...v0.24.7) (2025-09-12)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.6 ([1557cb5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/1557cb57099aaed0ad4889fac77af6f6b0918942)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.5...v0.24.6) (2025-09-11)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.3-build.20250909 ([190c0b0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/190c0b084e51d1409005ec660c59323936b99d56)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.4...v0.24.5) (2025-09-06)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.4 ([3e55172](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/3e551728ed991ae935f2b12b4d5b1c58a1ee7813)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.3...v0.24.4) (2025-09-05)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250904 ([8bc10c1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/8bc10c1017a168a85c176b5b2f4c289e2a90b02b)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.2...v0.24.3) (2025-09-02)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250828 ([26f4a97](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/26f4a977b64cef24e414baaae48e76a7944b051b)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.1...v0.24.2) (2025-08-28)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.2 ([0e48213](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/0e48213a7c717e8e490d16ea053a0403bd7d5d27)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.24.0...v0.24.1) (2025-08-27)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250821 ([7619b10](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/7619b10753e2044c35e42e0c5a5fcb684d95e418)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.24.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.23.2...v0.24.0) (2025-08-26)


### Features

* upgrade bitnami charts ([cb6d1f7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/cb6d1f7aab7840ffa4d68539669e0c1310266a8c)), closes [univention/dev/internal/team-nubus#1406](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1406)

## [0.23.2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.23.1...v0.23.2) (2025-08-19)


### Bug Fixes

* **deps:** Update dependency univention/dev/nubus-for-k8s/common-ci to v1.44.1 ([a2d99a2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a2d99a219a4a99392d79f59e8cf0d5ef5d925ec6)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.23.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.23.0...v0.23.1) (2025-08-19)


### Bug Fixes

* **deps:** Update gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base Docker tag to v5.2.2-build.20250814 ([bd7ab8d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/bd7ab8deef6a7ae93168fb641a6d572b55429a5d)), closes [#0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/issues/0)

## [0.23.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.22.0...v0.23.0) (2025-07-17)


### Features

* update ucs-base to 5.2.2-build.20250714 ([e2aefec](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e2aefec77f72126c30330c8918d315395adff623)), closes [univention/dev/internal/team-nubus#1320](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1320)


### Bug Fixes

* missing dependencies in Dockerfile ([33f3977](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/33f3977e500d37377ea09787150cab08d808fa6d)), closes [univention/dev/internal/team-nubus#1320](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1320)

## [0.22.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.21.1...v0.22.0) (2025-06-27)


### Features

* **helm-test-harness:** Verify that ldap.bindDn respects the global baseDn ([3ab5916](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/3ab59163d0788bd5203b8caca9d490c3112c8fa2)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)

## [0.21.1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.21.0...v0.21.1) (2025-06-26)


### Bug Fixes

* **helm-test-harness:** Replace hardcoded value by attribute in central navigation tests ([85daa19](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/85daa194db412a90a6654bb35cb5083687f27a0e)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)

## [0.21.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.20.0...v0.21.0) (2025-06-20)


### Features

* Add test chart "test-helm-values" ([14ac687](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/14ac687cd684e6378d349c2bc6af6529f94bb9b0))
* Add utility script to run tests on many local clones ([ea9e700](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ea9e7009378276ebf3dee66206b1a1743940f7e1))
* **helm-test-harness:** Add a deprecated decorator ([9480a53](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9480a53793a3e361718fad57f4a74c618bf9ad98))
* **helm-test-harness:** Add attribute "path_container" into DefaultAttributes ([57362a6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/57362a6dff97496653c88d5209e1be0fa72974b3))
* **helm-test-harness:** Add AuthOwner into ldap related tests ([564492e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/564492e0e1282f34a72ba2abe4905418bc724637))
* **helm-test-harness:** Add checks for the Nats client ([486c043](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/486c043ca7a85ad4d133a3ac5d1e6136d4c5dad6))
* **helm-test-harness:** Add checks for the SMTP client configuration ([de43208](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/de43208499f7dfe350be61a07bb74b0d7338f347))
* **helm-test-harness:** Add class SecretViaVolume to ldap client checks ([2b81821](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/2b818211869b53891113e8757d055e320cd6a0a1))
* **helm-test-harness:** Add client test template for memcached ([e2f3ff5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e2f3ff5b30293e3171d5146ada9439b50c6da256))
* **helm-test-harness:** Add common utility methods into AuthUsername for provisioning api ([85e41a1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/85e41a12a600fc680535f43f40852d6b05e3c605))
* **helm-test-harness:** Add owner role support into provisioning api related tests ([baf4030](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/baf403040148fad998c60b94b947a33a572756e0))
* **helm-test-harness:** Add secret usage mixin for mount based usage into postgresql checks ([e7d4670](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e7d4670c16d58b6704b69e3883460fd73a722b63))
* **helm-test-harness:** Add simple test template for a solo plain password value ([0bc9a8a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/0bc9a8a977d05bf9ae7256c4ac2b107b5ed3cf42))
* **helm-test-harness:** Add test template for consumer registration in provisioning api ([06fcb78](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/06fcb78a305ea2f7fff7de241552007c7e572ad5))
* **helm-test-harness:** Add umc client ([036fb21](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/036fb219a415ff9aac38117b879d4ca52c4ecaa7))
* **helm-test-harness:** Add UsernameViaEnv into provisioning api related checks ([e4978b4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e4978b4150f10cd42f73aa380c4e1eb284a8b3da))
* **helm-test-harness:** Change to "image.pullPolicy" instead of "image.imagePullPolicy" ([67a3214](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/67a3214cce2d9c94589f5c38157fae8db2b48ff6))
* **helm-test-harness:** Check nats connection parameters are quoted ([cf59b48](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/cf59b48ebb7d56a7f8ac34b9d73c4da90625ed1a))
* **helm-test-harness:** Cover "keep" handling in ldap and centralNavigation cases ([9ea5a07](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9ea5a07a21c73f0327101348fec3f6170c9f8109))
* **helm-test-harness:** Ensure that image pull policy is not configured by default ([60ebc06](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/60ebc06855e1f5dbd92ec0aa737b52cc59710cf4))
* **helm-test-harness:** Split nats client tests into AuthPassword and AuthUser ([34d644c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/34d644cd28a6ce23aab16df9c78278da6cd12ae7))
* **helm-test-harness:** Split out secret usage for postgresql checks ([b52d6d2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/b52d6d226706116724952ddd7297f47702f3bc26))
* **helm-test-harness:** Split the classes around ldap tests into smaller fragments ([c7dcaa6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/c7dcaa6bf5fe0d3a44b8b813c2057e4b585c5020))
* **helm-test-harness:** Trigger quoting errors in ldap connection tests ([c6dc041](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/c6dc04153973e5a06b4e2c2b342f82b45fff23e7))
* **nubus-common:** Add nubus-common.images.renderPullSecrets ([4d5a3a4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/4d5a3a42437d6acc3fc91628111883b698be93ec))
* **pytest-helm:** Report values of the call to helm_template ([fb2c961](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/fb2c961cdc8ca85a2aad56ec4a50ca584d0ca50c))


### Bug Fixes

* **helm-test-harness:** Adjust "path_container" default to work with CronJobs ([279598e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/279598ea5fe4602de16f397adeda0d7dba1d8853))
* **helm-test-harness:** Adjust username related smtp tests ([de06654](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/de066549ec422b0f0b4e86082319399a74da5970))
* **helm-test-harness:** Allow for ldap configuration to be nested ([d2cec78](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/d2cec788264d9e846fde1e56fea9618fa9dbfc40))
* **helm-test-harness:** Apply load_and_map in all image configuration related tests ([cbbc091](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/cbbc091dadb0d5ca1becce233ad7a5507a4b70bd))
* **helm-test-harness:** Correct check to enforce no default pull policy is set ([a15563e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a15563e057d7f6402616700d2c33ba974dcb0df2))
* **helm-test-harness:** Correct test values in check of image pull policy ([89c093a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/89c093af0fe0e356830222813f852bab7655934f))
* **helm-test-harness:** Handle wrong type in "keyMapping" gracefully ([9432e0f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9432e0f9c7c2ae8a62d1906500dbfa44e8b8fec8))
* **helm-test-harness:** Move derived password value into attribute in ldap tests ([f7b42b4](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/f7b42b409cf3130e5784e55232d2881d1c9673fc))
* **helm-test-harness:** Use secret_default_key in provisioning api related checks ([89e561f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/89e561f55ba184283f2db0211a1d886ad5ec72f4))
* Update container base image to version 0.18.2-build-2025-06-12 ([04ead7c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/04ead7c20fc0d2d21666130cfd495ca34436b46b))

## [0.20.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.19.0...v0.20.0) (2025-06-12)


### Features

* **helm-test-harness:** Add "workload_resource_kind" attribute into LDAP tests ([681cf2b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/681cf2bae7ead9167a5e34d805d4289d5c16b166)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add base class for best practice checks ([de23c14](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/de23c14d59a18102658e5e63c2aaa6e1b77ad9bf)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add check for local image pull secrets configuration ([e8f6de1](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e8f6de1b5ad9d817c6e0e76a916889d7377c32db)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add mixin LdapConnectionUri ([576c981](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/576c981e562555b178632e272674d3446f5de260))
* **helm-test-harness:** Add mixin to verify the ldap connection uri via config map ([b9bacb5](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/b9bacb553e3da48e94052c5afae0055f5a949c5c))
* **helm-test-harness:** Add support for CronJob resources in image related checks ([e8ecb23](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e8ecb236223518305150242b18938e3671c653b8)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Adjust json path in ldap tests to also work for CronJob objects ([401c64c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/401c64c45f2605bf90e7f3c87e43f3a4077804bc))
* **helm-test-harness:** Allow to filter out resources in labels test ([ce87e11](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ce87e11bcb7b724614e54c1bf8cc3e620a8a04ff)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** BaseTest inherits now DefaultAttributes ([089004a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/089004a2cf9eea4a9b9b6bb7d5777226144a8245))
* **helm-test-harness:** Duplicate password usage checks in ldap ([c0ab53b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/c0ab53bccd2e7782d0e17f4ba85e5c64af34e181)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Find "bind dn" in ldap tests via utility method ([fd67a10](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/fd67a100c1240ef800e9e18d0af425270724257d)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Ldap client test template allows the auth usage to be customized ([ed610c2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ed610c2332fce985b73a7b26a84c34807b85a5b7)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Move ldap connection related tests into ConnectionHostAndPort ([28d4919](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/28d491954507cb05a61cb6c039d47c66b49a378f))
* **helm-test-harness:** Remove unused code in image related tests ([33ef663](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/33ef6636cedd496168d33cc3684d147ae1540238)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Support copy operation in apply_mapping ([43bdd4e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/43bdd4e7b1c7c0435190ad51fed63c3b5a39f344)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **nubus-common:** Add template "nubus-common.annotations.render" ([997c02a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/997c02a26ae7592ea3e395538ce2fef4b89ea99e)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **nubus-common:** Add utility template "nubus-common.annotations.entries" ([b9e6ebd](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/b9e6ebdefe5f9a0dfb89cc9144e62973bb50a117)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Report Helm output in case of failed calls to "helm template" ([aabfb76](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/aabfb76ba108946b2eb2643328ea16c0df0de9ae)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Support also containers in CronJob resources ([e075f4c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e075f4c38c4f49af70b95a1ca067400597d16896)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)


### Bug Fixes

* **helm-test-harness:** Use HelmTemplateResult.get_resource in base class ([4436118](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/443611827a1c6afe75dad5c50d7c73e0f3ba9b68)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Avoid creating ghost keys in apply_mapping ([c1dbbbc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/c1dbbbc06f2d1854918a400f2e0b047dbac8fc84)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)

## [0.19.0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/compare/v0.18.0...v0.19.0) (2025-06-06)


### Features

* **common:** Migrate tests to use "pytest_helm.utils.load_yaml" ([c845228](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/c8452283b2a13df240ab68cadb74f1afdcb8ec09)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Activate assertion rewriting for all modules in pytest ([48bd942](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/48bd942da6c052f7cbdf7d19f04bb6180091a377)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add attribute workload_resource_type for object storage checks ([6a86b6a](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/6a86b6aa77fee740b7739af1ff0cdfc4719155f5)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add best practice checks for labels and annotations ([9a3614f](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/9a3614f41a0a179478f4ea335f0d11eac86ada05)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add best practice tests checking "additionalLabels" ([c014025](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/c01402545d055554295c6cb8d62b2a069dc74b46)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add check regarding correct default key to ObjectStorage ([96e943c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/96e943c80d8141434679b5dd8d1e56601f0d6a5b)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add checks for ldap client configuration ([ceaf286](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ceaf286458bef3f7fb77803491bc14ca3f80e67b)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add checks for postgresql client host and port configuration ([b5eb40c](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/b5eb40c45ad6cac62442f8739d1cab2b4900751e)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add checks for provisioning api client configuration ([bfbe827](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/bfbe827318c04d63c6f8ce2cf73fba73cbd2f772)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add more flexibility into UDM client tests ([2864ffc](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/2864ffcd0fd9dc187019d7d18730718e3b60f001)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Add postgresql client tests for authentication parameters ([e55e280](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e55e2803d1b1af31b6b147a986dd0eb0ece36cda)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Check connection parameters in ldap client test ([638beb7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/638beb73ad4c180da4dc2c126106be06eaac6258)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Improve errors in best practice tests by returning default values ([a5cb28b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/a5cb28b5a9609e524f85e6e49006273976e9ed02)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Migrate to "pytest_helm.utils.load_yaml" ([e56073b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e56073babf02fc19c157dd0c0a91aff3b202e018)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Use "chart" fixture in object storage tests ([e0405c7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/e0405c712ed34884d4d0c67ef93bd858c1a62dea)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest_helm:** Use ruamel.yaml in Helm fixture ([7a9cf76](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/7a9cf761fdf16eb0d57e39d24b8c38a2a95b19d6)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Add dumping of accessed resources via pytest's reporting ([549c73e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/549c73e80f21b9d6447aa72af35b2428a4289292)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Add utility function "load_yaml" ([5773e5d](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/5773e5d6e2cc7a77aaad36e64a57a63ac6db6c4b)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Prepare integration of ruamel.yaml with pytest_helm ([187d0b2](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/187d0b2b28f02f897b0be2f7f54bedf6ad0ce73c)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Remove usage of pyyaml including the dependency on it ([64bc8a7](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/64bc8a708edeab0e6510a184eaa9136ed34cb941)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Skip rendering Helm tests by default ([bd710d3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/bd710d3d4cd9ed8963cc0fb6d7b0c9b384e6c301)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Support a fixture "helm_default_values" ([7470b42](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/7470b42a5f32cfc733d5273bbf50e8eac021acdd)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Use ruamel.yaml in the reporting ([ad7910e](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ad7910e0295f780abe8341b15330d78dfc00c48c)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)


### Bug Fixes

* **common:** Skip rendering of values section in README ([561f3f6](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/561f3f6471ea0d8fb3a2b4b252fcf5cfd8c7e56e)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Correct case handling in object storage tests ([6b00577](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/6b005776bda7619035830d28f12ee78e66a1c75d)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **helm-test-harness:** Use snake case for keys in a Secret for object storage ([984fbdd](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/984fbdd2d92cd1f9c0c9d0506d02acef6e518d8f)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **nubus-common:** Skip rendering of values section in README ([ba8cb0b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/ba8cb0b0f70aa12b76f90414efef789b800b0819)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Correct handling of missing "initContainers" in "get_containers" ([201b10b](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/201b10b3c2a489c9926b99aab72ce1dc6dad27fc)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Raise KeyError if path cannot be found in YamlMapping.findone ([b4c7cd3](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/b4c7cd3c35c6e3ddd33a4ba958d2951c93d3e636)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)
* **pytest-helm:** Skip empty documents in result ([28353d0](https://git.knut.univention.de/univention/dev/nubus-for-k8s/common-helm/commit/28353d0ff5a83064f46f7b842b184f0877918bda)), closes [univention/dev/internal/team-nubus#892](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/892)

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
