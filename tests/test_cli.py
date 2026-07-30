import subprocess
import sys

from python_workflow_submitter import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "python_workflow_submitter", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
