from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from . import uploads
from .forms import UploadForm

# @uploads.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if form.validate_on_submit():
#         f = form.PhotoForm.
