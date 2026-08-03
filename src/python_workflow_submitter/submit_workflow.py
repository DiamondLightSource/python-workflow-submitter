import os

import dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from hera.workflows import Workflow

from python_workflow_submitter.auth.keycloak_checker import set_token_env_variable


async def submit_workflow(
    w: Workflow,
    host: str = str(os.environ.get("HOST")),
    visit: str = str(os.environ.get("VISIT")),
):
    yamlstr = w.to_yaml()  # pyright:ignore
    dotenv.load_dotenv(dotenv_path="src/.env", override=True)
    token: str = set_token_env_variable()

    transport = AIOHTTPTransport(
        url=host,
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    mutation = gql("""
mutation Submit($visit: VisitInput!, $manifest: String!) {
  submitWorkflow(
    visit: $visit
    manifest: $manifest
  ) {
    name
  }
}
""")
    result = await client.execute_async(
        mutation,
        variable_values={
            "visit": {
                "proposalCode": str(visit[:2]),
                "proposalNumber": int(visit[3:7]),
                "number": int(visit[-1]),
            },
            "manifest": f"""{yamlstr}""",
        },
    )
    name = str(result["submitWorkflow"]["name"])
    print(f"Job '{name}' submitted to {visit}")


async def submit_stock_workflow(
    name: str,
    parameters: dict,
    host: str = str(os.environ.get("HOST")),
    visit: str = str(os.environ.get("VISIT")),
):
    token: str = set_token_env_variable()
    transport = AIOHTTPTransport(
        url=host,
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    mutation = gql("""
mutation SubmitGeneric
($name: String!, $visit: VisitInput!, $parameters: JSON!){
submitWorkflowTemplate(
    name: $name
    visit: $visit
    parameters: $parameters
    ){
    name
    }
}
""")
    result = await client.execute_async(
        mutation,
        variable_values={
            "name": name,
            "visit": {
                "proposalCode": str(visit[:2]),
                "proposalNumber": int(visit[2:7]),
                "number": int(visit[-1]),
            },
            "parameters": parameters,
        },
    )
    name = str(result["submitWorkflowTemplate"]["name"])
    print(f"Job '{name}' submitted to {visit}")
