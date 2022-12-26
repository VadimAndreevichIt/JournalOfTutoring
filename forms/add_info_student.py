from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddInfoForm(FlaskForm):
    data = StringField('Дата занятия', validators=[DataRequired()])
    topic = StringField('Тема', validators=[DataRequired()])
    level = StringField('Уровень', validators=[DataRequired()])
    comment = StringField('Комментарий', validators=[DataRequired()])
    homework = StringField('Домашнее задание', validators=[DataRequired()])
    homework_mark = StringField('Оценка домашнего задания', validators=[DataRequired()])
    submit = SubmitField('Сохранить')