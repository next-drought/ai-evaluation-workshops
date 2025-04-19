import json
from pathlib import Path

import opik

from evaluation_playbook import opik_utils


def upload_dataset(
    name: str, data_path: Path, philosopher_ids: set[str] | None = None
) -> opik.Dataset:
    """Upload an evaluation dataset to Opik for monitoring and analysis.

    This function reads a JSON file containing evaluation data, optionally filters it
    by philosopher IDs, and creates a new Opik dataset. If a dataset with the same
    name exists, it will be deleted before creating the new one.

    Args:
        name (str): Name for the dataset in Opik.
        data_path (Path): Path to the JSON file containing evaluation data. The file
            should contain a "samples" key with a list of dictionaries, each having
            "philosopher_id" and "messages" fields.
        philosopher_ids (set[str] | None, optional): Set of philosopher IDs to filter
            the dataset. If provided, only samples for these philosophers will be included.
            Defaults to None, which includes all philosophers.

    Returns:
        opik.Dataset: The newly created and populated dataset in Opik.

    Raises:
        AssertionError: If the specified data_path does not exist.
        json.JSONDecodeError: If the data file is not valid JSON.

    Example:
        >>> dataset = upload_dataset(
        ...     name="philosopher_eval_v1",
        ...     data_path=Path("data/evaluation_dataset.json"),
        ...     philosopher_ids={"plato", "aristotle"}
        ... )
    """

    assert data_path.exists(), f"File {data_path} does not exist."

    with open(data_path, "r") as f:
        evaluation_data = json.load(f)

    if philosopher_ids:
        evaluation_data["samples"] = [
            sample
            for sample in evaluation_data["samples"]
            if sample["philosopher_id"] in philosopher_ids
        ]

    dataset_items = []
    for sample in evaluation_data["samples"]:
        dataset_items.append(
            {
                "philosopher_id": sample["philosopher_id"],
                "messages": sample["messages"],
            }
        )

    dataset = opik_utils.create_dataset(
        name=name,
        description="Dataset containing question-answer pairs for multiple philosophers.",
        items=dataset_items,
    )

    return dataset
