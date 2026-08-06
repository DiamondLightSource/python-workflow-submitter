import os

import dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from python_workflow_submitter.auth.keycloak_checker import set_token_env_variable
from python_workflow_submitter.lintyaml import lint_yaml


async def submit_workflow_yaml(
    path: str,
    visit: str = str(os.environ.get("VISIT")),
):
    """Submits a graphql mutation to run a given yaml file.

    Args:
        path (str): Path to the yaml file you wish to run.
        visit (str, optional): The visit to run the yaml within.
            Defaults to str(os.environ.get("VISIT")).
    """
    if lint_yaml(path):
        with open(f"{path}") as yamlfile:
            yamlstr = yamlfile.read().rstrip()
        dotenv.load_dotenv(dotenv_path="src/.env", override=True)
        token: str = set_token_env_variable()

        transport = AIOHTTPTransport(
            url="https://workflows.diamond.ac.uk/graphql",
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
                    "proposalNumber": int(visit[2:7]),
                    "number": int(visit[-1]),
                },
                "manifest": f"""{yamlstr}""",
            },
        )
        name = str(result["submitWorkflow"]["name"])
        print(f"Job '{name}' submitted to {visit}")
    else:
        print("Yaml did not successfully lint, not submitting.")


async def submit_workflow(
    name: str,
    parameters: dict,
    visit: str = str(os.environ.get("VISIT")),
):
    """_summary_

    Args:
        name (str): Name of the workflow you wish to run.
        parameters (dict): paramaters to parse into the workflow.
        visit (str, optional): The visit to run the yaml within.
            Defaults to str(os.environ.get("VISIT")).
    """
    token: str = set_token_env_variable()
    transport = AIOHTTPTransport(
        url="https://workflows.diamond.ac.uk/graphql",
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
