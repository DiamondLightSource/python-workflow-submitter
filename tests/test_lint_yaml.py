import subprocess
from unittest.mock import MagicMock, patch

from python_workflow_submitter.lintyaml import lint_yaml


@patch("python_workflow_submitter.lintyaml.subprocess.check_call")
@patch("python_workflow_submitter.lintyaml.os.path.exists")
def test_lint_yaml_valid_path(mock_path_exists: MagicMock, mock_sp: MagicMock):
    mock_path_exists.return_value = True
    lint_yaml("path")
    mock_sp.assert_called_once_with("argo lint path --offline", shell=True)
    assert lint_yaml("path") is True


@patch("python_workflow_submitter.lintyaml.print")
@patch("python_workflow_submitter.lintyaml.subprocess.check_call")
@patch("python_workflow_submitter.lintyaml.os.path.exists")
def test_lint_yaml_invalid_path(
    mock_path_exists: MagicMock, mock_sp: MagicMock, mock_print: MagicMock
):
    mock_path_exists.return_value = False
    lint_yaml("path")
    mock_sp.assert_not_called()
    mock_print.assert_called_once()
    assert lint_yaml("path") is False


@patch("python_workflow_submitter.lintyaml.subprocess.check_call")
@patch("python_workflow_submitter.lintyaml.os.path.exists")
def test_lint_yaml_raises_error(mock_path_exists: MagicMock, mock_sp: MagicMock):
    mock_path_exists.return_value = True
    mock_sp.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="argo lint path --offline"
    )
    assert lint_yaml("path") is False
