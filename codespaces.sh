#!/usr/bin/env bash
# Rode no terminal do Codespace, na raiz do repositorio:  bash codespaces.sh
set -e
pip install pytest==9.1.1 pytest-cov==7.1.0 mutmut==3.8.0

for ex in ex1 ex2 ex3; do
  echo "================ $ex ================"
  cd "$ex"
  python -m pytest -q --cov=src --cov-branch --cov-report=term-missing
  rm -rf mutants
  mutmut run || true
  mutmut results          # lista apenas os mutantes que sobreviveram
  cd ..
done
echo
echo "Para ver o diff de um mutante vivo:  cd exN && mutmut show <nome>"
