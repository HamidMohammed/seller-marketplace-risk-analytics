# =========================================================
# CONFIG LOADER UTILITY
# =========================================================

import yaml
import os


def load_config():

    """
    Load Silver layer YAML configuration file.
    """

    # Resolve project root dynamically
    current_dir = os.path.dirname(__file__)

    project_root = os.path.abspath(
        os.path.join(current_dir, "../../../")
    )

    # Build config path
    config_path = os.path.join(
        project_root,
        "pipelines",
        "silver",
        "configs",
        "silver_config.yaml"
    )

    # Load YAML config
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config

def resolve_path(path: str, config):

    environment = config["environment"]

    if environment == "local":
        return path

    if environment == "minio":

        path = path.replace(
            "data/bronze/",
            "s3a://bronze/"
        )

        path = path.replace(
            "data/silver/",
            "s3a://silver/"
        )

        path = path.replace(
            "data/gold/",
            "s3a://gold/"
        )

        return path

    raise ValueError(
        f"Unsupported environment: {environment}"
    )