# features.py

import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Extract basic lexical features from a URL string.
    Returns a dictionary of features for ML input.
    """
    features = {}

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    # Basic lexical features
    features["url_length"] = len(url)
    features["hostname_length"] = len(hostname)
    features["path_length"] = len(path)
    features["has_https"] = int(url.lower().startswith("https"))
    features["count_dots"] = url.count(".")
    features["count_hyphens"] = url.count("-")
    features["count_digits"] = sum(c.isdigit() for c in url)
    features["count_special_chars"] = len(re.findall(r"[^\w\s]", url))

    # IP address pattern
    ip_pattern = re.compile(r"(\d{1,3}\.){3}\d{1,3}")
    features["contains_ip"] = int(bool(ip_pattern.search(url)))

    # Suspicious keywords
    suspicious_words = ["login", "verify", "secure", "account", "update", "free", "confirm", "bank", "signin"]
    features["has_suspicious_words"] = int(any(word in url.lower() for word in suspicious_words))

    return features
