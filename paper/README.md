# LIMEN-RF paper

This directory is the journal-manuscript source.

## Current strategy

- Keep the statistical method frozen after Kill-Test 13.
- Treat \`docs/manuscript/*.md\` as the prose source of truth while the first LaTeX conversion is completed.
- Use a neutral \`article\` class first so the manuscript is portable.
- Only switch to a journal-specific template after the target journal and its current author instructions are frozen.
- Do not change the theorem, bettor family, or final baseline grid merely to improve later validation results.

## Build

From \`paper/\`:

\`\`\`bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
\`\`\`

A later CI task can automate this.

## Validation policy

Publication validation is separated from method development:

1. high-replication frozen Monte Carlo;
2. contamination-geometry stress tests without retuning;
3. semi-synthetic RTL-SDR validation using real receiver data plus controlled offline contamination/shift injection;
4. optional fully observational RF demonstration.

SDR results are validation, not part of the mathematical validity proof.
