# Validation

This section explains how each output of the pipeline was validated.

## Keyword Cloud

**How it was validated:**

- Verified that top words in the cloud match expected AI/ML terminology such as "learning", "training", "model", "attention", "network"
- Confirmed that English stopwords ("the", "and", "of") are absent from the output
- Cross-checked the abstract text extracted from XML against the original PDFs for two papers (1706.03762 and 1810.04805) to confirm correct extraction

## Figures per Paper

**How it was validated:**

- Manually opened three papers in a PDF viewer and counted visible figures
- Compared the manual count against the script output
- The Attention paper (1706.03762) contains at least 3 figures (architecture diagram, training curves, BLEU score results); the script count matches or exceeds this due to Grobid also tagging tables as `<figure>` elements in some cases — documented as a known limitation

## Link Extraction

**How it was validated:**

- Ran `test_extracted_links_are_valid_urls` from `tests/test_pipeline.py` to confirm all extracted strings start with `http://` or `https://`
- Manually verified links from one paper (1706.03762) against the reference list in the PDF
- Spot-checked 5 extracted URLs by visiting them in a browser to confirm they resolve correctly
