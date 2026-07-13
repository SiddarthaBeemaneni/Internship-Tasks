from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE="expense.db"

def get_db():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def create_table():
    conn=get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, amount REAL, category TEXT,
    payment_mode TEXT, expense_date TEXT, description TEXT)""")
    conn.commit(); conn.close()
create_table()

@app.route("/")
def home():
    conn=get_db()
    total=conn.execute("SELECT COALESCE(SUM(amount),0) FROM expenses").fetchone()[0]
    count=conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    recent=conn.execute("SELECT * FROM expenses ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    return render_template("index.html",total=total,count=count,recent=recent)

@app.route("/add-expense",methods=["GET","POST"])
def add_expense():
    if request.method=="POST":
        f=request.form
        conn=get_db()
        conn.execute("INSERT INTO expenses(title,amount,category,payment_mode,expense_date,description) VALUES(?,?,?,?,?,?)",
        (f["title"],f["amount"],f["category"],f["payment"],f["date"],f["description"]))
        conn.commit(); conn.close()
        return redirect("/expenses")
    return render_template("add_expense.html")

@app.route("/expenses")
def expenses():
    s=request.args.get("search","")
    c=request.args.get("category","")
    q="SELECT * FROM expenses WHERE 1=1"; p=[]
    if s: q+=" AND title LIKE ?"; p.append("%"+s+"%")
    if c: q+=" AND category=?"; p.append(c)
    conn=get_db(); data=conn.execute(q,p).fetchall(); conn.close()
    return render_template("expenses.html",expenses=data)

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    conn=get_db()
    if request.method=="POST":
        f=request.form
        conn.execute("UPDATE expenses SET title=?,amount=?,category=?,payment_mode=?,expense_date=?,description=? WHERE id=?",
        (f["title"],f["amount"],f["category"],f["payment"],f["date"],f["description"],id))
        conn.commit(); conn.close()
        return redirect("/expenses")
    e=conn.execute("SELECT * FROM expenses WHERE id=?",(id,)).fetchone()
    conn.close()
    return render_template("edit_expense.html",expense=e)

@app.route("/delete/<int:id>")
def delete(id):
    conn=get_db(); conn.execute("DELETE FROM expenses WHERE id=?",(id,)); conn.commit(); conn.close()
    return redirect("/expenses")

@app.route("/summary")
def summary():
    conn=get_db()
    total=conn.execute("SELECT COALESCE(SUM(amount),0) FROM expenses").fetchone()[0]
    highest=conn.execute("SELECT * FROM expenses ORDER BY amount DESC LIMIT 1").fetchone()
    category=conn.execute("SELECT category,COUNT(*) count FROM expenses GROUP BY category").fetchall()
    recent=conn.execute("SELECT * FROM expenses ORDER BY expense_date DESC LIMIT 5").fetchall()
    conn.close()
    return render_template("summary.html",total=total,highest=highest,category=category,recent=recent)

if __name__=="__main__":
    app.run(debug=True)
