import logging
from pathlib import Path

import matplotlib.pyplot as plt
from lxml import etree
from wordcloud import WordCloud

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

XML_DIR = Path("output/xml")
OUTPUT_PATH = Path("output/keyword_cloud.png")

# TEI XML namespace used by Grobid
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# Common words to exclude that don't carry scientific meaning
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to", "is", "for",
    "with", "on", "that", "this", "are", "we", "our", "by", "from",
    "be", "as", "at", "it", "its", "also", "can", "which", "have",
    "has", "been", "not", "these", "their", "they", "such", "more",
    "than", "both", "all", "each", "while", "using", "used", "show",
    "shown", "paper", "approach", "propose", "proposed", "present",
    "method", "results", "based", "model",
}


def extract_abstract(xml_path: Path) -> str:
    """Extract plain text from the <abstract> element in a TEI XML file."""
    try:
        tree = etree.parse(str(xml_path))
        # Grobid places the abstract inside //teiHeader/profileDesc/abstract
        abstract_elements = tree.findall(".//tei:abstract", TEI_NS)
        if not abstract_elements:
            logger.warning(f"No abstract found in {xml_path.name}")
            return ""
        # Join all text content inside <abstract>
        text = " ".join(abstract_elements[0].itertext())
        return text.strip()
    except etree.XMLSyntaxError as e:
        logger.error(f"XML parse error in {xml_path.name}: {e}")
        return ""


def build_corpus(xml_dir: Path) -> str:
    """Concatenate abstracts from all TEI XML files into a single string."""
    xml_files = sorted(xml_dir.glob("*.tei.xml"))
    if not xml_files:
        logger.error(f"No TEI XML files found in '{xml_dir}'. Run process_grobid.py first.")
        return ""

    logger.info(f"Found {len(xml_files)} XML files.")
    corpus_parts = []
    for xml_path in xml_files:
        abstract = extract_abstract(xml_path)
        if abstract:
            corpus_parts.append(abstract)
            logger.info(f"Extracted abstract from {xml_path.name} ({len(abstract)} chars)")
        else:
            logger.warning(f"Empty abstract for {xml_path.name}")

    return " ".join(corpus_parts)


def generate_cloud(corpus: str, output_path: Path) -> None:
    """Generate and save the keyword cloud image."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        stopwords=STOPWORDS,
        max_words=100,
        collocations=False,  # Avoid repeated bigrams
    ).generate(corpus)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Keyword Cloud — AI/ML Paper Abstracts", fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Keyword cloud saved to: {output_path}")


def main() -> None:
    corpus = build_corpus(XML_DIR)
    if not corpus:
        logger.error("No text to process. Exiting.")
        return

    generate_cloud(corpus, OUTPUT_PATH)
    logger.info("Done.")


if __name__ == "__main__":
    main()
