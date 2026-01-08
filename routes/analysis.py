from flask import send_file, make_response
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
import xlsxwriter
from flask import Blueprint, render_template, request
import os
from config import Config
from services.analysis_service import analyze_data
from services.file_loader import load_file
from services.charts_service import generate_line_chart, generate_bar_chart

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analysis', methods=['GET', 'POST'])
def analysis():
    files = []
    results = None
    df = None
    chart_income = None
    chart_balance = None
    selected_file = None
    filter_type = None
    filter_value = None
    available_months = []
    available_days = []
    analysis_results = None
    monthly_data = None
    daily_data = None
    trend_data = None
    category_data = None
    filtered_df = None

    if os.path.exists(Config.UPLOAD_FOLDER):
        files = [f for f in os.listdir(Config.UPLOAD_FOLDER) if f.endswith('.csv') or f.endswith('.xlsx')]

    if request.method == 'POST':
        import datetime
        file_path = request.form.get('file_path')
        filter_type = request.form.get('filter_type', 'all')
        filter_value = request.form.get('filter_value')
        
        selected_file = file_path
        if file_path:
            full_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
            df = load_file(full_path)
            
            # Użyj nowej funkcji analizy z filtrowaniem
            if filter_type == 'all':
                analysis_results = analyze_data(df)
            else:
                analysis_results = analyze_data(df, filter_type, filter_value)
            
            # Wyodrębnij wyniki
                results = analysis_results['kpi']
                available_months = analysis_results['available_months']
                available_days = analysis_results['available_days']
                monthly_data = analysis_results['monthly']
                daily_data = analysis_results['daily']
                trend_data = analysis_results['trend']
                category_data = analysis_results['category_analysis']
                filtered_df = analysis_results['filtered_df']
            
            # Wykres przychodów/kosztów w czasie
            if monthly_data is not None and not monthly_data.empty:
                chart_income = 'static/income_chart.png'
                # Przygotuj dane do wykresu
                plot_df = monthly_data[['Miesiąc', 'Suma przychodów', 'Suma kosztów']]
                import matplotlib.pyplot as plt
                plt.figure(figsize=(10, 6))
                plt.plot(plot_df['Miesiąc'], plot_df['Suma przychodów'], marker='o', label='Przychody')
                plt.plot(plot_df['Miesiąc'], plot_df['Suma kosztów'], marker='s', label='Koszty')
                plt.xlabel('Miesiąc')
                plt.ylabel('Wartość')
                plt.title('Przychody i koszty w czasie')
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(chart_income)
                plt.close()
            
            # Wykres salda miesięcznego
            if monthly_data is not None and not monthly_data.empty:
                chart_balance = 'static/balance_chart.png'
                import matplotlib.pyplot as plt
                plt.figure(figsize=(10, 6))
                colors = ['green' if x >= 0 else 'red' for x in monthly_data['Saldo']]
                plt.bar(monthly_data['Miesiąc'], monthly_data['Saldo'], color=colors)
                plt.xlabel('Miesiąc')
                plt.ylabel('Saldo')
                plt.title('Saldo miesięczne')
                plt.xticks(rotation=45)
                plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                plt.tight_layout()
                plt.savefig(chart_balance)
                plt.close()
            
            # Zapisz analizę do pliku txt
            with open('analysis_history.txt', 'a', encoding='utf-8') as f:
                f.write(f"---\nData: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Plik: {file_path}\n")
                f.write(f"Filtr: {filter_type} = {filter_value}\n")
                if results is not None:
                    for key, value in results.items():
                        f.write(f"{key}: {value}\n")
                f.write("\n")
    
    return render_template('analysis.html', 
                         results=results, 
                         files=files, 
                         selected_file=selected_file, 
                         df=df,
                         chart_income=chart_income, 
                         chart_balance=chart_balance,
                         filter_type=filter_type,
                         filter_value=filter_value,
                         available_months=available_months,
                         available_days=available_days,
                         analysis_results=analysis_results)


# --- Endpointy eksportu PDF/Excel ---

@analysis_bp.route('/analysis/export/pdf', methods=['POST'])
def export_pdf():
    file_path = request.form.get('file_path')
    filter_type = request.form.get('filter_type', 'all')
    filter_value = request.form.get('filter_value')
    if not file_path:
        return "Brak pliku do eksportu", 400
    full_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
    df = load_file(full_path)
    if filter_type == 'all':
        analysis_results = analyze_data(df)
    else:
        analysis_results = analyze_data(df, filter_type, filter_value)
    kpi = analysis_results['kpi']
    # Generowanie PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, y, "Raport finansowy")
    y -= 30
    p.setFont("Helvetica", 12)
    for key, value in kpi.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 18
        if y < 60:
            p.showPage()
            y = height - 40
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="raport.pdf", mimetype='application/pdf')

@analysis_bp.route('/analysis/export/excel', methods=['POST'])
def export_excel():
    file_path = request.form.get('file_path')
    filter_type = request.form.get('filter_type', 'all')
    filter_value = request.form.get('filter_value')
    if not file_path:
        return "Brak pliku do eksportu", 400
    full_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
    df = load_file(full_path)
    if filter_type == 'all':
        analysis_results = analyze_data(df)
    else:
        analysis_results = analyze_data(df, filter_type, filter_value)
    filtered_df = analysis_results['filtered_df']
    kpi = analysis_results['kpi']
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        filtered_df.to_excel(writer, sheet_name='Dane', index=False)
        # KPI na osobnym arkuszu
        kpi_df = pd.DataFrame(list(kpi.items()), columns=['Wskaźnik', 'Wartość'])
        kpi_df.to_excel(writer, sheet_name='Podsumowanie', index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="raport.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
