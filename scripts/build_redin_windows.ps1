# Build both REDIN manuscripts on Windows with the official local class.
# Usage (PowerShell): .\scripts\build_redin_windows.ps1
# Does not change frozen simulations, scientific source, or Git history.

[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $HOME "Downloads")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
$paper = Join-Path $repo "paper\redin"
$check = Join-Path $PSScriptRoot "check_redin_editorial.py"

# TinyTeX installed as the user's personal TeX Live distribution.
$texBin = Join-Path $env:APPDATA "TinyTeX\bin\windows"
if (-not (Get-Command xelatex -ErrorAction SilentlyContinue)) {
    if (Test-Path (Join-Path $texBin "xelatex.exe")) {
        $env:Path = "$texBin;$env:Path"
    }
}

foreach ($command in @("git", "xelatex", "latexmk")) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required program not found: $command"
    }
}

$required = @(
    "article.tex",
    "article_blind.tex",
    "packages\redina.cls",
    "packages\lineno.sty",
    "images\redin_logos\redin.png",
    "images\redin_logos\udea.png"
)
foreach ($item in $required) {
    $file = Join-Path $paper $item
    if (-not (Test-Path $file -PathType Leaf)) {
        throw "Missing REDIN template or manuscript file: $file"
    }
}

$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw "Python is needed for the editorial check (py or python)."
}

Push-Location $repo
try {
    Write-Host "=== REDIN editorial verification ==="
    & $python.Source $check
    if ($LASTEXITCODE -ne 0) {
        throw "Editorial compliance check failed."
    }

    $commit = (& git rev-parse --short HEAD).Trim()
    Write-Host "SOURCE_COMMIT=$commit"
}
finally {
    Pop-Location
}

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

Push-Location $paper
try {
    foreach ($stem in @("article", "article_blind")) {
        Write-Host "=== Compiling $stem.tex ==="
        & latexmk -C "$stem.tex"
        if ($LASTEXITCODE -ne 0) {
            throw "Cleanup failed for $stem.tex"
        }
        & latexmk -xelatex -interaction=nonstopmode -halt-on-error "$stem.tex"
        if ($LASTEXITCODE -ne 0) {
            throw "XeLaTeX compilation failed for $stem.tex"
        }

        $pdf = Join-Path $paper "$stem.pdf"
        $log = Join-Path $paper "$stem.log"
        if (-not (Test-Path $pdf -PathType Leaf)) {
            throw "Missing output PDF: $pdf"
        }
        if ((Get-Item $pdf).Length -lt 10000) {
            throw "Output PDF appears truncated: $pdf"
        }
        $logText = Get-Content $log -Raw
        if ($logText -match "(?i)undefined (citations|references)|LaTeX Error|Emergency stop") {
            throw "LaTeX error or unresolved references in $log"
        }

        $label = if ($stem -eq "article") { "IDENTIFIED" } else { "BLIND" }
        $target = Join-Path $OutputDirectory ("REDIN_LIMEN_RF_Revision_" + $label + ".pdf")
        Copy-Item $pdf $target -Force
        Write-Host "COMPILED=$target"
        Write-Host "PDF_BYTES=$((Get-Item $target).Length)"
    }
}
finally {
    Pop-Location
}

Write-Host "REDIN_LATEX_BUILD=PASS"
Write-Host "Inspect both PDFs visually, especially equations and the first/last pages."
