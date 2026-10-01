# REDIN manuscript build

This directory contains the journal-format wrappers for LIMEN-RF. The scientific source of truth remains:

- `paper/sections/*.tex`
- `paper/references.bib`
- frozen result artifacts under `results/`

Do not independently edit scientific claims in multiple wrappers.

## Manuscript wrappers

- `article.tex` — **identified** version. It contains Juan Felipe Orozco Cortés as author and points the data-availability statement to the public repository.
- `article_identified.tex` — synchronized identified alias kept for convenience.
- `article_blind.tex` — **double-blind reviewer** version. Author identity, affiliation, email, named contribution line, and repository URL are withheld.

The reviewer manuscript being anonymous does not make a public GitHub repository itself anonymous. If strict reviewer blinding is required, repository visibility/timing must be handled separately from the manuscript source.

## Official template support files

The journal's `redina.cls`, `lineno.sty`, and logo assets are not redistributed by this repository. Download the official REDIN LaTeX template from the journal's author instructions and place/unpack it locally so these paths exist:

```text
paper/redin-template/Latex Template/packages/redina.cls
paper/redin-template/Latex Template/packages/lineno.sty
paper/redin-template/Latex Template/images/redin_logos/redin.png
paper/redin-template/Latex Template/images/redin_logos/udea.png
```

Then copy the support files into the build directory:

```bash
cd ~/projects/limen-rf

mkdir -p paper/redin/packages paper/redin/images/redin_logos

cp "paper/redin-template/Latex Template/packages/redina.cls" \
   paper/redin/packages/redina.cls

cp "paper/redin-template/Latex Template/packages/lineno.sty" \
   paper/redin/packages/lineno.sty

cp "paper/redin-template/Latex Template/images/redin_logos/redin.png" \
   paper/redin/images/redin_logos/redin.png

cp "paper/redin-template/Latex Template/images/redin_logos/udea.png" \
   paper/redin/images/redin_logos/udea.png
```

## Compile

Compile from inside `paper/redin/`:

```bash
cd ~/projects/limen-rf/paper/redin

# Identified manuscript
latexmk -C article.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error article.tex

# Double-blind reviewer manuscript
latexmk -C article_blind.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error article_blind.tex
```

The supplied REDIN class loads `mathspec`, so XeLaTeX is required in practice.

On Ubuntu/WSL the relevant packages used for the verified build were installed from TeX Live, including `texlive-xetex`, `texlive-pstricks`, `texlive-fonts-extra`, and `texlive-publishers`.

## Expected template warning

The official REDIN example itself produces a title-block overfull warning of approximately 50.6 pt under the verified XeLaTeX environment. LIMEN-RF preserves the journal class rather than modifying `redina.cls` to suppress that template-level artifact.

Check the final log for real reference/citation failures:

```bash
grep -nE "undefined citations|undefined references|Error" article.log
grep -nE "undefined citations|undefined references|Error" article_blind.log
```

## Bibliography

The journal wrappers use the shared bibliography:

```tex
\bibliographystyle{IEEEtran}
\bibliography{../references}
```

Do not maintain a second bibliography database.

## Data availability

The identified wrapper points to:

`https://github.com/topassky3/limen-rf`

The blind wrapper intentionally withholds that identifying URL while preserving the same scientific sections.
