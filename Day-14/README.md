# TicketSense

An AI-assisted customer support ticket triage website. A visitor describes
their issue in plain language; the site predicts the right support queue,
priority level and ticket type, saves it to a database, and surfaces it on
a live dashboard.

## Stack

- **Backend:** Python, Flask
- **Database:** SQLite (file-based, zero setup — created automatically on first run)
- **ML:** scikit-learn (TF-IDF vectorizer + Logistic Regression classifiers)
- **Frontend:** HTML, CSS, vanilla JavaScript (no build step)

## A note on the uploaded model file

`model__1_.pkl` from your upload is a plain scikit-learn `LinearRegression`
that expects 4 unlabelled numeric inputs — it has no connection to raw
ticket text, so it can't power the "read a ticket and classify it" feature
this site needed. Instead, `training/train_model.py` trains three fresh
classifiers directly on your `dataset-tickets-multi-lang-4-20k.csv`
(one each for **queue**, **priority**, and **type**), using a shared TF-IDF
vectorizer. The trained models are already included under
`backend/models/`, so you don't have to retrain anything to run the site.

Rough validation accuracy on a held-out 15% split: type ~77%, priority ~50%,
queue ~39% (queue has 10 overlapping classes and is inherently the hardest
of the three — this is a realistic result for a from-scratch text
classifier, not a bug).

## Project structure

```
TicketSense/
├── backend/
│   ├── app.py              # Flask routes + JSON API
│   ├── database.py         # SQLite schema + queries
│   ├── ml_predictor.py     # Loads models, runs predictions
│   ├── requirements.txt
│   ├── models/
│   │   ├── vectorizer.pkl
│   │   └── classifiers.pkl
│   ├── templates/
│   │   ├── base.html       # header + footer shared layout
│   │   ├── index.html      # hero, how it works, features, live demo, contact
│   │   └── dashboard.html  # ticket table, filters, stats
│   └── static/
│       ├── css/style.css
│       └── js/ (main.js, home.js, dashboard.js)
└── training/
    ├── train_model.py                       # retrain from scratch if you want
    └── dataset-tickets-multi-lang-4-20k.csv
```

## Running it

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

- `/` — marketing homepage with a working live-demo ticket form
- `/dashboard` — live table of every ticket that's been submitted, with
  search + filters and inline status updates
- The SQLite database (`ticketsense.db`) is created automatically inside
  `backend/` the first time you run the app.

## Retraining the model (optional)

```bash
cd training
python train_model.py
```

This overwrites `backend/models/vectorizer.pkl` and `classifiers.pkl`.
Swap in your own labeled ticket CSV (same column names: `subject`, `body`,
`queue`, `priority`, `type`) to retrain on different data.

## API reference

| Method | Route                          | Purpose                          |
|--------|---------------------------------|-----------------------------------|
| GET    | `/api/tickets`                  | List tickets (filters: `status`, `queue`, `priority`, `q`) |
| POST   | `/api/tickets`                  | Submit + classify a new ticket   |
| PATCH  | `/api/tickets/<ref>/status`     | Update a ticket's status         |
| GET    | `/api/stats`                    | Dashboard summary counts         |
| POST   | `/api/contact`                  | Store a contact-form message     |
