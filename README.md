[![CI](https://github.com/Matt-Carre/python-workflow-submitter/actions/workflows/ci.yml/badge.svg)](https://github.com/Matt-Carre/python-workflow-submitter/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/Matt-Carre/python-workflow-submitter/branch/main/graph/badge.svg)](https://codecov.io/gh/Matt-Carre/python-workflow-submitter)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
# python_workflow_submitter

 Python alternative to creating and running argo workflows in the Data Analysis Platform

This allows for the submission of yaml files to Diamond's GraphQL API.
This automatically lints yaml files before submission.

Notably, this requires a .env file in your src/ folder.

What            | Where
:---:           | :---:
Source          | <https://github.com/Matt-Carre/python-workflow-submitter>
Docker          | `docker run ghcr.io/Matt-Carre/python-workflow-submitter:latest`
Releases        | <https://github.com/Matt-Carre/python-workflow-submitter/releases>

To submit your workflow notebook:

```python
from python_workflow_submitter.submit_workflow import submit_workflow_yaml

await submit_workflow_yaml("example.yaml")
```
To submit a workflow script:
```python 
import asyncio
from python_workflow_submitter.submit_workflow import submit_workflow_yaml

asyncio.run(submit_workflow_yaml("example.yaml", visit="ks10000-3"))
```

To submit a generic workflow via a graphql mutation:

```python 
import asyncio
from python_workflow_submitter.submit_workflow import submit_workflow

asyncio.run(
    submit_workflow(
        "example-template",
        {"png": True, "jpg": False, "jpeg": True, "tif": True, "tiff": False},
        visit=str(os.environ.get("VISIT")),
    )
)
```
To list workflows:
```python
import asyncio
from python_workflow_submitter.list_workflows import list_workflows

asyncio.run(list_workflows(limit=5, filter="EXAMPLES"))
```
To create a helm template in your helm chart folder
```python 
import asyncio
from python_workflow_submitter.create_helm_yaml import create_helm_yaml

create_helm_yaml("notebook.yaml", "/workspaces/your_path/helm", "values/values.yaml")
```
To list workflows in specific visit with optional filtering:
```python
import asyncio
from python_workflow_submitter.list_workflows import list_workflows_in_visit

asyncio.run(list_workflows(limit=5,filter=filter: {
    "creator": "gmg29649",
    "template": "example-template",
  	"workflowStatusFilter": {"succeeded": True}
  }))

```

To list information about a workflow in a visit with a specific name:
```python
import asyncio
from python_workflow_submitter.list_workflows import list_workflows_in_visit

asyncio.run(info_about_workflow(name="conditional-steps-tswxm", visit="ks10000-3"))
```
