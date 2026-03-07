# Paper Analysis Pipeline

[![CI](https://github.com/diegogrebate/ia-open-science/actions/workflows/ci.yml/badge.svg)](https://github.com/diegogrebate/ia-open-science/actions)
[![DOI](https://zenodo.org/badge/1166802123.svg)](https://doi.org/10.5281/zenodo.18879554)
[![Documentation](https://readthedocs.org/projects/ia-open-science/badge/?version=latest)](https://ia-open-science.readthedocs.io)

Text extraction and analysis of 10 open-access AI/ML research papers using [Grobid](https://github.com/kermitt2/grobid).

## Description

This project implements a reproducible pipeline that:

- Downloads 10 foundational AI/ML papers from ArXiv
- Processes them with Grobid (a PDF-to-TEI-XML machine learning library)
- Generates a **keyword cloud** from all paper abstracts
- Visualizes the **number of figures per paper** as a bar chart
- Extracts all **links/URLs** found in each paper

## Dataset

10 open-access AI/ML papers from ArXiv:

| ArXiv ID   | Title                           |
| ---------- | ------------------------------- |
| 1706.03762 | Attention Is All You Need       |
| 1810.04805 | BERT                            |
| 2005.14165 | GPT-3                           |
| 1512.03385 | Deep Residual Learning (ResNet) |
| 1406.2661  | Generative Adversarial Networks |
| 1412.6980  | Adam Optimizer                  |
| 2103.00020 | CLIP                            |
| 2105.05233 | Diffusion Models Beat GANs      |
| 2302.13971 | LLaMA                           |
| 1207.0580  | Dropout                         |

All papers are open-access. PDFs are not committed to this repository. Use `scripts/papers.py` to fetch them.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) — required for both installation methods
- [Poetry](https://python-poetry.org/) — for the local environment method only

## Installation

There are two ways to run this project.

### Option A — Docker Compose (recommended)

Runs the full pipeline in an isolated environment. No Python setup needed.

```bash
git clone https://github.com/diegogrebate/ia-open-science.git
cd ia-open-science
docker compose up
```

Results will appear in `output/` on your machine once the pipeline finishes.

### Option B — Poetry (local environment)

```bash
git clone https://github.com/diegogrebate/ia-open-science.git
cd ia-open-science

# Install dependencies
poetry install

# Activate the environment
poetry env activate
source <path printed by the above command>

# Create required folders
mkdir -p data/papers output/xml output/links
```

Then start Grobid in a separate terminal and keep it running:

```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.2
```

## Usage

### With Docker Compose

```bash
docker compose up
```

To run a single script instead of the full pipeline:

```bash
docker compose run pipeline python scripts/keyword_cloud.py
```

### With Poetry

Run scripts in this order:

```bash
poetry run python scripts/papers.py
poetry run python scripts/process_grobid.py
poetry run python scripts/keyword_cloud.py
poetry run python scripts/figures_chart.py
poetry run python scripts/extract_links.py
```

Outputs are saved to `output/`.

## Running Tests

```bash
poetry run pytest tests/ -v
```

## Validation

### Keyword Cloud

- Validated by manually checking that the top words in the cloud match expected AI/ML terminology (e.g., "learning", "training", "model", "network")
- Verified that stopwords are correctly filtered (common English words like "the", "and" are absent)

### Figures per Paper

- Cross-validated counts against manually checking a subset of papers in their original PDFs
- The Attention paper (1706.03762) should have at least 3 figures (architecture diagram, training curves, results tables)

### Link Extraction

- Verified that extracted links resolve (HTTP 200) using the URL test in `tests/test_pipeline.py`
- Cross-checked a sample paper's links against manually reading the PDF references section

## Limitations

- Grobid's figure detection counts `<figure>` tags in TEI XML, which may include tables (tagged as figures in some versions of Grobid)
- Abstract extraction assumes standard TEI structure — some papers with non-standard formatting may yield incomplete abstracts
- URL extraction via regex may capture malformed URLs from broken line wraps in the PDF
- The pipeline requires a running Grobid instance; if unavailable it retries 3 times then skips the file
- Docker Compose requires the Grobid health check to pass before the pipeline starts — on slow machines this may take over 30 seconds

## Project Structure

```
ia-open-science/
├── data/papers/              # Downloaded PDFs (not committed)
├── output/
│   ├── xml/                  # Grobid TEI XML output
│   ├── links/                # Extracted links per paper
│   ├── keyword_cloud.png
│   └── figures_per_paper.png
├── scripts/
│   ├── papers.py
│   ├── process_grobid.py
│   ├── keyword_cloud.py
│   ├── figures_chart.py
│   └── extract_links.py
├── tests/
│   └── test_pipeline.py
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── CITATION.cff
├── codemeta.json
└── README.md
```

## Citation

If you use this project, please cite it as described in `CITATION.cff`.

## Acknowledgements

- [Grobid](https://github.com/kermitt2/grobid) by Laurent Romary and Patrice Lopez
- Course: Open Science and AI in Research Software Engineering, UPM
