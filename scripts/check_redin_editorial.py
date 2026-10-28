from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
REDIN = PAPER / "redin"
SECTIONS = PAPER / "sections"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def between(text: str, start: str, end: str, label: str) -> str:
    i = text.find(start)
    if i < 0:
        fail(f"missing {label} start marker")
        return ""
    i += len(start)
    j = text.find(end, i)
    if j < 0:
        fail(f"missing {label} end marker")
        return ""
    return text[i:j]


def plain_words(tex: str) -> list[str]:
    tex = re.sub(r"%.*", " ", tex)
    tex = re.sub(r"\\(?:'|\\"|\^|~|c)\{?([A-Za-z])\}?", r"\1", tex)
    tex = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", tex)
    tex = tex.replace("\\(", " ").replace("\\)", " ")
    tex = tex.replace("{", " ").replace("}", " ")
    tex = re.sub(r"[^0-9A-Za-zÀ-ÿ-]+", " ", tex)
    return [w for w in tex.split() if w]


def check_front_matter(path: Path, *, identified: bool) -> None:
    text = read(path)
    abstract = between(text, "\\abstract{%\n", "\n}\n\n\\resumen", f"{path.name} abstract")
    resumen = between(text, "\\resumen{%\n", "\n}\n\n\\keywords", f"{path.name} resumen")
    kw_block = between(text, "\\keywords{%\n", "\n}\n\n\\begin{document}", f"{path.name} keywords")

    abstract_n = len(plain_words(abstract))
    resumen_n = len(plain_words(resumen))
    print(f"{path.name}: abstract_words={abstract_n}, resumen_words={resumen_n}")
    if abstract_n > 230:
        fail(f"{path.name}: abstract has {abstract_n} words (>230)")
    if resumen_n > 230:
        fail(f"{path.name}: resumen has {resumen_n} words (>230)")

    m = re.fullmatch(r"(.*?)%\n\}\{%\n(.*?)%", kw_block, flags=re.S)
    if not m:
        fail(f"{path.name}: could not parse bilingual keywords")
    else:
        en = [x.strip() for x in m.group(1).split(",") if x.strip()]
        es = [x.strip() for x in m.group(2).split(",") if x.strip()]
        print(f"{path.name}: keywords_en={len(en)}, keywords_es={len(es)}")
        if len(en) > 5 or len(es) > 5:
            fail(f"{path.name}: more than five keywords")
        title = between(text, "\\title{", "}\n\\titulo", f"{path.name} title").lower()
        titulo = between(text, "\\titulo{", "}\n\n", f"{path.name} Spanish title").lower()
        for kw in en:
            if kw.lower() in title:
                fail(f"{path.name}: English keyword repeats title phrase: {kw}")
        for kw in es:
            if kw.lower() in titulo:
                fail(f"{path.name}: Spanish keyword repeats title phrase: {kw}")

    if "\\section{AI-Use Statement}" not in text:
        fail(f"{path.name}: missing AI-Use Statement")

    if "private GitHub repository" in text:
        fail(f"{path.name}: stale private-repository wording remains")

    if identified and "J. F. Orozco Cort\\'es:" not in text:
        fail(f"{path.name}: Author contributions name format is not initials + surname")


def check_named_citations() -> None:
    text = "\n".join(read(p) for p in sorted(SECTIONS.glob("*.tex")))
    forbidden = [
        "Kuang and Xia",
        "Clarkson et al.",
        "Bashari, Sesia, and Romano",
        "Saha and Ramdas",
        "Shaer et al.",
    ]
    for phrase in forbidden:
        if phrase in text:
            fail(f"direct author naming remains in manuscript prose: {phrase}")


def check_float_and_equation_mentions() -> None:
    for path in sorted(SECTIONS.glob("*.tex")):
        text = read(path)
        for env in ("equation", "align"):
            pattern = re.compile(
                rf"\\begin\{{{env}\}}(?P<body>.*?)\\end\{{{env}\}}",
                flags=re.S,
            )
            for match in pattern.finditer(text):
                body = match.group("body")
                labels = re.findall(r"\\label\{([^}]+)\}", body)
                for label in labels:
                    before = text[max(0, match.start() - 700) : match.start()]
                    token = f"Equation~\\eqref{{{label}}}"
                    if token not in before:
                        fail(f"{path.name}: {label} is not introduced before display")

        for env, word in (("figure", "Figure"), ("table", "Table")):
            pattern = re.compile(
                rf"\\begin\{{{env}\}}(?P<body>.*?)\\end\{{{env}\}}",
                flags=re.S,
            )
            for match in pattern.finditer(text):
                body = match.group("body")
                labels = re.findall(r"\\label\{([^}]+)\}", body)
                for label in labels:
                    before = text[max(0, match.start() - 900) : match.start()]
                    token = f"{word}~\\ref{{{label}}}"
                    if token not in before:
                        fail(f"{path.name}: {label} is not mentioned as {word} before placement")


def check_reference_urls() -> None:
    bib = read(PAPER / "references.bib")
    entries = [e for e in re.split(r"(?=^@)", bib, flags=re.M) if e.strip()]
    print(f"references: entries={len(entries)}")
    for entry in entries:
        key_match = re.search(r"^@\w+\{([^,]+),", entry)
        key = key_match.group(1) if key_match else "<unknown>"
        if not re.search(r"^\s*url\s*=", entry, flags=re.M):
            fail(f"reference {key}: missing URL")


def main() -> int:
    check_front_matter(REDIN / "article.tex", identified=True)
    check_front_matter(REDIN / "article_identified.tex", identified=True)
    check_front_matter(REDIN / "article_blind.tex", identified=False)
    check_named_citations()
    check_float_and_equation_mentions()
    check_reference_urls()

    if failures:
        print("\nREDIN_EDITORIAL_CHECK=FAIL")
        for item in failures:
            print(f" - {item}")
        return 1

    print("\nREDIN_EDITORIAL_CHECK=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
