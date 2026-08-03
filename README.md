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

```python
from python_workflow_submitter.submit_workflow import submit_workflow

await submit_workflow(w)
```
