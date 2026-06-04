"""
config_loader.py

Objective:
Load Gold Layer configuration settings
from gold_config.yaml.

Project:
Olist Seller Intelligence Platform

Layer:
Gold Utilities
"""

import yaml
import os


def load_config():

    config_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../configs/gold_config.yaml"
        )
    )

    with open(
        config_path,
        "r"
    ) as file:

        config = yaml.safe_load(
            file
        )

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