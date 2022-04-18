import pytest

pytest_plugins = ["fixtures.accounts", "fixtures.deployments"]


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        # we treat "no tests collected" as passing
        session.exitstatus = pytest.ExitCode.OK


@pytest.fixture(autouse=True)
def isolation(module_isolation, fn_isolation):
    pass
