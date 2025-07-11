# features.py
# ---------------------------------------------------------
# 📊 Feature Extraction Module
# Extracts lexical/structural features from URLs
# ---------------------------------------------------------

import numpy as np
from urllib.parse import urlparse
import tldextract


def extract_basic_features(url: str) -> dict:
    """
    Extract common lexical and structural features from a given URL.
    These features are used by the ML model to classify the URL.
    """
    parsed          = urlparse(url)
    hostname        = parsed.hostname or ""
    ext             = tldextract.extract(url)

    length_url      = len(url)
    length_hostname = len(hostname)
    nb_dots         = url.count(".")
    nb_hyphens      = url.count("-")
    nb_at           = url.count("@")
    nb_qm           = url.count("?")
    nb_and          = url.count("&")
    nb_or           = url.count("|")
    nb_slash        = url.count("/")
    nb_www          = 1 if "www" in ext.subdomain.split(".") else 0

    digits          = sum(c.isdigit() for c in url)
    ratio_digits    = digits / length_url if length_url else 0.0

    google_index    = 0  # Placeholder
    page_rank       = 0  # Placeholder

    return {
        "length_url": length_url,
        "length_hostname": length_hostname,
        "nb_dots": nb_dots,
        "nb_hyphens": nb_hyphens,
        "nb_at": nb_at,
        "nb_qm": nb_qm,
        "nb_and": nb_and,
        "nb_or": nb_or,
        "nb_slash": nb_slash,
        "nb_www": nb_www,
        "ratio_digits_url": ratio_digits,
        "google_index": google_index,
        "page_rank": page_rank,
    }


def build_feature_vector(url: str, feat_list: list) -> np.ndarray:
    """
    Build a feature vector aligned with the feature list expected by the model.
    Missing features are padded with 0 to maintain dimensionality.
    """
    base = extract_basic_features(url)
    vector = [base.get(f, 0) for f in feat_list]
    return np.array(vector).reshape(1, -1)
