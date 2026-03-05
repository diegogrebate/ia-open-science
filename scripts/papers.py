import logging
import time
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# 10 foundational open-access AI/ML papers from ArXiv
PAPERS = [
    {"id": "1706.03762", "title": "Attention Is All You Need"},
    {"id": "1810.04805", "title": "BERT"},
    {"id": "2005.14165", "title": "GPT-3"},
    {"id": "1512.03385", "title": "Deep Residual Learning (ResNet)"},
    {"id": "1406.2661", "title": "Generative Adversarial Networks"},
    {"id": "1412.6980", "title": "Adam Optimizer"},
    {"id": "2103.00020", "title": "CLIP"},
    {"id": "2105.05233", "title": "Diffusion Models Beat GANs"},
    {"id": "2302.13971", "title": "LLaMA"},
    {"id": "1207.0580", "title": "Dropout"},
]

OUTPUT_DIR = Path("data/papers")
ARXIV_PDF_URL = "https://arxiv.org/pdf/{id}.pdf"


def download_paper(paper: dict, output_dir: Path) -> None:
    """Download a paper PDF from ArXiv."""
    arxiv_id = paper["id"]
    title = paper["title"]
    output_path = output_dir / f"{arxiv_id}.pdf"

    # No duplicate downloading
    if output_path.exists():
        logger.info(f"Skipping '{title}' — already downloaded.")
        return

    url = ARXIV_PDF_URL.format(id=arxiv_id)
    logger.info(f"Downloading '{title}' from {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Basic check, PDFs start with %PDF
        if not response.content.startswith(b"%PDF"):
            raise ValueError(f"Response for {arxiv_id} does not appear to be a PDF.")

        output_path.write_bytes(response.content)
        logger.info(f"Saved: {output_path}")

    except requests.RequestException as e:
        logger.error(f"Failed to download '{title}': {e}")
    except ValueError as e:
        logger.error(e)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for paper in PAPERS:
        download_paper(paper, OUTPUT_DIR)
        time.sleep(1)  # Avoid ratelimiting if any

    downloaded = list(OUTPUT_DIR.glob("*.pdf"))
    logger.info(f"\nDone. {len(downloaded)}/{len(PAPERS)} PDFs in '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()
