from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'csv', 'txt', 'xlsx'], 'Unsupported file format!')
    ])
    submit = SubmitField('Upload')
app/templates/base.html: