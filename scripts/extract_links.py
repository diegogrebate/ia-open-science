import csv
import logging
import re
from pathlib import Path

from lxml import etree

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

XML_DIR = Path("output/xml")
LINKS_DIR = Path("output/links")
ALL_LINKS_CSV = LINKS_DIR / "all_links.csv"

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# Regex to catch URLs that may appear in plain text nodes
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"\')\]},;]+"
)


def extract_links_from_xml(xml_path: Path) -> list[str]:
    """
    Extract URLs from a TEI XML file using two strategies:
    1. @target attributes on <ref> elements (structured links Grobid finds)
    2. Regex scan of all text nodes (catches inline URLs in body text)
    """
    try:
        tree = etree.parse(str(xml_path))
    except etree.XMLSyntaxError as e:
        logger.error(f"XML parse error in {xml_path.name}: {e}")
        return []

    found = set()

    # Strategy 1: structured <ref> elements with target attribute
    for ref in tree.findall(".//tei:ref[@target]", TEI_NS):
        target = ref.get("target", "").strip()
        if target.startswith("http"):
            found.add(target)

    # Strategy 2: regex over all text content
    full_text = " ".join(tree.getroot().itertext())
    for match in URL_PATTERN.findall(full_text):
        # Clean trailing punctuation that may have been captured
        url = match.rstrip(".,;:)")
        found.add(url)

    links = sorted(found)
    logger.info(f"{xml_path.name}: {len(links)} unique URLs found")
    return links


def save_per_paper(paper_id: str, links: list[str], output_dir: Path) -> None:
    """Save per-paper link list as a plain text file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{paper_id}_links.txt"
    out_path.write_text("\n".join(links), encoding="utf-8")
    logger.info(f"Saved: {out_path}")


def save_all_csv(all_links: list[dict], output_path: Path) -> None:
    """Save all links combined into a single CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["paper", "url"])
        writer.writeheader()
        writer.writerows(all_links)
    logger.info(f"Combined CSV saved to: {output_path}")


def main() -> None:
    xml_files = sorted(XML_DIR.glob("*.tei.xml"))
    if not xml_files:
        logger.error(f"No TEI XML files in '{XML_DIR}'. Run process_grobid.py first.")
        return

    logger.info(f"Found {len(xml_files)} XML files.")
    all_links = []

    for xml_path in xml_files:
        paper_id = xml_path.stem.replace(".tei", "")
        links = extract_links_from_xml(xml_path)
        save_per_paper(paper_id, links, LINKS_DIR)
        for url in links:
            all_links.append({"paper": paper_id, "url": url})

    save_all_csv(all_links, ALL_LINKS_CSV)
    logger.info(f"\nDone. Total unique URLs across all papers: {len(all_links)}")


if __name__ == "__main__":
    main()
