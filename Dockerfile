FROM python:3.10-slim

# Install system dependencies needed by lxml and wordcloud
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching — only reinstalls if these change)
COPY pyproject.toml poetry.lock ./

# Install dependencies only, not the project itself
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

# Copy the rest of the project
COPY scripts/ ./scripts/
COPY tests/ ./tests/

# Create expected directories
RUN mkdir -p data/papers output/xml output/links

# Default command runs the full pipeline
CMD ["bash", "-c", \
    "python scripts/papers.py && \
     python scripts/process_grobid.py && \
     python scripts/keyword_cloud.py && \
     python scripts/figures_chart.py && \
     python scripts/extract_links.py"]