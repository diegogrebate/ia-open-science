import csv
import logging
from pathlib import Path

import matplotlib.pyplot as plt
from lxml import etree

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

XML_DIR = Path("output/xml")
OUTPUT_CHART = Path("output/figures_per_paper.png")
OUTPUT_CSV = Path("output/figures_per_paper.csv")

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def get_paper_title(tree: etree._ElementTree) -> str:
    """Extract the paper title from the TEI header, fallback to filename."""
    titles = tree.findall(".//tei:titleStmt/tei:title", TEI_NS)
    if titles and titles[0].text:
        # Truncate long titles for chart readability
        return titles[0].text.strip()[:50]
    return "Unknown"


def count_figures(xml_path: Path) -> dict:
    """Count <figure> elements in a TEI XML file."""
    try:
        tree = etree.parse(str(xml_path))
        figures = tree.findall(".//tei:figure", TEI_NS)
        title = get_paper_title(tree)
        count = len(figures)
        logger.info(f"{xml_path.name}: {count} figures — '{title}'")
        return {"file": xml_path.stem, "title": title, "figures": count}
    except etree.XMLSyntaxError as e:
        logger.error(f"XML parse error in {xml_path.name}: {e}")
        return {"file": xml_path.stem, "title": xml_path.stem, "figures": 0}


def save_csv(data: list[dict], output_path: Path) -> None:
    """Save figure counts to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "title", "figures"])
        writer.writeheader()
        writer.writerows(data)
    logger.info(f"CSV saved to: {output_path}")


def generate_chart(data: list[dict], output_path: Path) -> None:
    """Generate and save a horizontal bar chart of figures per paper."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sort by figure count descending for readability
    data_sorted = sorted(data, key=lambda x: x["figures"], reverse=True)
    labels = [d["title"] for d in data_sorted]
    values = [d["figures"] for d in data_sorted]

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(labels, values, color="steelblue", edgecolor="white")

    # Add count labels at end of each bar
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center",
            fontsize=10,
        )

    ax.set_xlabel("Number of Figures", fontsize=12)
    ax.set_title("Number of Figures per Paper", fontsize=14, pad=15)
    ax.invert_yaxis()  # Highest at top
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Chart saved to: {output_path}")


def main() -> None:
    xml_files = sorted(XML_DIR.glob("*.tei.xml"))
    if not xml_files:
        logger.error(f"No TEI XML files in '{XML_DIR}'. Run process_grobid.py first.")
        return

    logger.info(f"Found {len(xml_files)} XML files.")
    data = [count_figures(xml_path) for xml_path in xml_files]

    save_csv(data, OUTPUT_CSV)
    generate_chart(data, OUTPUT_CHART)
    logger.info("Done.")


if __name__ == "__main__":
    main()
