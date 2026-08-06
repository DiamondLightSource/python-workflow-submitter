import os
import subprocess


def lint_yaml(yaml_path: str):
    """Lints a given yaml file with argo lint --offline. If you are intending to lint a
    helm chart, please create it first via helm -s .

    Args:
        yaml_path (str): path to the yaml you intend to lint
        helm (bool): checker to determine if the yaml is a unconstructed helm template

    Returns:
        _type_: bool (True if no errors, False if errors)
    """
    if os.path.exists(yaml_path):
        try:
            subprocess.check_call(f"argo lint {yaml_path} --offline", shell=True)
        except subprocess.CalledProcessError:
            return False
        return True
    else:
        print(f"No file '{yaml_path}' found.")
        return False
