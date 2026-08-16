"""Módulo de exemplo para testar chunking."""
import os
import json
from typing import Optional
from pathlib import Path


CONSTANT_VALUE = 42


def small_function(x: int) -> int:
    """Função pequena, deve caber num único chunk."""
    return x + 1


def medium_function(items: list[int]) -> dict[str, int]:
    """Função de tamanho médio."""
    result = {}
    for i, item in enumerate(items):
        key = f"item_{i}"
        result[key] = item * 2
    return result


def large_function(n: int) -> list[int]:
    """Função grande, deve forçar split se max_chunk_size for pequeno."""
    values = []
    for i in range(n):
        v = i * i
        v = v + CONSTANT_VALUE
        v = v - 1
        v = v // 2
        values.append(v)
        if v % 2 == 0:
            values.append(v * 2)
        else:
            values.append(v * 3)
    total = sum(values)
    average = total / len(values) if values else 0
    return values


class Processor:
    """Classe de exemplo com múltiplos métodos."""

    def __init__(self, name: str, config: Optional[dict] = None):
        self.name = name
        self.config = config or {}

    def process(self, data: list[int]) -> list[int]:
        """Processa uma lista de inteiros."""
        return [x * 2 for x in data]

    def save(self, path: str, data: dict) -> None:
        """Salva dados em disco como JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(path: str) -> dict:
        """Carrega dados de um arquivo JSON."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


class EmptyClass:
    """Classe sem corpo relevante além de pass."""
    pass


async def async_function(url: str) -> str:
    """Função assíncrona de exemplo."""
    return f"fetched: {url}"


if __name__ == "__main__":
    p = Processor("demo")
    print(p.process([1, 2, 3]))
    print(os.getcwd())
    print(Path(".").resolve())