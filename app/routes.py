from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    render_template
)
from .models import File
from .forms.upload_form import UploadForm
from .forms.password_form import PasswordForm
from app.services.file_upload_service import handle_file_upload
from app.services.file_download_service import handle_file_download

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        file_record = handle_file_upload(form.file.data, form.password.data)
        file_url = url_for('main.get_file', uuid=file_record.uuid)
        return render_template('upload_success.html', file_url=file_url)

    return render_template('index.html', form=form)

@bp.route('/get-file/<uuid>', methods=['GET', 'POST'])
def get_file(uuid):
    file_record = File.query.filter_by(uuid=uuid).first_or_404()
    form = PasswordForm()

    if form.validate_on_submit():
        return handle_file_download(file_record, form.password.data)

    return render_template('password_prompt.html', uuid=uuid, form=form)
