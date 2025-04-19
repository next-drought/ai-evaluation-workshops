from pathlib import Path

import click
from loguru import logger

from evaluation_playbook.config import settings
from evaluation_playbook.evaluation import upload_dataset


@click.command()
@click.option(
    "--dataset-name",
    default="philoagents_evaluation_dataset",
    help="Name of the dataset",
)
@click.option(
    "--data-path",
    type=click.Path(exists=True, path_type=Path),
    default=settings.EVALUATION_DATASET_FILE_PATH,
    help="Path to the dataset file",
)
def main(dataset_name: str, data_path: Path) -> None:
    """Upload a dataset to the evaluation system.

    This function uploads a dataset to be used for evaluating philosophical agents.

    Args:
        dataset_name: Name of the dataset to be uploaded.
        data_path: Path to the dataset file containing evaluation data.

    Returns:
        None
    """

    upload_dataset(
        name=dataset_name,
        data_path=data_path,
        philosopher_ids={"plato", "aristotle", "turing"},
    )

    logger.info(f"Dataset `{dataset_name}` uploaded successfully")


if __name__ == "__main__":
    main()
