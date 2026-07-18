"""
ml_predictor.py
Loads the TF-IDF vectorizer + classifiers trained on
dataset-tickets-multi-lang-4-20k.csv (see /training/train_model.py)
and exposes a single predict() function used by the Flask routes.

Note: the originally supplied model__1_.pkl is a plain scikit-learn
LinearRegression expecting 4 unlabelled numeric features - it has no
relationship to raw ticket text, so it can't power text-based triage.
The classifiers here were trained fresh on your ticket dataset instead
(TF-IDF -> Logistic Regression, one classifier per predicted field).
"""
import os
import re
import pickle

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

_vectorizer = None
_classifiers = None


def _load():
    global _vectorizer, _classifiers
    if _vectorizer is None or _classifiers is None:
        with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "rb") as f:
            _vectorizer = pickle.load(f)
        with open(os.path.join(MODELS_DIR, "classifiers.pkl"), "rb") as f:
            _classifiers = pickle.load(f)
    return _vectorizer, _classifiers


def _clean(text):
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _detect_language(text):
    """Very small heuristic language guess (en/de) used only for display -
    good enough for a demo without pulling in a heavy language-id library."""
    de_markers = [" der ", " die ", " das ", " und ", " ist ", " nicht ",
                  " ich ", " sie ", " ein ", " mit ", "ö", "ü", "ä", "ß"]
    t = f" {text.lower()} "
    hits = sum(1 for m in de_markers if m in t)
    return "de" if hits >= 2 else "en"


def predict(subject: str, body: str):
    vectorizer, classifiers = _load()
    text = _clean(f"{subject} {body}")
    X = vectorizer.transform([text])

    result = {"language": _detect_language(text)}
    for field, clf in classifiers.items():
        pred = clf.predict(X)[0]
        proba = None
        if hasattr(clf, "predict_proba"):
            probs = clf.predict_proba(X)[0]
            proba = round(float(max(probs)) * 100, 1)
        result[field] = pred
        result[f"{field}_confidence"] = proba
    return result
