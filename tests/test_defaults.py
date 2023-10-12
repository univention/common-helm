from utils import findone


def test_nothing_is_mounted_by_default(helm, chart_test_deployment):
    result = helm.helm_template(chart_test_deployment)
    deployment = helm.get_resource(result, kind="Deployment")

    assert not findone(deployment, "spec.template.spec.volumes")
    assert not findone(deployment, "spec.template.spec.containers[0].volumeMounts")
