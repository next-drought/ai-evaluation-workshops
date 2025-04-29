import asyncio

import opik
from loguru import logger
from opik.evaluation import evaluate
from opik.evaluation.metrics import (
    AnswerRelevance,
    ContextPrecision,
    ContextRecall,
    Hallucination,
    Moderation,
)

from evaluation_playbook.config import settings
from evaluation_playbook.domain.philosopher_factory import PhilosopherFactory
from evaluation_playbook.opik_utils import get_dataset
from evaluation_playbook.workflow import agent
from evaluation_playbook.workflow.state import state_to_str


async def evaluation_task(x: dict) -> dict:
    """Calls agentic app logic to evaluate philosopher responses.

    Args:
        x: Dictionary containing evaluation data with the following keys:
            messages: List of conversation messages where all but the last are inputs
                and the last is the expected output
            philosopher_id: ID of the philosopher to use

    Returns:
        dict: Dictionary with evaluation results containing:
            input: Original input messages
            context: Context used for generating the response
            output: Generated response from philosopher
            expected_output: Expected answer for comparison
    """

    # TODO: (Module 2 & 3) Call the agent on the input messages and return the response and context

    return {
        "input": input_messages,
        "context": context,
        "output": response,
        "expected_output": expected_output_message,
    }


def get_used_prompts() -> list[opik.Prompt]:
    # TODO: (Module 3) Get the used prompts to hook them to the experiment in Opik

    return prompts


def evaluate_agent(
    dataset_name: str,
    workers: int = 2,
    nb_samples: int | None = None,
) -> None:
    """Evaluates an agent using specified metrics and dataset.

    Runs evaluation using Opik framework with configured metrics for hallucination,
    answer relevance, moderation, and context recall.

    Args:
        dataset: Dataset containing evaluation examples.
            Must contain messages and philosopher_id.
        workers: Number of parallel workers to use for evaluation.
            Defaults to 2.
        nb_samples: Optional number of samples to evaluate.
            If None, evaluates the entire dataset.

    Raises:
        ValueError: If dataset is None
        AssertionError: If COMET_API_KEY is not set

    Returns:
        None
    """

    assert settings.OPIK_API_KEY, (
        "OPIK_API_KEY is not set. We need it to track the experiment with Opik."
    )

    # TODO: (Module 2 & 3) Get the evaluationdataset

    logger.info("Starting evaluation...")

    # TODO: (Module 2 & 3) Prepare metadata
    

    # TODO: (Module 2 & 3) Configure scoring metrics
   
    logger.info("Evaluation details:")
    logger.info(f"Dataset: {dataset.name}")
    logger.info(f"Metrics: {[m.__class__.__name__ for m in scoring_metrics]}")

    # TODO: (Module 2 & 3) Run the evaluation
