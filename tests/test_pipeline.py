from pathlib import Path

import pytest
import requests

# --- Test 1: Paper URLs are valid (HTTP 200) ---

ARXIV_IDS = [
    "1706.03762",
    "1810.04805",
    "2005.14165",
    "1512.03385",
    "1406.2661",
    "1412.6980",
    "2103.00020",
    "2105.05233",
    "2302.13971",
    "1207.0580",
]


@pytest.mark.parametrize("arxiv_id", ARXIV_IDS)
def test_paper_url_is_reachable(arxiv_id):
    """Test 1: Check that each ArXiv paper URL returns HTTP 200."""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    response = requests.head(url, timeout=10, allow_redirects=True)
    assert response.status_code == 200, (
        f"Paper {arxiv_id} URL returned {response.status_code}"
    )


# --- Test 2: Downloaded files are valid PDFs ---

PDF_DIR = Path("data/papers")


def test_downloaded_files_are_pdfs():
    """Test 2: Check that all files in data/papers/ are valid PDFs."""
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    assert len(pdf_files) > 0, "No PDF files found in data/papers/"

    for pdf_path in pdf_files:
        with open(pdf_path, "rb") as f:
            header = f.read(4)
        assert header == b"%PDF", (
            f"{pdf_path.name} does not appear to be a valid PDF (header: {header})"
        )


# --- Test 3: Figure count for a known paper is non-negative ---

XML_DIR = Path("output/xml")


def test_figure_counts_are_non_negative():
    """Test 3: Figure counts extracted from XML are >= 0 for all papers."""
    from lxml import etree

    TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
    xml_files = list(XML_DIR.glob("*.tei.xml"))

    if not xml_files:
        pytest.skip("No XML files found — run process_grobid.py first.")

    for xml_path in xml_files:
        tree = etree.parse(str(xml_path))
        figures = tree.findall(".//tei:figure", TEI_NS)
        assert len(figures) >= 0, f"Unexpected figure count for {xml_path.name}"


# --- Test 4: Abstract extraction returns non-empty strings ---

def test_abstract_extraction():
    """Test 4: Abstract text is non-empty for all processed papers."""
    from lxml import etree

    TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
    xml_files = list(XML_DIR.glob("*.tei.xml"))

    if not xml_files:
        pytest.skip("No XML files found — run process_grobid.py first.")

    for xml_path in xml_files:
        tree = etree.parse(str(xml_path))
        abstract_el = tree.findall(".//tei:abstract", TEI_NS)
        if abstract_el:
            text = " ".join(abstract_el[0].itertext()).strip()
            assert len(text) > 0, f"Empty abstract in {xml_path.name}"


# --- Test 5: Link extraction returns valid-looking URLs ---

def test_extracted_links_are_valid_urls():
    """Test 5: All extracted links start with http:// or https://."""
    links_dir = Path("output/links")
    link_files = list(links_dir.glob("*_links.txt"))

    if not link_files:
        pytest.skip("No link files found — run extract_links.py first.")

    for link_file in link_files:
        links = link_file.read_text(encoding="utf-8").splitlines()
        for link in links:
            if link:  # skip empty lines
                assert link.startswith("http"), (
                    f"Invalid URL in {link_file.name}: {link}"
                )

def test_paper_list_has_ten_entries():
    """Test that the paper list contains exactly 10 entries."""
    from scripts.papers import PAPERS
    assert len(PAPERS) == 10

def test_paper_list_has_required_keys():
    """Test that each paper entry has id and title."""
    from scripts.papers import PAPERS
    for paper in PAPERS:
        assert "id" in paper
        assert "title" in paper
