Com o Call_me_Maybe você já deve ter familiaridade com function calling, prompting e possivelmente APIs de LLM. Pra esse projeto o foco muda pra retrieval + geração fundamentada em contexto. Prioridades de estudo:

1. Fundamentos de RAG (essencial)
Pipeline completo: indexing → retrieval → augmenting → generating
Diferença entre RAG e fine-tuning (por que não retreinar)
Trade-offs: quando confiar na base retrievada vs. conhecimento interno do modelo (risco de alucinação)
2. Retrieval — o coração do projeto
TF-IDF: term frequency / inverse document frequency, como funciona o scoring
BM25: evolução do TF-IDF, parâmetros k1 e b, por que costuma performar melhor
Bibliotecas: bm25s (recomendada no subject), ou sklearn.feature_extraction.text.TfidfVectorizer
Similaridade de vetores (cosine similarity) se for além do básico
3. Chunking
Estratégias diferentes pra código Python vs. Markdown (ex: dividir por função/classe no código, por seção/header no markdown)
Trade-off tamanho do chunk vs. precisão do retrieval (chunk grande = mais contexto mas menos preciso; pequeno = mais preciso mas pode perder contexto)
Overlap entre chunks (janela deslizante)
4. LLM local / inferência
Como carregar e rodar Qwen/Qwen3-0.6B localmente (via transformers ou vllm)
Gerenciamento de context window / limite de tokens
Prompt engineering pra respostas "grounded" (instruir o modelo a só usar o contexto fornecido, citar fonte, não inventar)
5. Avaliação de sistemas de retrieval
Métrica recall@k — o que mede, como calcular
Ground truth vs. predições, overlap de spans de texto (índices de caractere)
6. Ferramentas / boas práticas (você já deve saber da CC, mas reforça aqui)
pydantic (validação de modelos, BaseModel, Field)
Python Fire (gera CLI automaticamente a partir de funções/classes)
uv (gerenciador de projeto/dependências, se ainda não usou)
mypy com flags estritas + flake8
Ordem sugerida de estudo
RAG conceitual (30min de leitura, você já tem a base do Foreword do subject)
BM25/TF-IDF na prática — implementar um retrieval simples num dataset de teste
Chunking — testar estratégias diferentes e ver impacto no recall
Rodar o Qwen3-0.6B localmente, testar geração com contexto
Métricas de avaliação — implementar recall@k

Quer que eu aprofunde algum desses pontos (ex: como o BM25 calcula score, ou exemplos de chunking pra código Python)?

# Parser
-	 cli input usando fire

## Comandos e flags

- index: Index the repository
- search: Search for a single query
- search_dataset: Process multiple questions and output search results
- answer: Answer a single question with context
- answer_dataset: Generate answers from search results
- evaluate: Evaluate search results against ground truth