import os
from typing import TypedDict, cast

import dotenv
from keycloak import KeycloakOpenID
from keycloak.pkce_utils import generate_code_challenge, generate_code_verifier

from python_workflow_submitter.auth.open_auth_url import token_expired


class TokenResponse(TypedDict):
    access_token: str
    refresh_token: str


class DecodedToken(TypedDict):
    exp: int


def set_token_env_variable() -> str:
    """Provide the keycloak authentication token for the production graphql api.
    Requires port 8000 to be unused when ran.

    Returns:
        str: token obtained via keycloak
    """
    keycloak_openid = KeycloakOpenID(
        client_id="workflows-cli",
        server_url="https://identity.diamond.ac.uk/",
        realm_name="dls",
        client_secret_key="",
        pool_maxsize=1,
    )
    port = 8000
    code_verifier = generate_code_verifier()
    code_challenge, code_challenge_method = generate_code_challenge(code_verifier)
    auth_url = keycloak_openid.auth_url(
        redirect_uri=f"http://localhost:{port}/",
        scope="openid posix-uid profile email fedid",
        state="",
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )
    if token_expired(auth_url, port):
        token = cast(
            TokenResponse,
            keycloak_openid.token(  # pyright: ignore[reportUnknownMemberType]
                grant_type="authorization_code",
                code=str(os.environ.get("AUTH")),
                redirect_uri=f"http://localhost:{port}/",
                code_verifier=code_verifier,
            ),
        )
    else:
        token = cast(
            TokenResponse,
            keycloak_openid.refresh_token(  # pyright: ignore[reportUnknownMemberType]
                str(os.environ.get("REFRESHTOKEN"))
            ),
        )
    token_info = cast(
        DecodedToken,
        keycloak_openid.decode_token(  # pyright: ignore[reportUnknownMemberType]
            token["access_token"]
        ),
    )
    try:
        expire_time = int(token_info["exp"])
        dotenv.set_key("src/.env", "EXPIRY", str(expire_time))
        dotenv.set_key("src/.env", "TOKEN", token["access_token"].strip("'"))
        dotenv.set_key("src/.env", "REFRESHTOKEN", token["refresh_token"].strip("'"))
    except AttributeError:
        print("ERROR:")
        exit(1)
    finally:
        dotenv.load_dotenv(dotenv_path="src/.env", override=True)

    return token["access_token"]
