from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField

# WTForm for creating a slot post
class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[Length(min=1, max=250)])
    date_start = DateField("Start Date", validators=[DataRequired()])
    date_end = DateField("End Date", validators=[DataRequired()])
    rating = SelectField("Rating", choices=["1", "2", "3", "4", "5"], validators=[DataRequired()])
    description = StringField("Description", validators=[Length(min=1, max=500)])
    location = StringField("Location", validators=[DataRequired(), URL()])
    internet_rating = SelectField("Internet Rating", choices=["1", "2", "3", "4"], validators=[DataRequired()])
    submit = SubmitField("Submit Post")


