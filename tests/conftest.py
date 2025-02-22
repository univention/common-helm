
def pytest_addoption(parser):
    parser.addoption("--chart-path", help="Path of the Helm chart to test")
