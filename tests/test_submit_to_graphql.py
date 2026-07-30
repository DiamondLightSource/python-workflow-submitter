from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from python_workflow_submitter.submit_workflow import submit_workflow


@pytest.mark.asyncio
@patch("python_workflow_submitter.submit_workflow.dotenv.load_dotenv")
@patch("python_workflow_submitter.submit_workflow.Workflow")
@patch("python_workflow_submitter.submit_workflow.set_token_env_variable")
@patch("python_workflow_submitter.submit_workflow.Client")
async def test_submit_workflow_to_graphql(
    mock_client: AsyncMock,
    mock_key: MagicMock,
    mock_workflow: MagicMock,
    mock_load_env: MagicMock,
):

    mock_instance = AsyncMock()
    mock_key.return_value = "token"
    mock_client.return_value = mock_instance
    mock_instance.execute_async = AsyncMock(
        return_value={"submitWorkflow": {"name": "workflow123"}}
    )
    await submit_workflow(mock_workflow, host="fake", visit="ks10000-3")
    mock_load_env.assert_called_once_with(dotenv_path="src/.env", override=True)
    mock_instance.execute_async.assert_called_once()
    mock_workflow.to_yaml.assert_called_once()
