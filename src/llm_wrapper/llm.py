import torch
from typing import Any
from src.consts import SYSTEM_PROMPT
from src.models import MinimalSource
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    SentencePieceBackend, TokenizersBackend,
    BatchEncoding
)


class LLMWrapper():
    """
    LLMWrapper is a class that encapsulates a language model and its tokenizer
    for generating responses based on user prompts and contextual information.

    Attributes:
        tokenizer (TokenizersBackend | SentencePieceBackend): The tokenizer
        used for processing input text.
        model (Any): The language model used for generating responses.

    Methods:
        format_user_prompt(chunks: list[MinimalSource],
        user_prompt: str) -> str:
            Formats the user prompt by including context
            from the provided chunks.

        generation_pipeline(chunks: list[MinimalSource],
        user_prompt: str) -> str:
            Generates a response based on the user
            prompt and the provided context chunks.
    """

    def __init__(self) -> None:
        """
        Initializes the model and tokenizer for the Qwen3-0.6B.

        This constructor sets up the tokenizer and model using the
        pre-trained weights from the Qwen/Qwen3-0.6B repository.
        The tokenizer is initialized to handle input text, while
        the model is prepared for causal language modeling tasks.

        Attributes:
            tokenizer (TokenizersBackend | SentencePieceBackend):
                The tokenizer used for processing input text.
            model (Any):
                The causal language model loaded from the pre-trained weights.
        """

        self.tokenizer: TokenizersBackend | SentencePieceBackend = (
            AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
            )
        self.model: Any = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen3-0.6B"
            )

    def format_user_prompt(self, chunks: list[MinimalSource],
                           user_prompt: str) -> str:
        """
        Formats a user prompt by including context from a
        list of source chunks.

        Args:
            chunks (list[MinimalSource]): A list of source chunks
            containing file paths and content.
            user_prompt (str): The user's question or prompt.

        Returns:
            str: A formatted string that includes the context from the
            source chunks and the user's question.

        Notes:
            The function includes up to 4 source chunks in the formatted
            prompt. If no chunks are provided,
            it indicates that no documents were retrieved for the question.
        """

        formated_prompt: str = "Context:\n\n"
        for i, c in enumerate(chunks, start=1):
            if i == 5:
                break
            formated_prompt += f"Source {i}: {c.file_path}\n{c.content}\n\n"
        if not chunks:
            formated_prompt += ("No documents were retrieved "
                                "for this question.\n\n")
        return formated_prompt + f"Question: {user_prompt}"

    def generation_pipeline(self, chunks: list[MinimalSource],
                            user_prompt: str) -> str:
        """
        Generates a response based on the provided user prompt and
        chunks of minimal source data.

        Args:
            chunks (list[MinimalSource]): A list of minimal source object
            that provide context for the generation.
            user_prompt (str): The prompt provided by the user to guide
            the generation process.

        Returns:
            str: The generated response based on the user prompt and the
            provided chunks.

        Raises:
            AssertionError: If the tokenized prompt is not an instance of
            BatchEncoding.
        """

        tokenized_prompt = self.tokenizer.apply_chat_template(
            conversation=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": self.format_user_prompt(chunks, user_prompt)
                }
                ],
            add_generation_prompt=True,
            enable_thinking=False,
            sanitize_control_tokens=True,
            return_tensors="pt",
            return_dict=True
        )
        assert isinstance(tokenized_prompt, BatchEncoding)
        pl = len(tokenized_prompt['input_ids'][0])
        with torch.inference_mode():
            answer = self.model.generate(
                **tokenized_prompt,
                max_new_tokens=512,
                do_sample=False
                )
        decoded_answer = self.tokenizer.decode(
            answer[0][pl:],
            skip_special_tokens=True,
            )
        if isinstance(decoded_answer, str):
            return decoded_answer
        return decoded_answer[0]
