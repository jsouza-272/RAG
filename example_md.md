# Header1
Texto do primeiro bloco.
Mais uma linha aqui.
Ainda mais uma linha para dar tamanho a este bloco.

## Header2
Texto do segundo bloco.
Continuação do segundo bloco com mais conteúdo.

### Header3
Subseção pequena.

## Header4
Bloco de código abaixo, com um comentário dentro
para testar se o regex de header não confunde com "#".

```python
# Isto é um comentário dentro de um bloco de código
def foo():
    return 1


def bar():
    return 2
```

Texto depois do código.

# Header5
Seção grande para testar force-split quando max_chunk_size for pequeno.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.

## Header6
Última subseção antes do fim.

#### Header7
Header de nível profundo (h4), pequeno conteúdo.

# Header8
Última seção do arquivo, sem conteúdo abaixo além desta linha.
