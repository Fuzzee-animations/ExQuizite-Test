from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS questions (question_id INTEGER PRIMARY KEY AUTOINCREMENT, question_text TEXT, options TEXT, correct TEXT, quiz TEXT)")
conn.commit()
conn.close()
    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_questions")
def get_questions():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    result = cursor.fetchall()
    return jsonify(result)

@app.route("/add_question")
def add_question():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    question_text = request.args.get("question_text")
    options = request.args.get("options")
    correct = request.args.get("correct")
    quiz = request.args.get("quiz")
    cursor.execute("INSERT INTO questions (question_text, options, correct, quiz) VALUES (?, ?, ?, ?)", [question_text, options, correct, quiz])
    conn.commit()
    return "success!"

@app.route("/delete_question")
def delete_question():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    question_id = request.args.get("id")
    cursor.execute("DELETE FROM questions WHERE question_id = ?", [question_id])
    conn.commit()
    return "success!"

@app.route("/update")
def update():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    id = request.args.get("id")
    question_text = request.args.get("question_text")
    options = request.args.get("options")
    correct = request.args.get("correct")
    quiz = request.args.get("quiz")
    cursor.execute("UPDATE questions SET question_text = ?, options = ?, correct = ?, quiz = ? WHERE question_id = ?", [question_text, options, correct, quiz, id])
    conn.commit()
    return "success!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
