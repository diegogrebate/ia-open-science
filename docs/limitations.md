# Limitations

- **Figure counting:** Grobid tags both figures and tables as `<figure>` elements in TEI XML. The figure count per paper may therefore be higher than the actual number of visual figures.

- **Abstract extraction:** Assumes standard TEI structure output from Grobid. Papers with non-standard formatting or scanned PDFs may yield incomplete or empty abstracts.

- **URL extraction:** The regex-based fallback may capture malformed URLs created by line breaks in the original PDF. These are included in the output as-is.

- **Grobid dependency:** The pipeline requires a locally running Grobid server. If the server is unavailable or overloaded (HTTP 503), processing is retried up to 3 times then skipped with a warning.

- **ArXiv access:** Downloading papers requires internet access. ArXiv may rate-limit repeated requests; a 1-second delay between downloads is included to mitigate this.

- **Language:** The stopword list in `keyword_cloud.py` is English-only. Papers with multilingual content may produce unexpected terms in the cloud.
