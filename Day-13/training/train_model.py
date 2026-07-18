import pandas as pd, pickle, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import os
DATA_PATH = os.path.join(os.path.dirname(__file__), 'dataset-tickets-multi-lang-4-20k.csv')
df = pd.read_csv(DATA_PATH)
df['subject'] = df['subject'].fillna('')
df['body'] = df['body'].fillna('')
df['text'] = (df['subject'] + ' ' + df['body']).str.strip()
df = df[df['text'].str.len() > 3].reset_index(drop=True)

def clean(t):
    t = re.sub(r'<[^>]+>', ' ', str(t))
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

df['text'] = df['text'].apply(clean)

X = df['text']
targets = ['queue', 'priority', 'type']
results = {}

vectorizer = TfidfVectorizer(max_features=8000, ngram_range=(1,2), min_df=2, sublinear_tf=True)
X_vec = vectorizer.fit_transform(X)

models = {}
for t in targets:
    y = df[t]
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.15, random_state=42, stratify=y)
    clf = LogisticRegression(max_iter=1000, class_weight='balanced', C=2.0)
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(t, 'accuracy:', round(acc,3))
    models[t] = clf

out_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models')
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, 'vectorizer.pkl'), 'wb') as f:
    pickle.dump(vectorizer, f)
with open(os.path.join(out_dir, 'classifiers.pkl'), 'wb') as f:
    pickle.dump(models, f)

print('Saved models.')
