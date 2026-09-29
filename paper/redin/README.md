# REDIN submission build

This directory is the journal-format layer for LIMEN-RF. The scientific source of truth remains:

- \`paper/sections/*.tex\`
- \`paper/references.bib\`
- frozen result artifacts under \`results/\`

Do not copy-edit scientific claims separately in this directory.

## Template files required locally

Copy the official REDIN template support files into this directory:

\`\`\`bash
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
\`\`\`

## Compile

Compile from inside \`paper/redin\` so the REDIN class can find its relative \`packages/\` and \`images/\` paths:

\`\`\`bash
cd ~/projects/limen-rf/paper/redin

latexmk -xelatex -interaction=nonstopmode -halt-on-error article.tex
\`\`\`

If XeLaTeX exposes incompatibilities in the supplied journal class, the template README also permits PDFLaTeX. Prefer XeLaTeX for the submission build unless the official class requires otherwise.

## Double-blind metadata

The REDIN class renders \`Authors: Double-blind review\` on the title page. The current article source also uses non-identifying placeholders. Before the non-anonymous final submission, complete:

- author name and ORCID;
- affiliation;
- corresponding-author email;
- competing-interest declaration;
- acknowledgements, if any;
- funding;
- author contributions;
- data/code availability.

## Bibliography

The journal build uses:

\`\`\`tex
\bibliographystyle{IEEEtran}
\bibliography{../references}
\`\`\`

Do not maintain a second bibliography database.
