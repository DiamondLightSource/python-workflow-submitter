from unittest.mock import MagicMock, patch

import pytest

from python_workflow_submitter.create_helm_yaml import create_helm_yaml


@patch("python_workflow_submitter.create_helm_yaml.subprocess.run")
@patch("python_workflow_submitter.create_helm_yaml.os.path.exists")
def test_create_helm_yaml_template_not_found_raises(
    mock_exists: MagicMock,
    mock_run: MagicMock,
):
    mock_exists.return_value = False

    with pytest.raises(FileExistsError):
        create_helm_yaml(yaml_name="name.yaml", chart_dir="/charts/")

    mock_run.assert_not_called()


@patch("python_workflow_submitter.create_helm_yaml.subprocess.run")
@patch("python_workflow_submitter.create_helm_yaml.os.path.exists")
def test_create_helm_yaml_values_not_found_raises(
    mock_exists: MagicMock,
    mock_run: MagicMock,
):
    mock_exists.side_effect = lambda path: {
        "/charts/templates/name.yaml": True,
        "/charts/values.yaml": False,
    }.get(path, False)

    with pytest.raises(FileExistsError):
        create_helm_yaml(
            yaml_name="name.yaml", chart_dir="/charts", values_dir="not_real"
        )

    mock_run.assert_not_called()


@patch("python_workflow_submitter.create_helm_yaml.open")
@patch("python_workflow_submitter.create_helm_yaml.subprocess.run")
@patch("python_workflow_submitter.create_helm_yaml.os.path.exists")
def test_create_helm_yaml_real_path(
    mock_exists: MagicMock,
    mock_run: MagicMock,
    mock_open: MagicMock,
):
    mock_exists.return_value = True
    create_helm_yaml(
        yaml_name="name.yaml", chart_dir="/charts", values_dir="values_dir"
    )
    mock_run.assert_called_once_with(
        "helm template . -s templates/name.yaml  -f values_dir",
        cwd="/charts",
        shell=True,
        capture_output=True,
        text=True,
    )
    mock_open.assert_called()


@patch("python_workflow_submitter.create_helm_yaml.open")
@patch("python_workflow_submitter.create_helm_yaml.subprocess.run")
@patch("python_workflow_submitter.create_helm_yaml.os.path.exists")
def test_create_helm_yaml_real_path_no_value(
    mock_exists: MagicMock,
    mock_run: MagicMock,
    mock_open: MagicMock,
):
    mock_exists.return_value = True
    create_helm_yaml(
        yaml_name="name.yaml",
        chart_dir="/charts",
    )
    mock_run.assert_called_once_with(
        "helm template . -s templates/name.yaml  -f /charts/values.yaml",
        cwd="/charts",
        shell=True,
        capture_output=True,
        text=True,
    )
    mock_open.assert_called()


@patch("python_workflow_submitter.create_helm_yaml.open")
@patch("python_workflow_submitter.create_helm_yaml.subprocess.run")
@patch("python_workflow_submitter.create_helm_yaml.os.path.exists")
def test_create_helm_yaml_value_none(
    mock_exists: MagicMock,
    mock_run: MagicMock,
    mock_open: MagicMock,
):
    mock_exists.side_effect = lambda path: {
        "/charts/templates/name.yaml": True,
        "/charts/values.yaml": False,
    }.get(path, False)

    create_helm_yaml(yaml_name="name.yaml", chart_dir="/charts", values_dir=None)

    mock_run.assert_called_once_with(
        "helm template . -s templates/name.yaml",
        cwd="/charts",
        shell=True,
        capture_output=True,
        text=True,
    )
    mock_open.assert_called()
