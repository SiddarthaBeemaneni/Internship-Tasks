from flask import Flask, render_template, request
import numpy as np
import joblib

app=Flask(__name__)
model=joblib.load("model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    f1=float(request.form["feature1"])
    f2=float(request.form["feature2"])
    f3=float(request.form["feature3"])
    f4=float(request.form["feature4"])
    pred=model.predict(np.array([[f1,f2,f3,f4]]))
    return render_template("result.html", prediction_text=f"Prediction: {pred[0]}")

if __name__=="__main__":
    app.run(debug=True)
