from pathlib import Path
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE = Path(__file__).resolve().parent

def load_data():
    df = pd.read_csv(BASE / "data" / "dataset.csv")
    print("Shape:", df.shape)
    print(df.head())
    print(df.dtypes)
    return df

def eda(df):
    print("\nNulls:\n", df.isnull().sum())
    print("\nDescribe:\n", df.describe(include="all").T)
    for c in ["priority", "language", "type", "queue"]:
        print(f"\n{c}:\n", df[c].value_counts(dropna=False))
    print("\nPriority by language:\n", pd.crosstab(df["language"], df["priority"]))
    # Observation 1: The dataset is multilingual.
    # Observation 2: Priority has low, medium, and high classes.
    # Observation 3: Subject and body contain the main predictive text.
    # Observation 4: Ticket types and queues vary across the dataset.
    # Observation 5: Several tag columns contain many missing values.

def clean_data(df):
    df = df.copy()
    df["subject"] = df["subject"].fillna("")
    df["body"] = df["body"].fillna("")
    df["priority"] = df["priority"].fillna(df["priority"].mode()[0])
    print("Nulls in model columns after cleaning:",
          df[["subject","body","priority"]].isnull().sum().sum())
    return df

def train_model(df):
    X = (df["subject"] + " " + df["body"]).str.strip()
    y = df["priority"].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y)
    model = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=6000, ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=500, class_weight="balanced"))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, pred))
    with open(BASE / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    return acc

if __name__ == "__main__":
    df = clean_data(load_data())
    eda(df)
    train_model(df)
