from flask import Flask, session, redirect, url_for, render_template, request
from db_script import *
import random

def start_quiz(quiz=-1):
    session["quiz"] = quiz
    session["next_question"] = next_question(quiz)
    session["total"] = len(session["next_question"])
    session["result"] = 0
    session["current_question"] = 0

def quiz_form():
    quiz_list = show_quiz()
    print(quiz_list)
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
    session["current_question"] += 1

def test():
    if not("quiz" in session) or int(session["quiz"]) < 0:
        return redirect(url_for("index"))
    else:
        print(2)
        if request.method == "POST":
            equals_question(request.form.get("answer"), session["next_question"][session["current_question"]-1][2])
        if session["next_question"] is None or session["current_question"] == session["total"]:
            return redirect(url_for("result"))
        else:
            tmp_questions = list(session["next_question"][session["current_question"]][2:])
            print(type(tmp_questions))
            random.shuffle(tmp_questions)
            print(session["next_question"])
            return render_template("test.html",
                                   question= session["next_question"][session["current_question"]][1],
                                   answer_list= tmp_questions,
                                   question_id= session["next_question"][session["current_question"]][0])

def result():
    html = render_template("result.html",right_answer=session["result"],total=session["total"])
    session.clear()
    return html

app = Flask(__name__,template_folder= "template", static_folder= "static")
app.add_url_rule("/", "index", index, methods=["post","get"])
app.add_url_rule("/index", "index", index, methods=["post","get"])
app.add_url_rule("/test", "test", test, methods=["post","get"])
app.add_url_rule("/result", "result", result, methods=["post","get"])
app.secret_key = "32131321"

if __name__ == "__main__":
    app.run()

