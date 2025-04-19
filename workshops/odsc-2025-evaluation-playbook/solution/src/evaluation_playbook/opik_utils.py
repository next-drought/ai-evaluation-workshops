import os

import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator

from evaluation_playbook.config import settings


def configure() -> None:
    if settings.OPIK_API_KEY and settings.OPIK_PROJECT:
        try:
            client = OpikConfigurator(api_key=settings.OPIK_API_KEY.get_secret_value())
            default_workspace = client._get_default_workspace()
        except Exception:
            logger.warning(
                "Default workspace not found. Setting workspace to None and enabling interactive mode."
            )
            default_workspace = None

        os.environ["OPIK_PROJECT_NAME"] = settings.OPIK_PROJECT

        try:
            opik.configure(
                api_key=settings.OPIK_API_KEY.get_secret_value(),
                workspace=default_workspace,
                use_local=False,
                force=True,
            )
            logger.info(
                f"Opik configured successfully using workspace '{default_workspace}'"
            )
        except Exception:
            logger.warning(
                "Couldn't configure Opik. There is probably a problem with the OPIK_API_KEY or OPIK_PROJECT environment variables or with the Opik server."
            )
    else:
        logger.warning(
            "OPIK_API_KEY and OPIK_PROJECT are not set. Set them to enable prompt monitoring with Opik."
        )


def get_dataset(name: str) -> opik.Dataset | None:
    client = opik.Opik()
    try:
        dataset = client.get_dataset(name=name)
    except Exception:
        dataset = None

    return dataset


def create_dataset(name: str, description: str, items: list[dict]) -> opik.Dataset:
    client = opik.Opik()

    client.delete_dataset(name=name)

    dataset = client.create_dataset(name=name, description=description)
    dataset.insert(items)

    return dataset
