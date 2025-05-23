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

    philosopher_factory = PhilosopherFactory()
    philosopher = philosopher_factory.get_philosopher(x["philosopher_id"])

    input_messages = x["messages"][:-1]
    expected_output_message = x["messages"][-1]

    response, latest_state = await agent.call(
        messages=input_messages,
        philosopher_id=philosopher.id,
        new_thread=True,
    )
    context = state_to_str(latest_state)

    return {
        "input": input_messages,
        "context": context,
        "output": response,
        "expected_output": expected_output_message,
    }


def get_used_prompts() -> list[opik.Prompt]:
    client = opik.Opik()

    prompts = [
        client.get_prompt(name="odsc_evaluation_playbook_philosopher_character_card"),
    ]
    prompts = [p for p in prompts if p is not None]

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

    dataset = get_dataset(dataset_name)
    if not dataset:
        raise ValueError(f"Dataset with name `{dataset_name}` not found in Opik.")

    logger.info("Starting evaluation...")

    experiment_config = {
        "model_id": settings.OPENAI_MODEL,
        "dataset_name": dataset.name,
    }
    used_prompts = get_used_prompts()

    scoring_metrics = [
        Hallucination(),
        AnswerRelevance(),
        Moderation(),
        ContextRecall(),
        ContextPrecision(),
    ]

    logger.info("Evaluation details:")
    logger.info(f"Dataset: {dataset.name}")
    logger.info(f"Metrics: {[m.__class__.__name__ for m in scoring_metrics]}")

    evaluate(
        dataset=dataset,
        task=lambda x: asyncio.run(evaluation_task(x)),
        scoring_metrics=scoring_metrics,
        experiment_config=experiment_config,
        task_threads=workers,
        nb_samples=nb_samples,
        prompts=used_prompts,
    )
