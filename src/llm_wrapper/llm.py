import torch
from src.consts import SYSTEM_PROMPT
from src.models import MinimalSource
from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    SentencePieceBackend, TokenizersBackend,
)


class LLMWrapper():
    def __init__(self) -> None:
        self.tokenizer: TokenizersBackend | SentencePieceBackend = (
            AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
            )
        self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")

    def format_user_prompt(self, chunks: list[MinimalSource],
                           user_prompt: str) -> str:
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
