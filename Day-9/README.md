# Machine Learning Classification Model Comparison

Two classifiers are compared on the uploaded multilingual support-ticket dataset.

## Task and preprocessing
- Original rows: 20,000
- Rows used: 20,000
- Target: `queue`
- Features: combined `subject` + `body`
- Classes: 10
- Split: stratified 80/20 (`random_state=42`)
- Representation: TF-IDF unigrams/bigrams, maximum 20,000 features

## Models
1. SGD Logistic Classifier (`SGDClassifier(loss="log_loss")`)
2. Linear SVM (`LinearSVC`)

## Results
| Model | Accuracy | Precision (weighted) | Recall (weighted) | F1-Score (weighted) |
|---|---:|---:|---:|---:|
| SGD Logistic Classifier | 0.4138 | 0.4166 | 0.4138 | 0.4052 |
| Linear SVM | 0.4830 | 0.4853 | 0.4830 | 0.4827 |

## Conclusion
`Linear SVM` performed better overall by weighted F1-score on the held-out test set.

## Run
```bash
pip install pandas scikit-learn matplotlib
python model_comparison.py
```
