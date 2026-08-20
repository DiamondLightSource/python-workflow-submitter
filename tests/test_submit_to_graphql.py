from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from python_workflow_submitter.submit_workflow import (
    submit_workflow,
    submit_workflow_yaml,
)


@pytest.mark.asyncio
@patch("python_workflow_submitter.submit_workflow.dotenv.load_dotenv")
@patch("python_workflow_submitter.submit_workflow.open")
@patch("python_workflow_submitter.submit_workflow.lint_yaml")
@patch("python_workflow_submitter.submit_workflow.set_token_env_variable")
@patch("python_workflow_submitter.submit_workflow.Client")
async def test_submit_workflow_to_graphql(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_lint: MagicMock,
    mock_open: MagicMock,
    mock_load_env: MagicMock,
):
    mock_lint.return_value = True
    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflow": {"name": "workflow123"}}
    )
    await submit_workflow_yaml("fakeyaml", visit="ks10000-3")
    mock_load_env.assert_called_once_with(dotenv_path="src/.env", override=True)
    mock_instance.execute_async.assert_called_once()
    mock_open.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.submit_workflow.print")
@patch("python_workflow_submitter.submit_workflow.open")
@patch("python_workflow_submitter.submit_workflow.lint_yaml")
@patch("python_workflow_submitter.submit_workflow.set_token_env_variable")
@patch("python_workflow_submitter.submit_workflow.Client")
async def test_submit_failed_lint(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_lint: MagicMock,
    mock_open: MagicMock,
    mock_print: MagicMock,
):
    mock_lint.return_value = False
    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflow": {"name": "workflow123"}}
    )
    await submit_workflow_yaml("fakeyaml", visit="ks10000-3")
    mock_instance.execute_async.assert_not_called()
    mock_open.assert_not_called()
    mock_print.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.submit_workflow.set_token_env_variable")
@patch("python_workflow_submitter.submit_workflow.Client")
async def test_submit_stock_workflow(
    mock_client: AsyncMock,
    mock_key: MagicMock,
):

    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflowTemplate": {"name": "workflow123"}}
    )
    await submit_workflow(name="workflow123", parameters={}, visit="ks10000-3")
    mock_instance.execute_async.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.submit_workflow.print")
@patch("python_workflow_submitter.submit_workflow.dotenv.load_dotenv")
@patch("python_workflow_submitter.submit_workflow.open")
@patch("python_workflow_submitter.submit_workflow.lint_yaml")
@patch("python_workflow_submitter.submit_workflow.set_token_env_variable")
@patch("python_workflow_submitter.submit_workflow.Client")
async def test_submit_workflow_to_graphql_bad_visit(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_lint: MagicMock,
    mock_open: MagicMock,
    mock_load_env: MagicMock,
    mock_print: MagicMock,
):
    mock_lint.return_value = True
    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflow": {"name": "workflow123"}}
    )
    await submit_workflow_yaml("fakeyaml", visit="BAD")
    mock_load_env.assert_not_called()
    mock_open.assert_not_called()
    mock_print.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.submit_workflow.print")
@patch("python_workflow_submitter.submit_workflow.set_token_env_variable")
@patch("python_workflow_submitter.submit_workflow.Client")
async def test_submit_stock_workflow_bad_visit(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_print: MagicMock,
):

    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflowTemplate": {"name": "workflow123"}}
    )
    await submit_workflow(name="workflow123", parameters={}, visit="BAD")
    mock_print.assert_called_once_with("Visit 'BAD' is invalid.")
