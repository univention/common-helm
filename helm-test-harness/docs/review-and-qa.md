# Review and QA


## Trying changes with many repositories

You'll need:
- The code of `common-helm` with the correct branch checked out.
- Clones of other repositories which you want to use for the test run.
  - Hint: Make sure to use the correct branch, esp. if changes in `common-helm`
    are related to changes in the other repository.

Start a shell via `uv`:

```shell
# TODO: Choose your shell
uv --project ../common-helm run bash
uv --project ../common-helm run zsh
```

Run the tests via one-off commands:

```shell
# portal all tests
for x in portal-server portal-consumer notifications-api frontend; do pytest $x/tests/chart; done

# udm
pytest tests/chart
```

Or use the utility script in
[`../scripts/test-many-repos.sh`](../scripts/test-many-repos.sh).


### Hints

- Be sure to have your **Helm dependencies** up to date, e.g. run `helm dep build`
  for the charts under test if needed.

- In case you want to see the **error reporting**, just go into the
  `helm-test-harness` sources and add a nice `assert False` at the end of a test
  case or tweak the chart templates to break something, e.g Labels, Annotations
  or Secrets handling.
