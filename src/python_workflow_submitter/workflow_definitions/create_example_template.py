import json
import os

from hera.shared import global_config
from hera.workflows import (
    DAG,
    Artifact,
    Parameter,
    Script,
    Volume,
    Workflow,
    script,  # pyright: ignore[reportUnknownVariableType]
)
from hera.workflows import models as m
from hera.workflows.archive import NoneArchiveStrategy

global_config.set_class_defaults(  # pyright: ignore
    Script, image=str(os.environ.get("DEFAULT_IMAGE"))
)


@script(
    command=["python"],
    outputs=Parameter(
        name="out-parameters", value_from=m.ValueFrom(path="/tmp/parameters.json")
    ),
    volume_mounts=[m.VolumeMount(name="tmpdir", mount_path="/tmp")],
)
def generate_parameters(
    png: str,
    jpg: str,
    jpeg: str,
    tif: str,
    tiff: str,
):
    import json

    params: list[dict[str, int | list[int] | str] | None] = [
        {"width": 500, "height": 500, "weights": [255, 1, 100], "extension": "png"}
        if png.lower() == "true"
        else None,
        {"width": 600, "height": 200, "weights": [100, 150, 100], "extension": "jpg"}
        if jpg.lower() == "true"
        else None,
        {"width": 300, "height": 400, "weights": [100, 150, 100], "extension": "jpeg"}
        if jpeg.lower() == "true"
        else None,
        {"width": 300, "height": 200, "weights": [230, 100, 1], "extension": "tif"}
        if tif.lower() == "true"
        else None,
        {"width": 200, "height": 300, "weights": [230, 100, 1], "extension": "tiff"}
        if tiff.lower() == "true"
        else None,
    ]
    params_to_write: list[dict[str, int | list[int] | str]] = [
        image_params for image_params in params if image_params is not None
    ]
    with open("/tmp/parameters.json", "w") as f:
        json.dump(params_to_write, f)


@script(
    command=["python"],
    volume_mounts=[m.VolumeMount(name="tmpdir", mount_path="/tmp")],
    outputs=[
        Parameter(
            name="out-paths",
            value_from=m.ValueFrom(
                path="/tmp/{{inputs.parameters.extension}}-path.json"
            ),
        ),
        Artifact(
            name="{{inputs.parameters.extension}}-image",
            path="/tmp/{{inputs.parameters.extension}}-image.{{inputs.parameters.extension}}",
            archive=NoneArchiveStrategy(),
        ),
    ],
)
def create_image(
    width: int, height: int, weights: tuple[int, int, int], extension: str
):
    import json

    from PIL import Image

    def create_pattern(
        width: int,
        height: int,
        weights: tuple[int, int, int],
    ) -> Image.Image:
        print(f"width: {width}")
        print(f"height: {height}")
        print(f"RBG weights: {weights}")
        image = Image.new("RGB", (width, height))
        pixels = image.load()
        for i in range(width):
            for j in range(height):
                pixels[i, j] = (  # pyright: ignore[reportOptionalSubscript]
                    (i + j * 50) % weights[0],
                    weights[1],
                    (i * 300 + j) % weights[2],
                )
        return image

    image = create_pattern(width, height, weights)
    path = f"/tmp/{extension}-image.{extension}"
    image.save(path)
    with open(f"/tmp/{extension}-path.json", "w") as f:
        json.dump(path, f)


@script(
    command=["python"],
    volume_mounts=[m.VolumeMount(name="tmpdir", mount_path="/tmp")],
    outputs=Artifact(
        name="hdf5output",
        path="/tmp/images.hdf5",
        archive=NoneArchiveStrategy(),
    ),
)
def to_hdf5(paths: str):

    import h5py  # pyright: ignore[reportMissingTypeStubs]
    import numpy as np
    from PIL import Image

    print("creating hdf5 file")
    with h5py.File("/tmp/images.hdf5", "w") as f:
        for i, path in enumerate(paths):
            path = path.strip('"')
            print(f"Got {path}")
            with Image.open(path) as image:
                arr = np.array(image)
                f.create_dataset(  # pyright: ignore[reportUnknownMemberType]
                    f"image_{i}", data=arr, dtype=arr.dtype
                )
    print("done")


with Workflow(
    pod_spec_patch=json.dumps(
        {
            "containers": [
                {
                    "name": "main",
                    "resources": {
                        "limits": {
                            "cpu": "1",
                            "memory": "1Gi",
                        },
                        "requests": {
                            "cpu": "1",
                            "memory": "1Gi",
                        },
                    },
                }
            ]
        }
    ),
    tolerations=[
        m.Toleration(
            key="nodetype", operator="Equal", value="gpu", effect="NoSchedule"
        ),
        m.Toleration(
            key="nodegroup", operator="Equal", value="workflows", effect="NoSchedule"
        ),
    ],
    name="hera-example",
    entrypoint="workflowentry",
    api_version="argoproj.io/v1alpha1",
    kind="WorkflowTemplate",
    labels={"workflows.diamond.ac.uk/science-group-examples": "true"},
    annotations={
        "workflows.argoproj.io/title": "example remade via hera",
        "workflows.argoproj.io/description": """Replicates the functionality of
example.yaml""",
        "workflows.diamond.ac.uk/repository": "https://github.com/Matt-Carre/python-workflow-submitter",
    },
    volumes=Volume(name="tmpdir", mount_path="/tmp/", size="1Gi"),
) as w:
    with DAG(name="workflowentry"):
        params = generate_parameters(
            name="params",
            arguments={
                "png": "True",
                "jpg": "True",
                "jpeg": "True",
                "tif": "True",
                "tiff": "True",
            },
        )
        makeimages = create_image(with_param=params.get_parameter("out-parameters"))
        makehdf5 = to_hdf5(
            arguments={
                "paths": makeimages.get_parameter("out-paths"),
            }
        )
        params >> makeimages >> makehdf5  # pyright: ignore


with open("src/python_workflow_submitter/templates/example.txt", "w") as div:
    div.write(w.to_yaml())  # pyright: ignore[reportUnknownMemberType]
