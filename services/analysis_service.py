import pandas as pd
from services.file_loader import load_file
from services.data_cleaner import clean_data
from services.professional_calculations_service import ProfessionalCalculations

def analyze_data(df, filter_type=None, filter_value=None):
    """
    Analizuj dane z możliwością filtrowania
    
    Args:
        df: DataFrame z danymi
        filter_type: 'month', 'day', 'date_range', lub None
        filter_value: wartość filtra (np. '2024-01' dla miesiąca, '2024-01-15' dla dnia)
    """
    df = clean_data(df)
    
    # Użyj profesjonalnych obliczeń
    calc = ProfessionalCalculations(df)
    
    # Zastosuj filtr jeśli podany
    filtered_df = df
    if filter_type == 'month' and filter_value:
        # Format: YYYY-MM
        year, month = map(int, filter_value.split('-'))
        filtered_df = calc.filter_by_month(year, month)
    elif filter_type == 'day' and filter_value:
        # Format: YYYY-MM-DD
        year, month, day = map(int, filter_value.split('-'))
        filtered_df = calc.filter_by_day(year, month, day)
    elif filter_type == 'date_range' and filter_value:
        # Format: YYYY-MM-DD,YYYY-MM-DD
        start_date, end_date = filter_value.split(',')
        filtered_df = calc.filter_by_date_range(start_date, end_date)
    
    # Oblicz KPI dla przefiltrowanych danych
    kpi = calc.calculate_kpi(filtered_df)
    
    # Oblicz analizę trendów
    trend = calc.calculate_trend()
    
    # Analiza miesięczna
    monthly = calc.calculate_monthly_summary()
    
    # Analiza dzienna
    daily = calc.calculate_daily_summary()
    
    # Analiza kategorii
    category_analysis = calc.calculate_category_analysis()
    
    # Pobierz dostępne okresy
    available_months = calc.get_available_months()
    available_days = calc.get_available_days()
    
    return {
        'kpi': kpi,
        'trend': trend,
        'monthly': monthly,
        'daily': daily,
        'category_analysis': category_analysis,
        'available_months': available_months,
        'available_days': available_days,
        'filtered_df': filtered_df
    }

def analyze_data_legacy(df):
    """Stara wersja funkcji dla kompatybilności wstecznej"""
    df = clean_data(df)
    summary = {}
    if 'income' in df.columns:
        summary['Suma przychodów'] = df['income'].sum()
    if 'expense' in df.columns:
        summary['Suma kosztów'] = df['expense'].sum()
    if 'income' in df.columns and 'expense' in df.columns:
        summary['Saldo'] = df['income'].sum() - df['expense'].sum()
    summary['Liczba transakcji'] = len(df)
    # Analiza miesięczna
    monthly = None
    if 'month' in df.columns and 'income' in df.columns and 'expense' in df.columns:
        monthly = df.groupby('month').agg({'income': 'sum', 'expense': 'sum'})
        monthly['balance'] = monthly['income'] - monthly['expense']
        monthly = monthly.reset_index()
    return summary, monthly
