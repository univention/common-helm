
def test_nothing_is_mounted_by_default(helm):
    common = "../helm/test-deployment"
    result = helm.helm_template(common)

    # TODO: Use the functions on the "helm" fixture instead
    result = list(result)
    deployment = result[0]

    # TODO: I'd love to write "deployment['spec.template.spec.volumes']" or similar
    assert not deployment["spec"]["template"]["spec"]["volumes"]
    assert not deployment["spec"]["template"]["spec"]["containers"][0]["volumeMounts"]

    assert False, "Finish me!"
