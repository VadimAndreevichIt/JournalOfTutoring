from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddStudentForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    link = StringField('Ссылка на занятие', validators=[DataRequired()])
    class_student = StringField('Класс')
    data1 = StringField('Понедельник')
    data2 = StringField('Вторник')
    data3 = StringField('Среда')
    data4 = StringField('Четверг')
    data5 = StringField('Пятница')
    data6 = StringField('Суббота')
    data7 = StringField('Воскресенье')
    submit = SubmitField('Сохранить')