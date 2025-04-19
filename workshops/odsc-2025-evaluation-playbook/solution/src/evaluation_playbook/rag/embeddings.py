from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from evaluation_playbook.config import settings


EmbeddingsModel = HuggingFaceEmbeddings | OpenAIEmbeddings


def get_embedding_model(
    model_id: str,
    device: str = "cpu",
) -> EmbeddingsModel:
    """Gets an instance of a HuggingFace embedding model.

    Args:
        model_id (str): The ID/name of the HuggingFace embedding model to use
        device (str): The compute device to run the model on (e.g. "cpu", "cuda").
            Defaults to "cpu"

    Returns:
        EmbeddingsModel: A configured HuggingFace embeddings model instance
    """
    return get_openai_embedding_model(model_id, device)


def get_openai_embedding_model(model_id: str, device: str) -> OpenAIEmbeddings:
    """Gets an instance of an OpenAI embedding model."""

    assert settings.OPENAI_API_KEY, (
        "OPENAI_API_KEY is not set. We need it to use the OpenAI embedding model."
    )

    return OpenAIEmbeddings(model=model_id, api_key=settings.OPENAI_API_KEY)


def get_huggingface_embedding_model(
    model_id: str, device: str
) -> HuggingFaceEmbeddings:
    """Gets a HuggingFace embedding model instance.

    Args:
        model_id (str): The ID/name of the HuggingFace embedding model to use
        device (str): The compute device to run the model on (e.g. "cpu", "cuda")

    Returns:
        HuggingFaceEmbeddings: A configured HuggingFace embeddings model instance
            with remote code trust enabled and embedding normalization disabled
    """
    return HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs={"device": device, "trust_remote_code": True},
        encode_kwargs={"normalize_embeddings": False},
    )
