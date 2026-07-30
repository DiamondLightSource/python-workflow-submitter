import os
from unittest.mock import MagicMock, call, patch

from pytest import mark

from python_workflow_submitter.auth.keycloak_checker import set_token_env_variable


@mark.parametrize(
    "return_present",
    [
        (False),
        (True),
    ],
)
@patch("python_workflow_submitter.auth.keycloak_checker.dotenv.load_dotenv")
@patch("python_workflow_submitter.auth.keycloak_checker.dotenv.set_key")
@patch("python_workflow_submitter.auth.keycloak_checker.KeycloakOpenID")
@patch("python_workflow_submitter.auth.keycloak_checker.generate_code_verifier")
@patch("python_workflow_submitter.auth.keycloak_checker.generate_code_challenge")
@patch("python_workflow_submitter.auth.keycloak_checker.token_expired")
def test_set_token_env_variable(
    mock_token_expired: MagicMock,
    mock_gen_code_challenge: MagicMock,
    mock_gen_code_verifier: MagicMock,
    mock_gen_keycloak_id: MagicMock,
    mock_set_key: MagicMock,
    mock_load_env: MagicMock,
    return_present: bool,
):
    port=8000
    mock_gen_code_verifier.return_value = "verifier"
    mock_gen_code_challenge.return_value = ("challenge", "S256")
    os.environ["AUTH"] = "auth_url_code"
    os.environ["REFRESHTOKEN"] = "refresh"

    keycloak = MagicMock()
    mock_gen_keycloak_id.return_value = keycloak
    mock_token_expired.return_value = return_present
    keycloak.auth_url.return_value = "https://mock.site"
    token = {
        "access_token": "fake_token",
        "refresh_token": "fake_refresh",
    }
    keycloak.token.return_value = token
    keycloak.refresh_token.return_value = token
    keycloak.decode_token.return_value = {"exp": 123456789}
    assert set_token_env_variable() == "fake_token"

    mock_token_expired.assert_called_once_with("https://mock.site", port)
    if return_present:
        keycloak.token.assert_called_once_with(
            grant_type="authorization_code",
            code="auth_url_code",
            redirect_uri=f"http://localhost:{port}/",
            code_verifier="verifier",
        )
        keycloak.refresh_token.assert_not_called()
    else:
        keycloak.refresh_token.assert_called_once_with("refresh")
        keycloak.token.assert_not_called()
    mock_set_key.assert_has_calls(
        [
            call("src/.env", "EXPIRY", str(123456789 + 1800)),
            call("src/.env", "TOKEN", "fake_token"),
            call("src/.env", "REFRESHTOKEN", "fake_refresh"),
        ]
    )
    mock_load_env.assert_called_once_with(
        dotenv_path="src/.env",
        override=True,
    )

@patch("python_workflow_submitter.auth.keycloak_checker.exit")
@patch("python_workflow_submitter.auth.keycloak_checker.print")
@patch("python_workflow_submitter.auth.keycloak_checker.dotenv.load_dotenv")
@patch("python_workflow_submitter.auth.keycloak_checker.dotenv.set_key")
@patch("python_workflow_submitter.auth.keycloak_checker.KeycloakOpenID")
@patch("python_workflow_submitter.auth.keycloak_checker.generate_code_verifier")
@patch("python_workflow_submitter.auth.keycloak_checker.generate_code_challenge")
@patch("python_workflow_submitter.auth.keycloak_checker.token_expired")
def test_set_token_env_variable_attribute_error(
    mock_token_expired: MagicMock,
    mock_gen_code_challenge: MagicMock,
    mock_gen_code_verifier: MagicMock,
    mock_gen_keycloak_id: MagicMock,
    mock_set_key: MagicMock,
    mock_load_env: MagicMock,
    mock_print: MagicMock,
    mock_exit: MagicMock,
):
    mock_gen_code_verifier.return_value = "verifier"
    mock_gen_code_challenge.return_value = ("challenge", "S256")
    mock_token_expired.return_value = True

    os.environ["REFRESHTOKEN"] = "refresh"

    keycloak = MagicMock()
    mock_gen_keycloak_id.return_value = keycloak

    token = {
        "access_token": "fake_token",
        "refresh_token": "fake_refresh",
    }

    keycloak.refresh_token.return_value = token

    decoded = MagicMock()
    decoded.__getitem__.side_effect = AttributeError
    keycloak.decode_token.return_value = decoded

    set_token_env_variable()

    mock_print.assert_called_once_with("ERROR:")
    mock_exit.assert_called_once_with(1)
    mock_set_key.assert_not_called()
    mock_load_env.assert_called_once_with(
        dotenv_path="src/.env",
        override=True,
    )
