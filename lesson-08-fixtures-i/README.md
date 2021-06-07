# Fixtures

## [🎥 Video 8: Fixtures 1 🎬](https://youtu.be/YrGuC45GkQc)


Fixtures provide quick access to custom Brownie objects frequently used throughout testing.  Visit the [Brownie Documentation](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html#fixtures) for more detail and the [PyTest Documentation]( https://docs.pytest.org/en/6.2.x/) for additional background.


## FIXTURES

PyTest fixtures are located in tests/conftest.py

Fixtures are created by prepending the function with the fixture decorator

	@pytest.fixture
	def my_fixture():
		...


## FIXTURE SCOPES
The scope of the fixture can be passed to determine when the fixture is destroyed.

	@pytest.fixture(scope=_scope_)
	def my_fixture():
		...

  * **function:** (default) fixture destroyed at end of test
  * **class:** fixture destroyed at last test in class
  * **module:** fixture destroyed at last test in module
  * **session:** fixture destroyed at end of test session
