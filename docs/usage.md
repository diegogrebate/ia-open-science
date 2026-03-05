# Usage

Run the scripts in the following order after completing [Installation](installation.md).

## 1. Download papers

```bash
poetry run python scripts/papers.py
```

Downloads 10 ArXiv PDFs to `data/papers/`. Skips files already present.

## 2. Process with Grobid

```bash
poetry run python scripts/process_grobid.py
```

Sends each PDF to the local Grobid server and saves TEI-XML responses to `output/xml/`.
Grobid must be running before executing this step.

## 3. Generate keyword cloud

```bash
poetry run python scripts/keyword_cloud.py
```

Extracts abstracts from all XML files and generates `output/keyword_cloud.png`.

## 4. Generate figures chart

```bash
poetry run python scripts/figures_chart.py
```

Counts `<figure>` elements per paper and generates `output/figures_per_paper.png` and `output/figures_per_paper.csv`.

## 5. Extract links

```bash
poetry run python scripts/extract_links.py
```

Extracts all URLs from each paper and saves them to `output/links/`.

## Running tests

```bash
poetry run pytest tests/ -v
```
