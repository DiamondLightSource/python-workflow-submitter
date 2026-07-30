# Setting up a development environment
1. run "uv lock" to generate the uv.lock file
2. Create .env in this folder (with the path src/.env) containing the following variables:

HOST=https://workflows.diamond.ac.uk/graphql (to submit to the production cluster)
DEFAULT_IMAGE= (usually python 3.10)
VISIT= (the Visit you wish to run the template on)
TOKEN=
EXPIRY=
AUTH=

3. Build the dev container

# Submitting a workflow
1. At the start of your workflow definition file, add:

```python
from python_workflow_submitter.submit_to_graphql import submit_workflow
```

2. At the end of a workflow definition file, once your workflow (w) is created, add:
```python
submit_workflow(w)
```

NOTE: Be sure to remove this line upon commiting changes, as all workflow definition files are 
by default, ran on pre-commit, to ensure that any yaml files they create are up to date.

# Building a custom image
While in src, the same folder as a Dockerfile:

podman build -t ghcr.io/Your-Github-Name/image-name .
podman login ghcr.io
podman push ghcr.io/Your-Github-Name/image-name

Then go to your github profile, packages, and set image-name's visibility to public
After this, you may add 'image' in the script decorator, to run specific scripts within that image
Alternatively, you can set the default image at the top of the file by adding:

```python
global_config.set_class_defaults(  # pyright: ignore
    Script, image=str(os.environ.get("DEFAULT_IMAGE"))
)
```
