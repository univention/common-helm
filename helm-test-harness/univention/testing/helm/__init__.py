# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

# NOTE: This ensures that the details about assert statements are printed out
# by pytest. Pytest is achieving this by rewriting the code during module
# import.
#
# See: https://docs.pytest.org/en/stable/how-to/assert.html#assertion-introspection-details

pytest.register_assert_rewrite(
    "univention.testing.helm.best_practice",
    "univention.testing.helm.client",

    # NOTE: Cannot use "univention.testing.helm" because it is already imported
    # when this code runs. Consider moving below templates into a sub-package.
    "univention.testing.helm.configmap",
    "univention.testing.helm.container",
    "univention.testing.helm.deployment",
    "univention.testing.helm.secret",
)
