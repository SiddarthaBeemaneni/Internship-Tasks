from pathlib import Path
import pickle
BASE = Path(__file__).resolve().parent
with open(BASE / "model.pkl", "rb") as f:
    model = pickle.load(f)
cases = [
    "Critical production server outage. All customers cannot access the service.",
    "Please explain the charge shown on my latest invoice.",
    "I suggest adding dark mode in a future version."
]
pred = model.predict(cases)
proba = model.predict_proba(cases)
for i, (p, probs) in enumerate(zip(pred, proba), 1):
    print(f"Case {i}: {p} (confidence {probs.max():.2%})")
