# TicketSense

TicketSense predicts support-ticket **priority** from multilingual ticket text.

## Dataset
Uses `dataset-tickets-multi-lang3-4k.csv` from the supplied archive, copied to `data/dataset.csv`.

## Pipeline
- Load and inspect shape, head, and dtypes
- EDA: nulls, `describe()`, `value_counts()`, and target grouping
- Clean missing subject/body values
- 80/20 stratified train/test split
- TF-IDF text features
- Class-balanced Logistic Regression classifier
- Save trained model as `model.pkl`
- Predict 3 real-world example cases
- Save 3 charts as PNG

## Accuracy
Measured test accuracy: **57.63%**

## Run
```bash
pip install -r requirements.txt
python train.py
python predict.py
```

## Files
- `model.py` — full load/EDA/clean/train/evaluate/save pipeline
- `train.py` — retraining entry point
- `predict.py` — loads model and predicts 3 cases
- `model.pkl` — saved trained model
- `charts/` — 3 PNG visualizations
- `requirements.txt` — dependencies
