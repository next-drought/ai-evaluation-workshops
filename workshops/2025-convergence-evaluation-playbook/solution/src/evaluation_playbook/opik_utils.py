import os

import opik
from loguru import logger
from opik.configurator.configure import OpikConfigurator

from evaluation_playbook.config import settings


def configure() -> None:
    """Configure Opik monitoring with API key and project settings.

    This function sets up Opik monitoring using the configured API key and project name.
    If the configuration fails or required settings are missing, warning messages are logged.

    Raises:
        Exception: If there are issues with the Opik server connection or configuration.
    """

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
    """Retrieve an Opik dataset by name.

    Args:
        name (str): The name of the dataset to retrieve.

    Returns:
        opik.Dataset | None: The requested dataset if found, None otherwise.
    """
    client = opik.Opik()
    try:
        dataset = client.get_dataset(name=name)
    except Exception:
        dataset = None

    return dataset


def create_dataset(name: str, description: str, items: list[dict]) -> opik.Dataset:
    """Create a new Opik dataset with the given items.

    If a dataset with the same name exists, it will be deleted before creating
    the new one.

    Args:
        name (str): Name for the new dataset.
        description (str): Description of the dataset.
        items (list[dict]): List of items to insert into the dataset.

    Returns:
        opik.Dataset: The newly created and populated dataset.
    """

    client = opik.Opik()

    dataset = client.create_dataset(name=name, description=description)
    dataset.insert(items)

    return dataset
