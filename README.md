📊 NumPy & Pandas Practice Exercises

📖 Overview

This repository contains **six beginner-friendly Python exercises** designed to help learners understand the fundamentals of **NumPy** and **Pandas**. The exercises focus on working with arrays, DataFrames, CSV files, missing values, grouping data, and performing basic **Exploratory Data Analysis (EDA)**.

These hands-on tasks are ideal for students and beginners starting their journey in Python for data analysis.

📂 Exercises Included

1️⃣ NumPy Marks Analyzer

🎯 Objective

Create a NumPy array containing the marks of 10 students and compute basic statistics.

📚 Concepts Covered

* Creating NumPy arrays
* Mean
* Maximum & Minimum
* Standard Deviation
* Boolean Filtering
* Counting values

🔍 Tasks

* Store marks in a NumPy array.
* Calculate the average marks.
* Find the highest and lowest marks.
* Compute the standard deviation.
* Count the number of students who passed (marks ≥ 50).
* Display a summary report.

Sample Output

text
Average Marks : 65.3
Highest Marks : 92
Lowest Marks  : 38
Passed        : 8
Failed        : 2

 2️⃣ DataFrame Builder

🎯 Objective

Create a Pandas DataFrame manually and perform basic inspection.

📚 Concepts Covered

* Creating DataFrames
* Viewing rows
* Checking shape
* Data types
* Adding new columns

🔍 Tasks

* Create a DataFrame of five students.
* Display the first few rows.
* Show the DataFrame shape.
* Display column data types.
* Add a **Result** column indicating **Pass** or **Fail** based on marks.

Sample Output

| Name  | Age | City     | Marks | Result |
| ----- | --: | -------- | ----: | ------ |
| Alice |  20 | New York |    85 | Pass   |
| Bob   |  21 | Chicago  |    45 | Fail   |

---

3️⃣ CSV Explorer

🎯 Objective

Learn how to load and inspect a CSV dataset.

📚 Concepts Covered

* Reading CSV files
* Dataset inspection
* Viewing rows
* Column names
* Value counts

🔍 Tasks

Load the **student-mat.csv** dataset and display:

* Dataset shape
* Column names
* First three rows
* Last three rows
* Count of students with internet access

Functions Used

* `pd.read_csv()`
* `head()`
* `tail()`
* `value_counts()`

4️⃣ Missing Data Detective

🎯 Objective

Detect and handle missing values in a dataset.

📚 Concepts Covered

* Finding null values
* Filling missing numeric values
* Filling missing text values

🔍 Tasks

* Identify missing values in every column.
* Replace missing numeric values with the column mean.
* Replace missing text values with **"Unknown"**.
* Verify that all missing values have been handled.

Functions Used

* `isnull()`
* `fillna()`
* `select_dtypes()`

---

5️⃣ Group & Compare

🎯 Objective

Analyze student performance using grouping operations.

📚 Concepts Covered

* GroupBy
* Mean
* Sorting
* Largest values

🔍 Tasks

* Calculate the average final grade (**G3**) based on study time.
* Calculate the average grade by gender.
* Display the top five students with the highest final grades.

Functions Used

* `groupby()`
* `mean()`
* `nlargest()`

---

6️⃣ Full EDA Report

🎯 Objective

Create a reusable function for basic Exploratory Data Analysis (EDA).

📚 Concepts Covered

* Functions
* Data inspection
* Descriptive statistics
* Missing value analysis
* Categorical analysis

🔍 Tasks

The `eda_report(df)` function automatically displays:

* Dataset shape
* Missing values
* Statistical summary
* Value counts for categorical columns

Example

```python
eda_report(df)
```

---

🛠 Technologies Used

* Python 3.x
* NumPy
* Pandas

---

# 📁 Project Structure

```text
Project/
│
├── student-mat.csv
├── cloudwatch_server_resource_anomaly_predictor_100k.csv
├── numpy_marks.py
├── dataframe_builder.py
├── csv_explorer.py
├── missing_data.py
├── group_compare.py
├── eda_report.py
└── README.md
```

---

▶️ Getting Started

Install Dependencies

```bash
pip install numpy pandas
```

Run Any Exercise

```bash
python numpy_marks.py
```

or

```bash
python eda_report.py
```

---

🎯 Learning Outcomes

By completing these exercises, you will be able to:

* Create and manipulate NumPy arrays.
* Build and modify Pandas DataFrames.
* Read and inspect CSV datasets.
* Detect and handle missing values.
* Perform group-based data analysis.
* Generate reusable EDA reports.
* Understand the fundamentals of Python-based data analysis.

---

💡 Notes

* Keep the CSV files in the same directory as the Python scripts.
* If your dataset contains different column names, update the code accordingly.
* The `eda_report()` function is reusable and works with any Pandas DataFrame.

---

🚀 Future Improvements

Possible enhancements for this project include:

* Data visualization using Matplotlib and Seaborn.
* Correlation heatmaps.
* Feature engineering examples.
* Data filtering and sorting exercises.
* Exporting cleaned datasets to CSV.
* Interactive notebooks using Jupyter.

---

📚 Conclusion

These exercises provide a practical introduction to **NumPy** and **Pandas**, covering essential data analysis workflows such as array manipulation, DataFrame operations, CSV handling, data cleaning, grouping, and exploratory data analysis. Together, they build a strong foundation for further learning in **Data Analytics**, **Machine Learning**, and **Data Science**.
