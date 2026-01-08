from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from config import Config

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('Nie wybrano pliku')
            return redirect(request.url)
        if not file.filename:
            flash('Nie wybrano pliku')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS:
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            flash('Plik wgrany poprawnie')
            return redirect(url_for('analysis.analysis'))
        else:
            flash('Nieprawidłowy typ pliku')
            return redirect(request.url)
    return render_template('upload.html')
