# features.py

import re
from urllib.parse import urlparse

def extract_features(url):
    features = {}

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    # Match names exactly to what your model expects:
    features["length_url"] = len(url)
    features["length_hostname"] = len(hostname)
    features["nb_dots"] = url.count(".")
    features["nb_hyphens"] = url.count("-")
    features["nb_at"] = url.count("@")
    features["nb_qm"] = url.count("?")
    features["nb_and"] = url.count("&")
    features["nb_or"] = url.count("|")
    features["nb_slash"] = url.count("/")
    features["nb_www"] = int("www" in url.lower())

    # Ratio of digits in URL
    num_digits = sum(c.isdigit() for c in url)
    features["ratio_digits_url"] = num_digits / len(url) if len(url) > 0 else 0.0

    return features
