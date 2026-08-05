[![CI](https://github.com/Matt-Carre/python-workflow-submitter/actions/workflows/ci.yml/badge.svg)](https://github.com/Matt-Carre/python-workflow-submitter/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/Matt-Carre/python-workflow-submitter/branch/main/graph/badge.svg)](https://codecov.io/gh/Matt-Carre/python-workflow-submitter)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
# python_workflow_submitter

 Python alternative to creating and running argo workflows in the Data Analysis Platform

This allows for the submission of Hera workflow objects to Diamond's GraphQL API.

What            | Where
:---:           | :---:
Source          | <https://github.com/Matt-Carre/python-workflow-submitter>
Docker          | `docker run ghcr.io/Matt-Carre/python-workflow-submitter:latest`
Releases        | <https://github.com/Matt-Carre/python-workflow-submitter/releases>

To submit your workflow notebook:
Notably, this requires a .env file in your source folder with the following parameters:
HOST=https://workflows.diamond.ac.uk/graphql
VISIT=
EXPIRY=
AUTH=
TOKEN=


```python
from python_workflow_submitter.submit_workflow import submit_workflow

await submit_workflow(w)
```
To submit a workflow script:
```python 
import asyncio
from python_workflow_submitter.submit_workflow import submit_workflow

asyncio.run(submit_workflow(w))
```

To submit a generic workflow via a graphql mutation in a notebook:

```python
import os
from python_workflow_submitter.submit_workflow import submit_stock_workflow

await submit_stock_workflow(
        "example-template",
        {"png": "True", "jpg": "False", "jpeg": "True", "tif": "True", "tiff": "False"},
        host= str(os.environ.get("HOST")),
        visit= str(os.environ.get("VISIT")),
    )
```
Alternatively:
```python 
import asyncio
from python_workflow_submitter.submit_workflow import submit_workflow

asyncio.run(submit_stock_workflow(
        "example-template",
        {"png": "True", "jpg": "False", "jpeg": "True", "tif": "True", "tiff": "False"},
        host= str(os.environ.get("HOST")),
        visit= str(os.environ.get("VISIT")),
    ))

To list workflows:
```python
import asyncio
from python_workflow_submitter.list_workflows import list_workflows

asyncio.run(list_workflows(limit=5,filter={"scienceGroup":"EXAMPLES"}))

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

asyncio.run(info_about_workflow(name="conditional-steps-tswxm",visit=ks10000-3))
```
