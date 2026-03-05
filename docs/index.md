# Paper Analysis Pipeline

A reproducible pipeline for extracting and analysing text from 10 open-access AI/ML research papers using [Grobid](https://github.com/kermitt2/grobid).

## What it does

- Downloads 10 foundational AI/ML papers from ArXiv
- Processes them with Grobid to extract structured TEI-XML
- Generates a **keyword cloud** from all paper abstracts
- Visualises the **number of figures per paper** as a bar chart
- Extracts all **URLs/links** found in each paper

## Quick start

```bash
git clone https://github.com/diegogrebate/ia-open-science
cd ia-open-science
poetry install
poetry env activate && source <env>

# In a separate terminal, start Grobid:
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.2

# Then run the pipeline:
poetry run python scripts/papers.py
poetry run python scripts/process_grobid.py
poetry run python scripts/keyword_cloud.py
poetry run python scripts/figures_chart.py
poetry run python scripts/extract_links.py
```

See [Installation](installation.md) and [Usage](usage.md) for full details.
