# Installation

## Requirements

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for environment management
- [Docker](https://docs.docker.com/get-docker/) for running Grobid

## Steps

### 1. Clone the repository

```bash
git clone https://github.com/diegogrebate/ia-open-science
cd ia-open-science
```

### 2. Install dependencies with Poetry

```bash
poetry install
```

### 3. Activate the environment

```bash
poetry env activate
source <path printed by the above command>
```

### 4. Start Grobid via Docker

Run this in a separate terminal and keep it open during pipeline execution:

```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.2
```

Verify it is running by visiting `http://localhost:8070` in your browser.
