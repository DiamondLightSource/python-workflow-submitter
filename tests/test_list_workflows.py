from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from python_workflow_submitter.list_workflows import (
    info_about_workflow,
    list_workflows,
    list_workflows_in_visit,
)


@pytest.mark.asyncio
@patch("python_workflow_submitter.list_workflows.json.dumps")
@patch("python_workflow_submitter.list_workflows.set_token_env_variable")
@patch("python_workflow_submitter.list_workflows.Client")
async def test_list_workflows(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_json: MagicMock,
):

    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"workflowTemplates": {"name": "workflow123"}}
    )
    await list_workflows(limit=5, filter={"scienceGroup": "EXAMPLES"}, host="fake")
    mock_instance.execute_async.assert_called_once()
    mock_json.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.list_workflows.json.dumps")
@patch("python_workflow_submitter.list_workflows.set_token_env_variable")
@patch("python_workflow_submitter.list_workflows.Client")
async def test_list_workflows_in_visit(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_json: MagicMock,
):

    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"workflowTemplates": {"name": "workflow123"}}
    )
    await list_workflows_in_visit(
        limit=5,
        filter={
            "creator": "gmg29649",
            "template": "example-template",
            "workflowStatusFilter": {"succeeded": True},
        },
        host="fake",
        visit="ks10000-3",
    )
    mock_instance.execute_async.assert_called_once()
    mock_json.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.list_workflows.json.dumps")
@patch("python_workflow_submitter.list_workflows.set_token_env_variable")
@patch("python_workflow_submitter.list_workflows.Client")
async def test_info_about_workflow(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_json: MagicMock,
):
    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"workflow": {"name": "workflow123"}}
    )
    await info_about_workflow(name="fakename", host="fake", visit="ks10000-3")
    mock_instance.execute_async.assert_called_once()
    mock_json.assert_called_once()


@pytest.mark.asyncio
@patch("python_workflow_submitter.list_workflows.print")
@patch("python_workflow_submitter.list_workflows.json.dumps")
@patch("python_workflow_submitter.list_workflows.set_token_env_variable")
@patch("python_workflow_submitter.list_workflows.Client")
async def test_info_about_workflow_none_resp(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_json: MagicMock,
    mock_print: MagicMock,
):
    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(return_value={"workflow": None})
    await info_about_workflow(name="fakename", host="fake", visit="ks10000-3")
    mock_instance.execute_async.assert_called_once()
    mock_json.assert_not_called()
    mock_print.assert_called_once()
