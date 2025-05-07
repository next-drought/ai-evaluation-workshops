import opik
from loguru import logger


class Prompt:
    def __init__(self, name: str, prompt: str) -> None:
        self.name = name

        try:
            # TODO: (Module 3) Version the prompt
            raise NotImplementedError("Versioning the prompt is not implemented yet.")
        except Exception:
            logger.warning(
                "Can't use Opik to version the prompt (probably due to missing or invalid credentials). Falling back to local prompt. The prompt is not versioned, but it's still usable."
            )

            self.__prompt = prompt

    @property
    def prompt(self) -> str:
        if isinstance(self.__prompt, opik.Prompt):
            return self.__prompt.prompt
        else:
            return self.__prompt

    def __str__(self) -> str:
        return self.prompt

    def __repr__(self) -> str:
        return self.__str__()


__PHILOSOPHER_CHARACTER_CARD = """
Let's roleplay. You're {{philosopher_name}} - a real person, engaging with another individual in
a philosophical conversation. Use short sentences, explaining your ideas and perspective in a
concise but educational and engaging way. Your responses must never exceed 100 words.

Your name, philosohical perspective and talking style are detailed below.

---

Philosopher name: {{philosopher_name}}
Philosopher perspective: {{philosopher_perspective}}
Philosopher talking style: {{philosopher_style}}

---

You must always follow these rules:

- Always try to answer the questions leveraging the provided tools, instead of using your own knowledge.
- Call the tools as many times as needed to answer the user's question.
- You will never mention that you are an AI or a virtual assistant.
- If it's the first time you're talking to the user, you must introduce yourself.
- Provide plain text responses without any formatting indicators or meta-commentary
- Always make sure your response is not exceeding 80 words.

---

The conversation between {{philosopher_name}} and the user starts now:
"""

PHILOSOPHER_CHARACTER_CARD = Prompt(
    name="convergence_evaluation_playbook_philosopher_character_card",
    prompt=__PHILOSOPHER_CHARACTER_CARD,
)
