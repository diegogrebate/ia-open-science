import logging
import time
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"
PDF_DIR = Path("data/papers")
XML_DIR = Path("output/xml")
TIMEOUT = 60  # seconds per request
RETRY_WAIT = 5  # seconds to wait if Grobid is busy (503)


def is_grobid_alive() -> bool:
    """Check Grobid server online before processing."""
    try:
        response = requests.get("http://localhost:8070/api/isalive", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def process_pdf(pdf_path: Path, output_dir: Path) -> None:
    """Send a single PDF to Grobid and save the TEI-XML response."""
    xml_path = output_dir / f"{pdf_path.stem}.tei.xml"

    # No duplicates
    if xml_path.exists():
        logger.info(f"Skipping {pdf_path.name} — XML already exists.")
        return

    logger.info(f"Processing: {pdf_path.name}")

    with open(pdf_path, "rb") as pdf_file:
        files = {"input": (pdf_path.name, pdf_file, "application/pdf")}
        params = {"consolidateHeader": "1"}

        for attempt in range(3):
            try:
                response = requests.post(
                    GROBID_URL,
                    files=files,
                    data=params,
                    timeout=TIMEOUT,
                )

                if response.status_code == 200:
                    xml_path.write_text(response.text, encoding="utf-8")
                    logger.info(f"Saved XML: {xml_path}")
                    return
                elif response.status_code == 503:
                    logger.warning(
                        f"Grobid busy (503), retrying in {RETRY_WAIT}s... "
                        f"(attempt {attempt + 1}/3)"
                    )
                    time.sleep(RETRY_WAIT)
                else:
                    logger.error(
                        f"Unexpected status {response.status_code} for {pdf_path.name}"
                    )
                    return

            except requests.RequestException as e:
                logger.error(f"Request failed for {pdf_path.name}: {e}")
                return

    logger.error(f"Failed to process {pdf_path.name} after 3 attempts.")


def main() -> None:
    if not is_grobid_alive():
        logger.error(
            "Grobid server is not running. Start it with:\n"
            "  docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.2"
        )
        return

    logger.info("Grobid server is up.")
    XML_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        logger.error(f"No PDFs found in '{PDF_DIR}'. Run papers.py first.")
        return

    logger.info(f"Found {len(pdfs)} PDFs to process.")
    for pdf_path in pdfs:
        process_pdf(pdf_path, XML_DIR)
        time.sleep(1)  # Avoid overwhelming local server

    xml_files = list(XML_DIR.glob("*.tei.xml"))
    logger.info(f"\nDone. {len(xml_files)}/{len(pdfs)} XMLs in '{XML_DIR}'.")


if __name__ == "__main__":
    main()
