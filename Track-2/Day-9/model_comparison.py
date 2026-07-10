"""Multilingual support-ticket queue classification: two-model comparison."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import (confusion_matrix, ConfusionMatrixDisplay, accuracy_score,
    precision_score, recall_score, f1_score, classification_report)

DATASET=Path("dataset-tickets-multi-lang-4-20k(5).csv")
df=pd.read_csv(DATASET)
data=df[["subject","body","queue"]].copy()
data["subject"]=data["subject"].fillna("")
data["body"]=data["body"].fillna("")
data["queue"]=data["queue"].fillna("Unknown").astype(str)
data["text"]=(data["subject"].str.strip()+" "+data["body"].str.strip()).str.strip()
data=data[data["text"].str.len()>0]

X_train_text,X_test_text,y_train,y_test=train_test_split(
    data["text"],data["queue"],test_size=0.20,random_state=42,stratify=data["queue"])

vectorizer=TfidfVectorizer(max_features=20000,ngram_range=(1,2),min_df=2,
    sublinear_tf=True,strip_accents="unicode")
X_train=vectorizer.fit_transform(X_train_text)
X_test=vectorizer.transform(X_test_text)

models={
 "SGD Logistic Classifier":SGDClassifier(loss="log_loss",max_iter=1000,tol=1e-3,
     class_weight="balanced",random_state=42),
 "Linear SVM":LinearSVC(class_weight="balanced",random_state=42)
}
labels=sorted(data["queue"].unique())
summary=[]

for i,(name,model) in enumerate(models.items(),1):
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    acc=accuracy_score(y_test,pred)
    pre=precision_score(y_test,pred,average="weighted",zero_division=0)
    rec=recall_score(y_test,pred,average="weighted",zero_division=0)
    f1=f1_score(y_test,pred,average="weighted",zero_division=0)
    summary.append({"Model":name,"Accuracy":acc,"Precision":pre,"Recall":rec,"F1-Score":f1})
    print(f"\n{name}\n"+"="*70)
    print(f"Accuracy: {acc:.4f}\nPrecision (weighted): {pre:.4f}\nRecall (weighted): {rec:.4f}\nF1-Score (weighted): {f1:.4f}")
    print("\nClassification Report:\n",classification_report(y_test,pred,zero_division=0))
    cm=confusion_matrix(y_test,pred,labels=labels)
    fig,ax=plt.subplots(figsize=(16,14))
    ConfusionMatrixDisplay(cm,display_labels=labels).plot(
        ax=ax,xticks_rotation=90,cmap="Blues",colorbar=False,values_format="d")
    ax.set_title(f"Confusion Matrix — {name}")
    plt.tight_layout()
    plt.savefig(f"confusion_matrix_model{i}.png",dpi=160,bbox_inches="tight")
    plt.close()

summary_df=pd.DataFrame(summary)
print("\nComparison:\n",summary_df.to_string(index=False))
summary_df.to_csv("metrics_comparison.csv",index=False)
