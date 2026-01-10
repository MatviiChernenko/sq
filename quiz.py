from flask import Flask, session, redirect, url_for, render_template, request
from db_script import *

def start_quiz(quiz=-1):
    session["quiz"] = quiz
    session["next_question"] = next_question(quiz,0)
    session["result"] = 0
    session["total"] = 0

def quiz_form():
    quiz_list = show_quiz()
    return render_template("index.html", quiz_list= quiz_list)

def index():
    if request.method == "GET":
        start_quiz()
        return quiz_form()
    else:
        quiz_id = request.form.get("quiz")
        start_quiz(quiz_id)
        print(1)
        return redirect(url_for("test"))
    
def equals_question(answer,right_answer):
    if answer == right_answer:
        session["result"] += 1
    session["total"] += 1

def test():
    if not("quiz" in session) or int(session["quiz"]) < 0:
        return redirect(url_for("index"))
    else:
        if request.method == "POST":
            equals_question(request.form.get(), session["next_question"][0][2])
        session["next_question"] = next_question(session["quiz"], session["total"])
        if session["next_question"] is None or len(session["next_question"]) == 0:
            return redirect(url_for("result"))
        else:
            session["total"] += 1
            return render_template("test.html",
                                   question= session["next_question"][0][1],
                                   answer_list= session["next_questioin"][0][2],
                                   question_id= session["next_question"][0][0])

def result():
    return "HELLO"

app = Flask(__name__,template_folder= "template", static_folder= "static")
app.add_url_rule("/", "index", index, methods=["post","get"])
app.add_url_rule("/index", "index", index, methods=["post","get"])
app.add_url_rule("/test", "test", test, methods=["post","get"])
app.add_url_rule("/result", "result", result, methods=["post","get"])
app.secret_key = "32131321"

if __name__ == "__main__":
    app.run()

