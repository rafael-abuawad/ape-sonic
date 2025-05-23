import pytest
from ape._cli import cli as ape_cli
from click.testing import CliRunner

EXPECTED_OUTPUT = """
sonic
├── local  (default)
│   └── test  (default)
├── mainnet
│   └── node  (default)
└── blaze
    └── node  (default)
""".strip()


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return ape_cli


def assert_rich_text(actual: str, expected: str):
    """
    The output from `rich` causes a bunch of extra spaces to
    appear at the end of each line. For easier testing, we remove those here.
    Also, we ignore whether the expected line is at the end or in the middle
    of the output to handle cases when the test-runner has additional plugins
    installed.
    """
    expected_lines = [
        x.replace("└", "").replace("├", "").replace("│", "").strip()
        for x in expected.strip().split("\n")
    ]
    actual_lines = [
        x.replace("└", "").replace("├", "").replace("│", "").strip()
        for x in actual.strip().split("\n")
    ]

    for expected_line in expected_lines:
        assert expected_line in actual_lines


def test_networks(runner, cli, sonic):
    sonic.mainnet.set_default_provider("node")
    sonic.blaze.set_default_provider("node")

    result = runner.invoke(cli, ("networks", "list"))
    assert_rich_text(result.output, EXPECTED_OUTPUT)