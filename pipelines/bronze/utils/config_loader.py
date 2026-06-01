import yaml
import os


def load_config():

    config_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../configs/bronze_config.yaml"
        )
    )

    with open(config_path, "r") as file:

        config = yaml.safe_load(file)

    return config