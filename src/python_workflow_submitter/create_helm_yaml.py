import os
import subprocess


def create_helm_yaml(
    yaml_name: str,
    chart_dir: str,
    values_dir: str | None = None,
):
    """Creates a yaml file in chart_dir named post_helm_{yaml_name}.

    Args:
        yaml_name (str): The name of the file within the helm templates folder you wish
        to convert into a post-helm yaml.
        chart_dir (str): The directory containing the helm chart.yaml
        values_dir (str | None, optional): The directory or file containing
        values.yaml, or another file to obtain values from. Defaults to None.

    Raises:
        FileExistsError: If the path to yaml_name cannot be found, or to the valuesdir
        cannot be found, we raise this.
    """
    if os.path.exists(f"{chart_dir}/templates/{yaml_name}"):
        if not values_dir and os.path.exists(f"{chart_dir}/values.yaml"):
            valuepath = f" -f {values_dir}/values.yaml"
            yamlstr = subprocess.run(
                f"helm template . -s templates/{yaml_name} {valuepath}",
                cwd=chart_dir,
                shell=True,
                capture_output=True,
                text=True,
            )
        elif values_dir and os.path.exists(f"{chart_dir}/{values_dir}"):
            valuepath = f" -f {values_dir}"
            yamlstr = subprocess.run(
                f"helm template . -s templates/{yaml_name} {valuepath}",
                cwd=chart_dir,
                shell=True,
                capture_output=True,
                text=True,
            )
        elif values_dir is None:
            yamlstr = subprocess.run(
                f"helm template . -s templates/{yaml_name}",
                cwd=chart_dir,
                shell=True,
                capture_output=True,
                text=True,
            )
        else:
            raise FileExistsError
        with open(f"{chart_dir}/post_helm_{yaml_name}", "w") as phy:
            phy.write(yamlstr.stdout)
    else:
        raise FileExistsError
