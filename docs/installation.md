# Installation

There are two ways to run this project: Docker Compose (recommended, no Python setup needed) or Poetry (local environment).

## Requirements

- [Docker](https://docs.docker.com/get-docker/) — required for both methods
- [Poetry](https://python-poetry.org/) — only needed for the local environment method

---

## Option A — Docker Compose (recommended)

Docker Compose runs both Grobid and the pipeline together automatically. Think of it as a self-contained lab: everything spins up, runs, and the results appear in your `output/` folder.

### Steps

```bash
git clone https://github.com/diegogrebate/ia-open-science.git
cd ia-open-science
docker compose up
```

That's it. Docker Compose will:

1. Pull and start the Grobid server
2. Wait until Grobid is healthy
3. Build and run the pipeline
4. Save all outputs to `output/` on your machine

To run a single script instead of the full pipeline:

```bash
docker compose run pipeline python scripts/keyword_cloud.py
```

---

## Option B — Poetry (local environment)

### 1. Clone the repository

```bash
git clone https://github.com/diegogrebate/ia-open-science.git
cd ia-open-science
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Activate the environment

```bash
poetry env activate
source <path printed by the above command>
```

### 4. Create required folders

```bash
mkdir -p data/papers output/xml output/links
```

### 5. Start Grobid

Run this in a **separate terminal** and keep it open during pipeline execution:

```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.2
```

Verify it is running by visiting `http://localhost:8070` in your browser. You should see the Grobid web interface.

### 6. Run the pipeline

```bash
poetry run python scripts/papers.py
poetry run python scripts/process_grobid.py
poetry run python scripts/keyword_cloud.py
poetry run python scripts/figures_chart.py
poetry run python scripts/extract_links.py
```
