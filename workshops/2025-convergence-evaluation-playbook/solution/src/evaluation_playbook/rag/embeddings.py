from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from evaluation_playbook.config import settings

EmbeddingsModel = HuggingFaceEmbeddings | OpenAIEmbeddings


def get_embedding_model(
    model_id: str,
    device: str = "cpu",
) -> EmbeddingsModel:
    """Get an embedding model instance based on the model ID.

    Currently redirects to OpenAI embeddings, but can be extended to support
    different embedding model providers.

    Args:
        model_id (str): The identifier for the embedding model to use.
        device (str, optional): Computing device to run the model on ('cpu' or 'cuda').
            Defaults to "cpu".

    Returns:
        EmbeddingsModel: A configured embedding model instance (OpenAI or HuggingFace).
    """

    return get_openai_embedding_model(model_id, device)


def get_openai_embedding_model(model_id: str, device: str) -> OpenAIEmbeddings:
    """Get an OpenAI embedding model instance.

    Args:
        model_id (str): The identifier for the OpenAI embedding model.
        device (str): Computing device specification (not used for OpenAI models
            as they are API-based).

    Returns:
        OpenAIEmbeddings: A configured OpenAI embeddings model instance.

    Raises:
        AssertionError: If OPENAI_API_KEY is not set in the environment.
    """

    assert settings.OPENAI_API_KEY, (
        "OPENAI_API_KEY is not set. We need it to use the OpenAI embedding model."
    )

    return OpenAIEmbeddings(model=model_id, api_key=settings.OPENAI_API_KEY)


def get_huggingface_embedding_model(
    model_id: str, device: str
) -> HuggingFaceEmbeddings:
    """Get a HuggingFace embedding model instance.

    Args:
        model_id (str): The identifier for the HuggingFace embedding model.
        device (str): Computing device to run the model on ('cpu' or 'cuda').

    Returns:
        HuggingFaceEmbeddings: A configured HuggingFace embeddings model instance
            with remote code trust enabled and embedding normalization disabled.

    Note:
        The model is configured with trust_remote_code=True and normalize_embeddings=False
        for compatibility with most embedding models.
    """

    return HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs={"device": device, "trust_remote_code": True},
        encode_kwargs={"normalize_embeddings": False},
    )
