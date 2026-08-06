import json
import os
import re

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from python_workflow_submitter.auth.keycloak_checker import set_token_env_variable


# TODO add in maintainer when fixed
async def list_workflows(limit: int = 5, filtervalue: str = "EXAMPLES"):
    """Lists workflows available to run given the current filter.

    Args:
        limit (int): maximum number of workflows to return
        filtervalue (str): filter to apply. Valid values are:
            ["MX",
            "EXAMPLES",
            "MAGNETIC_MATERIALS",
            "CONDENSED_MATTER",
            "IMAGING",
            "BIO_CRYO_IMAGING",
            "SURFACES",
            "CRYSTALLOGRAPHY",
            "SPECTROSCOPY",]
    """
    filter = {}
    filter["scienceGroup"] = filtervalue
    token: str = set_token_env_variable()
    transport = AIOHTTPTransport(
        url="https://workflows.diamond.ac.uk/graphql",
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    valid_values = [
        "MX",
        "EXAMPLES",
        "MAGNETIC_MATERIALS",
        "CONDENSED_MATTER",
        "IMAGING",
        "BIO_CRYO_IMAGING",
        "SURFACES",
        "CRYSTALLOGRAPHY",
        "SPECTROSCOPY",
    ]
    if (filter["scienceGroup"]) in valid_values:
        lim = f"""limit: {str(limit)},"""
        fil = re.sub(r"'", "", f"""filter: {filter}""")

        mutation = gql(
            """query WorkflowTemplates {
            workflowTemplates("""
            + lim
            + fil
            + """) {
                nodes {
                    name
                    title
                }
            }
        }
        """
        )
        result = await client.execute_async(
            mutation,
        )
        json_result = json.loads(re.sub(r"'", '"', str(result)))
        print(json.dumps(json_result, indent=2))
    else:
        print("Filter value must be in: " + str(valid_values))


async def list_workflows_in_visit(
    limit: int = 5,
    filter: dict[str, str | dict[str, str | bool]] | None = None,
    visit: str = str(os.environ.get("VISIT")),
):
    """List workflows in a visit, with optional filtering

    Args:
        limit (int, optional): The maximum number of workflows to describe.
            Defaults to 5.
        filter (dict[str, str  |  dict[str, str  |  bool]] | None, optional):
            The filters you wish to apply to the workflow. Includes:
            creator (fedID) (str), template (name of template ran) (str),
            status filter (dict[str,bool]) (whether pending, running, succeeded, failed,
            or error). Defaults to None.
        visit (str, optional): The visit to inspect. Defaults to
            str(os.environ.get("VISIT")).
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
    query = gql("""
    query Workflows(
    $visit: VisitInput!,
    $limit: Int!,
    $filter: WorkflowFilter
    ) {
    workflows(
        visit: $visit,
        limit: $limit,
        filter: $filter
    ) {
        nodes {
            name
            status {
                __typename
            }
        }
    }
    }
    """)

    result = await client.execute_async(
        query,
        variable_values={
            "visit": {
                "proposalCode": visit[:2],
                "proposalNumber": int(visit[2:7]),
                "number": int(visit[-1]),
            },
            "limit": limit,
            "filter": filter,
        },
    )
    json_result = json.loads(re.sub(r"'", '"', str(result)))
    print(json.dumps(json_result, indent=2))


async def info_about_workflow(
    name: str,
    visit: str = str(os.environ.get("VISIT")),
) -> None:
    """Prints the name, parameters, template reference, creator id, and status
    of a specific workflow that is running or was ran on the provided visit.

    Args:
        name (str): The name of the workflow you wish to look at.
        visit (str, optional): The visit the workflow is running / was ran on.
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
    query = gql("""
    query Workflow(
    $visit: VisitInput!,
    $name: String!,
    ) {
    workflow(
        visit: $visit,
        name: $name,
    ) {
        name
        parameters
        templateRef
        creator {creatorId}
        status {__typename}
    }
}
    """)

    result = await client.execute_async(
        query,
        variable_values={
            "visit": {
                "proposalCode": visit[:2],
                "proposalNumber": int(visit[2:7]),
                "number": int(visit[-1]),
            },
            "name": name,
        },
    )
    if result["workflow"] is not None:
        print(json.dumps(result, indent=2))
    else:
        print(f"No workflow with name {name} found.")
