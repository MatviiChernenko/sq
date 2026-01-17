import sqlite3

conn = None
curs = None

def open():
    global conn, curs
    conn = sqlite3.connect("quiz.sqlite")
    curs = conn.cursor()

def close():
    curs.close()
    conn.close()

def do(request):
    curs.execute(request)
    conn.commit()

def clea_db():
    open()
    do("DROP TABLE IF EXISTS quiz_content")
    do("DROP TABLE IF EXISTS question")
    do("DROP TABLE IF EXISTS quiz")
    close()

def create():
    open()
    curs.execute("PRAGMA foreign_keys= on")
    do("""
       CREATE TABLE IF NOT EXISTS quiz(
       id INTEGER PRIMARY KEY,
       name VARCHAR)
       """)
    do("""
        CREATE TABLE IF NOT EXISTS question(
       id INTEGER PRIMARY KEY,
       question VARCHAR,
       right_answer VARCHAR,
       wrong_answer1 VARCHAR,
       wrong_answer2 VARCHAR,
       wrong_answer3 VARCHAR)
       """)
    do("""
       CREATE TABLE IF NOT EXISTS quiz_content(
       id INTEGER PRIMARY KEY,
       quiz_id INT,
       question_id INT,
       FOREIGN KEY (quiz_id) REFERENCES quiz(id),
       FOREIGN KEY (question_id) REFERENCES question(id))
       """)
    close()
def add_question():
    question =[
        ("Скількі зубів в дорослої людини","32","30","25","40"),
        
        ("Коли день незалежності","24 серпня","1 вересня","20 червня","16 лютого"),
        ("Скількі років існує день незалежності","34","25","50","9"),

        ("Коли придумали футбол","1863","1945","1799","2000"),
        ("Хто найпопулярнішій футболіст","Кріштіану Роналду","Ліонель Мессі","Андрій Шевченко","Олег Блохін")
    ]
    open()
    curs.executemany("""
                INSERT INTO question(question, right_answer, wrong_answer1, wrong_answer2, wrong_answer3)
                VALUES(?,?,?,?,?)
                     """,question)
    conn.commit()
    close()
def add_quiz():
    quiz = [
        ("Біологія",),
        ("Незалежність",),
        ("Футбол",)
    ]
    open()
    curs.executemany("""
                INSERT INTO quiz(name)
                VALUES (?)
                    """,quiz)
    conn.commit()
    close()

def add_links():
    links = [
        (1, 1), (2, 2), (2, 3), (3, 4), (3, 5)
    ]
    open()
    curs.executemany("""
                        INSERT INTO quiz_content (quiz_id, question_id)
                        VALUES (?,?)
                     """,links)
    conn.commit()
    close()

def show_quiz():
    open()
    curs.execute("SELECT id, name FROM quiz")
    result = curs.fetchall()
    close()
    return result

def next_question(quiz,question):
    open()
    curs.execute("""SELECT question.id, question.question, question.right_answer,question.wrong_answer1,question.wrong_answer2,question.wrong_answer3
                 FROM question, quiz_content
                 WHERE question.id == (?) AND quiz_content.quiz_id == (?) AND quiz_content.question_id == question.id""", (question,quiz))
    result = curs.fetchall()
    close()
    return result

def main():

    clea_db()
    create()
    add_question()
    add_quiz()
    add_links()

if __name__ == "__main__":
    #main()
    print(next_question(1,1))
