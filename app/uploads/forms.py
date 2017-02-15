from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class UploadForm(Form):
    uploadFile = FileField(validators=[FileRequired()])
