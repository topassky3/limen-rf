#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
else
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  bibtex main
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
fi

echo "Built: $(pwd)/main.pdf"
