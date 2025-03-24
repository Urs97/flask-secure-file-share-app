from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask import current_app

class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def validate_file(form, field):
        filename = field.data.filename
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in current_app.config['ALLOWED_EXTENSIONS']:
            raise ValidationError('Allowed file types are txt, pdf, png, jpg, jpeg, gif.')
