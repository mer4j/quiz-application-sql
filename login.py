# Author: mer4j  from github

import sqlite3

def username_exists(username, table):
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    query = f"SELECT COUNT(*) FROM {table} WHERE username = ?"
    c.execute(query, (username,))
    result = c.fetchone()[0]
    conn.close()
    return result > 0

def teacher_login(user, key, email, phone):
    if username_exists(user, "teacher"):
        #print(f"Username '{user}' already exists.")
        return
    conn = None
    try:
        conn = sqlite3.connect("quiz.db")
        c = conn.cursor()
        query = "INSERT INTO teacher (username, password, email, phone_number) VALUES (?, ?, ?, ?)"
        c.execute(query, (user, key, email, phone))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def student_login(name, user, key, email):
    if username_exists(user, "student"):
        #print(f"Username '{user}' already exists.")
        return
    conn = None
    try:
        conn = sqlite3.connect("quiz.db")
        c = conn.cursor()
        query = "INSERT INTO student (username, password, name, email) VALUES (?, ?, ?, ?)"
        c.execute(query, (user, key, name, email))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


