FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY scripts/ ./scripts/
COPY tests/ ./tests/

RUN mkdir -p data/papers output/xml output/links

CMD ["bash", "-c", \
    "python scripts/papers.py && \
     python scripts/process_grobid.py && \
     python scripts/keyword_cloud.py && \
     python scripts/figures_chart.py && \
     python scripts/extract_links.py"]