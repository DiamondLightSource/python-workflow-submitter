import os
from unittest.mock import MagicMock, patch

from python_workflow_submitter.auth.open_auth_url import (
    CallbackHandler,
    _open_auth_url,  # pyright:ignore
    token_expired,
)


@patch("python_workflow_submitter.auth.open_auth_url.dotenv.set_key")
@patch("python_workflow_submitter.auth.open_auth_url.time.time")
@patch("python_workflow_submitter.auth.open_auth_url.webbrowser.open")
@patch("python_workflow_submitter.auth.open_auth_url._ReusingHTTPServer")
def test_open_auth_url_normal_function(
    mock_http_server: MagicMock,
    mock_open_browser: MagicMock,
    mock_time: MagicMock,
    mock_set_key: MagicMock,
):
    mock_time.return_value = 100
    os.environ["EXPIRY"] = ""

    server = mock_http_server.return_value
    server.auth_code = "this_is_your_code"

    _open_auth_url("url", 5173)
    server.handle_request.assert_called_once()
    mock_open_browser.assert_called_once_with("url")
    mock_set_key.assert_called_once_with(
        "src/.env",
        "AUTH",
        "this_is_your_code",
    )
    server.socket.shutdown.assert_called_once()
    server.server_close.assert_called_once()
    assert os.environ["AUTH"] == "this_is_your_code"


@patch("python_workflow_submitter.auth.open_auth_url.dotenv.set_key")
@patch("python_workflow_submitter.auth.open_auth_url.time.time")
@patch("python_workflow_submitter.auth.open_auth_url.exit")
@patch("python_workflow_submitter.auth.open_auth_url.webbrowser.open")
@patch("python_workflow_submitter.auth.open_auth_url._ReusingHTTPServer")
def test_open_auth_url_raises_error(
    mock_http_server: MagicMock,
    mock_open_browser: MagicMock,
    mock_exit: MagicMock,
    mock_time: MagicMock,
    mock_set_key: MagicMock,
):
    mock_time.return_value = 100
    os.environ["EXPIRY"] = ""

    server = mock_http_server.return_value
    server.handle_request.side_effect = OSError

    _open_auth_url("url", 5173)
    mock_open_browser.assert_called_once_with("url")
    assert os.environ["AUTH"] == ""
    mock_exit.assert_called_once_with(1)
    mock_set_key.assert_not_called()
    server.socket.shutdown.assert_called_once()
    server.server_close.assert_called_once()


@patch("python_workflow_submitter.auth.open_auth_url._open_auth_url")
@patch("python_workflow_submitter.auth.open_auth_url.dotenv.load_dotenv")
@patch("python_workflow_submitter.auth.open_auth_url.time.time")
def test_token_expired(
    mock_time: MagicMock,
    mock_load_env: MagicMock,
    mock_open_auth_url: MagicMock,
):
    mock_time.return_value = 100
    os.environ["EXPIRY"] = "50"

    assert token_expired("url", 5173) is True

    mock_load_env.assert_called_once_with(
        dotenv_path="src/.env",
        override=True,
    )
    mock_open_auth_url.assert_called_once_with("url", 5173)


@patch("python_workflow_submitter.auth.open_auth_url._open_auth_url")
@patch("python_workflow_submitter.auth.open_auth_url.dotenv.load_dotenv")
@patch("python_workflow_submitter.auth.open_auth_url.time.time")
def test_token_not_expired(
    mock_time: MagicMock,
    mock_load_env: MagicMock,
    mock_open_auth_url: MagicMock,
):
    mock_time.return_value = 100
    os.environ["EXPIRY"] = "200"

    assert token_expired("url", 5173) is False

    mock_load_env.assert_called_once_with(
        dotenv_path="src/.env",
        override=True,
    )
    mock_open_auth_url.assert_not_called()


def test_handler_normal_function():
    handler = CallbackHandler.__new__(CallbackHandler)
    handler.path = "/?code=this_is_your_code"

    handler.server = MagicMock()

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()
    handler.wfile.write = MagicMock()

    handler.do_GET()

    assert handler.server.auth_code == "this_is_your_code"
    handler.send_response.assert_called_once_with(200)
    handler.wfile.write.assert_called_once_with(
        b"Authorization successful. You can close this window."
    )


def test_handler_error_response():
    handler = CallbackHandler.__new__(CallbackHandler)
    handler.path = "/"

    handler.server = MagicMock()

    handler.send_response = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()
    handler.wfile.write = MagicMock()

    handler.do_GET()

    handler.send_response.assert_called_once_with(400)
    handler.end_headers.assert_called_once()
    handler.wfile.write.assert_called_once_with(b"Missing authorization code.")
