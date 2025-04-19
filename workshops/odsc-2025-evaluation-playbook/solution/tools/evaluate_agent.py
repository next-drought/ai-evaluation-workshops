from pathlib import Path

import click
from loguru import logger

from evaluation_playbook.evaluation import evaluate_agent
from evaluation_playbook.config import settings


@click.command()
@click.option(
    "--dataset-name",
    default="philoagents_evaluation_dataset",
    help="Name of the dataset",
)
@click.option("--workers", default=1, type=int, help="Number of workers")
@click.option(
    "--nb-samples", default=20, type=int, help="Number of samples to evaluate"
)
def main(dataset_name: str, workers: int, nb_samples: int) -> None:
    """Evaluate an agent on a dataset.

    This function runs the evaluation of an agent against a specified dataset using
    the configured number of workers and samples.

    Args:
        dataset_name (str): Name of the dataset to evaluate against.
        workers (int): Number of parallel workers to use for evaluation.
        nb_samples (int): Number of samples to evaluate from the dataset.

    Returns:
        None
    """

    evaluate_agent(dataset_name=dataset_name, workers=workers, nb_samples=nb_samples)

    logger.info(f"Evaluation completed for dataset `{dataset_name}`")


if __name__ == "__main__":
    main()
