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
