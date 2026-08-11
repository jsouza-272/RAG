#!/bin/bash
# Testa a validação de todos os comandos do CLI via `make run`
# Uso: ./test_validator.sh

clear

set -u

PASS=0
FAIL=0

run_test() {
    local desc="$1"
    local expect="$2"   # "ok" ou "fail"
    shift 2
    local args="$*"

    output=$(make run ARGS="$args" 2>&1)
    status=$?

    if [ "$expect" = "ok" ] && [ $status -eq 0 ]; then
        echo "[PASS] $desc"
        PASS=$((PASS+1))
    elif [ "$expect" = "fail" ] && [ $status -ne 0 ]; then
        echo "[PASS] $desc"
        PASS=$((PASS+1))
    else
        echo "[FAIL] $desc (esperado=$expect, status=$status)"
        echo "       output: $output"
        FAIL=$((FAIL+1))
    fi
}

echo "== index =="
run_test "max_chunk_size válido"                 ok   index --max_chunk_size=2000
run_test "max_chunk_size default"                ok   index
run_test "max_chunk_size negativo"               fail index --max_chunk_size=-500
run_test "max_chunk_size zero"                   fail index --max_chunk_size=0
run_test "max_chunk_size string"                 fail index --max_chunk_size=abc
run_test "max_chunk_size float"                  fail index --max_chunk_size=200.5
run_test "max_chunk_size vazio"                  fail index --max_chunk_size=

#echo ""
#echo "== search =="
#run_test "query e k válidos"                     ok   search --query="What is PagedAttention?" --k=5
#run_test "query vazia"                           fail search --query="" --k=5
#run_test "sem query"                             fail search --k=5
#run_test "k negativo"                            fail search --query="test" --k=-1
#run_test "k zero"                                fail search --query="test" --k=0
#run_test "k string"                              fail search --query="test" --k=abc
#run_test "k float"                               fail search --query="test" --k=2.5

echo ""
echo "== search_dataset =="
run_test "args válidos"                          ok   search_dataset --dataset_path=datasets_public/public/AnsweredQuestions/dataset_docs_public.json --k=10 --save_directory=data/output
run_test "dataset_path inexistente"              fail search_dataset --dataset_path=data/nao_existe.json --k=10 --save_directory=data/output
run_test "sem dataset_path"                      fail search_dataset --k=10 --save_directory=data/output
run_test "k inválido"                            fail search_dataset --dataset_path=data/dataset_docs_public.json --k=0 --save_directory=data/output
run_test "save_directory vazio"                  fail search_dataset --dataset_path=data/dataset_docs_public.json --k=10 --save_directory=

echo ""
echo "== answer =="
run_test "query e k válidos"                     ok   answer "'How to configure OpenAI server?'" --k=10
run_test "query vazia"                           fail answer "" --k=10
run_test "k negativo"                            fail answer "test" --k=-3
run_test "k float"                            	 fail answer "test" --k=3.5

echo ""
echo "== answer_dataset =="
run_test "args válidos"                          ok   answer_dataset --student_search_results_path=datasets_public/public/AnsweredQuestions/dataset_docs_public.json --save_directory=data/output/answers
run_test "path inexistente"                      fail answer_dataset --student_search_results_path=data/nao_existe.json --save_directory=data/output/answers
run_test "sem save_directory"                    fail answer_dataset --student_search_results_path=data/output/search_results.json

#echo ""
#echo "== evaluate =="
#run_test "args válidos"                          ok   evaluate --student_answer_path=data/output/search_results.json --dataset_path=data/dataset_answered.json --k=10 --max_context_length=2000
#run_test "student_answer_path inexistente"       fail evaluate --student_answer_path=data/nao_existe.json --dataset_path=data/dataset_answered.json --k=10 --max_context_length=2000
#run_test "k negativo"                            fail evaluate --student_answer_path=data/output/search_results.json --dataset_path=data/dataset_answered.json --k=-1 --max_context_length=2000
#run_test "max_context_length negativo"           fail evaluate --student_answer_path=data/output/search_results.json --dataset_path=data/dataset_answered.json --k=10 --max_context_length=-100

echo ""
echo "== Resultado: $PASS passou, $FAIL falhou =="

[ $FAIL -eq 0 ]