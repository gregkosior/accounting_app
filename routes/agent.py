from flask import Blueprint, render_template, request, redirect, url_for
import os
from config import Config
from services.analysis_service import analyze_data
from services.file_loader import load_file

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/agent', methods=['GET', 'POST'])
def agent():
    step = int(request.form.get('step', 1))
    files = [f for f in os.listdir(Config.UPLOAD_FOLDER) if f.endswith('.csv') or f.endswith('.xlsx')] if os.path.exists(Config.UPLOAD_FOLDER) else []
    selected_file = request.form.get('file_path')
    filter_type = request.form.get('filter_type')
    filter_value = request.form.get('filter_value')
    report_type = request.form.get('report_type')
    results = None
    analysis_results = None
    df = None
    available_months = []
    available_days = []
    next_step = step
    message = None

    if request.method == 'POST':
        if step == 1:
            if selected_file:
                next_step = 2
            else:
                message = 'Musisz wybrać plik do analizy.'
                next_step = 1
        elif step == 2:
            if filter_type:
                next_step = 3
            else:
                message = 'Musisz wybrać zakres analizy.'
                next_step = 2
        elif step == 3:
            if not selected_file:
                message = 'Musisz wybrać plik do analizy.'
                next_step = 1
            elif not report_type:
                message = 'Musisz wybrać typ raportu.'
                next_step = 3
            else:
                # Wykonaj analizę i zaproponuj eksport
                full_path = os.path.join(Config.UPLOAD_FOLDER, selected_file)
                df = load_file(full_path)
                if filter_type == 'all':
                    analysis_results = analyze_data(df)
                else:
                    analysis_results = analyze_data(df, filter_type, filter_value)
                results = analysis_results['kpi']
                available_months = analysis_results['available_months']
                available_days = analysis_results['available_days']
                message = 'Analiza zakończona. Czy chcesz wygenerować raport PDF lub Excel?'
                next_step = 4
        elif step == 4:
            # Przekieruj do eksportu
            if request.form.get('export_pdf'):
                return redirect(url_for('analysis.export_pdf'))
            elif request.form.get('export_excel'):
                return redirect(url_for('analysis.export_excel'))
            else:
                next_step = 1

    return render_template('agent.html', step=next_step, files=files, selected_file=selected_file, filter_type=filter_type, filter_value=filter_value, report_type=report_type, results=results, available_months=available_months, available_days=available_days, message=message)
