import sqlite3

from flask import Flask, render_template, redirect, request
from data import db_session, student
from data.student import Student
from data.user import User
from forms.add_info_student import AddInfoForm
from forms.login_form import LoginForm
from forms.new_student import AddStudentForm
from data import func_student
from flask_login import LoginManager, login_user, login_required, logout_user
import pyperclip
import datetime
from waitress import serve


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'sdwe12eef4f231sdf313f32313'
daysofweek = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(1)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template("main.html")


@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_page():
    if request.method == "POST":
        if "lp" in request.form:
            sp = request.form["lp"].split('-')
            rez = f'Логин: {sp[1] + sp[0]} \nПароль: {sp[0] + sp[1]}'
            pyperclip.copy(rez)
        elif 'setting' in request.form:
            sp = request.form["setting"].split('-')
            return redirect(f"/change_student/{sp[0]}")
        else:
            for i in request.form:
                id = i
            return redirect(f"/journal_student/{id}")
    db_sess = db_session.create_session()
    studets = db_sess.query(Student).all()
    st = []
    for i in studets:
        st.append(i.get_info())
    db_sess.close()
    return render_template("students_page.html", students=st, days=daysofweek)


@app.route('/change_student/<id>', methods=['GET', 'POST'])
@login_required
def change_student(id):
    form = AddStudentForm()
    if request.method == "POST":
        conn = sqlite3.connect("db/students.db")
        cur = conn.cursor()
        data_lesson = func_student.get_time_lessons(daysofweek, [form.data1.data, form.data2.data, form.data3.data,
                                                                 form.data4.data, form.data5.data, form.data6.data,
                                                                 form.data7.data])
        name = form.username.data
        phone = form.phone.data
        link = form.link.data
        class_student = form.class_student.data
        cur.execute(f''' UPDATE students 
        SET phone = "{phone}",
            link = "{link}",
            name = "{name}",
            data_lesson = "{data_lesson}",
            class_student= "{class_student}"
            WHERE id = "{str(id)}";
        ''')
        cur.execute(f''' UPDATE users
                SET login = "{name + str(id)}",
                    hashed_password = "{func_student.hash_password(str(id) + name)}",
                    name = "{name}"
                    WHERE id = "{str(id)}";
                ''')
        conn.commit()
        conn.close()
        return redirect(f"/schedule")

    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == str(id)).first()
    db_sess.close()
    sl = {}
    for i in daysofweek:
        sl[i] = ""
    sp = student.data_lesson.split(';')
    for i in sp:
        temp = i.split('-')
        sl[temp[0]] = temp[1]
    return render_template("change_student.html", form=form, student=student, data_lesson=sl)


@app.route('/journal_student/<id>', methods=['GET', 'POST'])
@login_required
def journal_student(id):
    db_sess = db_session.create_session()
    studets = db_sess.query(Student).all()
    st = []
    for i in studets:
        st.append(i.get_info())
    db_sess.close()
    st_active = []
    for i in st:
        if i[0] == id:
            st_active = i
            break
    stutent_info = func_student.get_student_info(id)
    for i in range(len(stutent_info)):
        stutent_info[i] = list(stutent_info[i])
        if stutent_info[i][6] == '':
            stutent_info[i].append( 'не выполнено')
        elif int(stutent_info[i][6]) < 60:
            stutent_info[i].append('3')
        elif int(stutent_info[i][6]) <= 75:
            stutent_info[i].append('4')
        elif int(stutent_info[i][6]) < 100:
            stutent_info[i].append('5')
    return render_template("journal_student_page.html", student_active=st_active,
                           stutent_info=stutent_info)


@app.route('/delete_student/<id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    if request.method == "POST":
        if 'no' in request.form:
            return redirect("/schedule")
        elif 'yes' in request.form:
            conn = sqlite3.connect("db/students.db")
            cur = conn.cursor()
            cur.execute(f''' DELETE FROM students 
                WHERE id = "{str(id)}";   
            ''')
            cur.execute(f''' DELETE FROM users 
                            WHERE id = "{str(id)}";   
            ''')
            cur.execute(f'''DROP TABLE {"user" + str(id)}
            ''')
            conn.commit()
            conn.close()
            return redirect("/schedule")

    db_sess = db_session.create_session()
    user = db_sess.query(Student).filter(Student.id == str(id)).first()
    db_sess.close()
    return render_template("delete_student.html", user=user)


@app.route('/change_info/<id>/<id_inf>', methods=['GET', 'POST'])
@login_required
def change_info(id, id_inf):
    if request.method == 'POST':
        if 'delete' in request.form:
            func_student.delete_info(id, id_inf)
        else:
            level = "-"
            if 'r1' in request.form:
                level = "Превосходит ожидания"
            elif "r2" in request.form:
                level = "Соотвествует ожиданиям"
            elif "r3" in request.form:
                level = "Не соотвествует ожиданиям"
            func_student.change_info(request.form, id, id_inf, level)
        return redirect(f'/journal/{id}')
    form = AddInfoForm()
    db_sess = db_session.create_session()
    user = db_sess.query(Student).filter(Student.id == str(id)).first()
    db_sess.close()
    info = func_student.get_info(id, id_inf)
    return render_template(f"change_info.html", form=form, user=user, info=info)


@app.route('/journal/<id>', methods=['GET', 'POST'])
@login_required
def journal(id):
    form = AddInfoForm()
    if request.method == "POST":
        if 'change' in request.form:
            return redirect(f'/change_info/{id}/{request.form["change"]}')
        else:
            sl = {}
            sl["data"] = form.data.data
            sl["topic"] = form.topic.data
            sl["comment"] = form.comment.data
            sl["homework"] = form.homework.data
            sl["homework mark"] = form.homework_mark.data
            if 'r1' in request.form:
                sl["level"] = "Превосходит ожидания"
            elif "r2" in request.form:
                sl["level"] = "Соотвествует ожиданиям"
            elif "r3" in request.form:
                sl["level"] = "Не соотвествует ожиданиям"
            else:
                sl["level"] = "-"
            func_student.add_student_new_info(id, sl)

    db_sess = db_session.create_session()
    studets = db_sess.query(Student).all()
    st = []
    for i in studets:
        st.append(i.get_info())
    db_sess.close()
    if id == '0':
        return render_template("journal_page.html", students=st, href="/journal/", indentificator=id)
    else:
        st_active = []
        for i in st:
            if i[0] == id:
                st_active = i
                break
        stutent_info = func_student.get_student_info(id)
        return render_template("journal_page.html", students=st, href="/journal/",
                               indentificator=id, student_active=st_active, stutent_info=stutent_info,
                               form=form, today=datetime.datetime.now().strftime("%d.%m.%Y"))


@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            id = db_sess.query(Student).all()[-1].id + 1
        except Exception:
            id = 1
        new_student = Student()
        data_lesson = func_student.get_time_lessons(daysofweek, [form.data1.data, form.data2.data, form.data3.data,
                                                                 form.data4.data, form.data5.data, form.data6.data,
                                                                 form.data7.data])
        new_student.name = form.username.data
        new_student.phone = form.phone.data
        new_student.link = form.link.data
        new_student.data_lesson = data_lesson
        new_student.class_student = form.class_student.data
        db_sess.add(new_student)
        db_sess.commit()
        db_sess.close()

        conn = sqlite3.connect("db/students.db")
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE {"user" + str(id)} (
            id  INT PRIMARY KEY,
            data_lesson TEXT,
            topic TEXT,
            comment TEXT,
            level TEXT,
            homework TEXT,
            homework_mark TEXT) ''')

        cur.execute(f''' INSERT INTO users (login, hashed_password, type, name) 
            VALUES ("{form.username.data + str(id)}", 
            "{str(func_student.hash_password(str(id) + form.username.data))}", 2, "{form.username.data}");
        ''')
        conn.commit()
        conn.close()
        return redirect('/schedule')
    return render_template("add_student.html", form=form)


if __name__ == '__main__':
    db_session.global_init("db/students.db")
    #app.run(port=5000, host='127.0.0.1', debug=True)
    serve(app, host='0.0.0.0', port=5000)