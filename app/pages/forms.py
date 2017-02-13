from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, DateField, TextField
from wtforms.validators import Optional, Length, Required


class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1,64)])
    location = StringField('Location', validators=[Optional(), Length(1,64)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')

class CreateThreadForm(Form):
    title = TextField(validators=[Required()])
    content = TextAreaField(validators=[Required(), Length(1,512)])
    submit = SubmitField('Post topic')
