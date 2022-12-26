import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def get_student_info(id):
    name_table = "user" + str(id)
    conn = sqlite3.connect("db/students.db")
    cur = conn.cursor()
    rez = cur.execute(f'''SELECT * FROM {name_table} ''').fetchall()
    conn.close()
    return rez


def change_info(obj, id, id_info, level):
    name_table = "user" + str(id)
    conn = sqlite3.connect("db/students.db")
    cur = conn.cursor()
    cur.execute(f''' UPDATE {name_table}
            SET data_lesson = "{obj['data']}",
                topic = "{obj['topic']}",
                comment = "{obj['comment']}",
                level = "{level}",
                homework = "{obj['homework']}",
                homework_mark = "{obj['homework_mark']}"
                WHERE id = "{str(id_info)}";
            ''')
    conn.commit()
    conn.close()

def delete_info(id, id_inf):
    name_table = "user" + str(id)
    conn = sqlite3.connect("db/students.db")
    cur = conn.cursor()
    cur.execute(f''' DELETE FROM {name_table}
                            WHERE id = "{str(id_inf)}";''')
    conn.commit()
    conn.close()

def get_info(id, id_info):
    name_table = "user" + str(id)
    conn = sqlite3.connect("db/students.db")
    cur = conn.cursor()
    rez = cur.execute(f'''SELECT * FROM {name_table} WHERE id = "{id_info}" ''').fetchone()
    conn.close()
    return rez


def add_student_new_info(id, sl):
    name_table = "user" + str(id)
    conn = sqlite3.connect("db/students.db")
    cur = conn.cursor()
    temp = cur.execute(f'''SELECT * from {name_table}''').fetchall()
    if temp:
        new_id = temp[-1][0] + 1
    else:
        new_id = 1
    cur.execute(f'''INSERT INTO {name_table}(id, data_lesson, topic, comment, level, homework, homework_mark)
                        VALUES("{str(new_id)}",
                                "{sl['data']}",
                                "{sl['topic']}",
                                "{sl['comment']}",
                                "{sl['level']}",
                                "{sl['homework']}",
                                "{sl['homework mark']}" );''')
    conn.commit()
    conn.close()


def get_time_lessons(days, time):
    rez = ""
    for i in range(len(days)):
        if time[i]:
            rez = rez + days[i] + "-" + time[i] + ";"
    return rez[:len(rez) - 1]


def hash_password(password):
    return generate_password_hash(password)


def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)