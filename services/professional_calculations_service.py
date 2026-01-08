import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ProfessionalCalculations:
    """Profesjonalne obliczenia finansowe i wskaźniki KPI"""
    
    def __init__(self, df):
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Przygotowanie danych - konwersja dat, dodanie kolumn pomocniczych"""
        # Sprawdź czy są kolumny z datami
        date_columns = ['date', 'data', 'Date', 'Data']
        date_col = None
        for col in date_columns:
            if col in self.df.columns:
                date_col = col
                break
        
        if date_col:
            self.df['date'] = pd.to_datetime(self.df[date_col], errors='coerce')
            self.df['year'] = self.df['date'].dt.year
            self.df['month'] = self.df['date'].dt.month
            self.df['day'] = self.df['date'].dt.day
            self.df['month_name'] = self.df['date'].dt.strftime('%Y-%m')
            self.df['day_name'] = self.df['date'].dt.strftime('%Y-%m-%d')
        
        # Standaryzacja kolumn
        if 'income' not in self.df.columns and 'przychod' in self.df.columns:
            self.df['income'] = self.df['przychod']
        if 'expense' not in self.df.columns and 'koszt' in self.df.columns:
            self.df['expense'] = self.df['koszt']
        
        # Wypełnij brakujące wartości
        if 'income' in self.df.columns:
            self.df['income'] = self.df['income'].fillna(0)
        if 'expense' in self.df.columns:
            self.df['expense'] = self.df['expense'].fillna(0)
    
    def filter_by_month(self, year, month):
        """Filtruj dane po roku i miesiącu"""
        if 'year' in self.df.columns and 'month' in self.df.columns:
            return self.df[(self.df['year'] == year) & (self.df['month'] == month)]
        return self.df
    
    def filter_by_day(self, year, month, day):
        """Filtruj dane po konkretnym dniu"""
        if 'year' in self.df.columns and 'month' in self.df.columns and 'day' in self.df.columns:
            return self.df[(self.df['year'] == year) & 
                          (self.df['month'] == month) & 
                          (self.df['day'] == day)]
        return self.df
    
    def filter_by_date_range(self, start_date, end_date):
        """Filtruj dane po zakresie dat"""
        if 'date' in self.df.columns:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            return self.df[(self.df['date'] >= start) & (self.df['date'] <= end)]
        return self.df
    
    def calculate_kpi(self, df=None):
        """Oblicz kluczowe wskaźniki wydajności (KPI)"""
        if df is None:
            df = self.df
        
        kpi = {}
        
        # Podstawowe metryki
        if 'income' in df.columns:
            kpi['Suma przychodów'] = round(df['income'].sum(), 2)
            kpi['Średni przychód'] = round(df['income'].mean(), 2)
            kpi['Max przychód'] = round(df['income'].max(), 2)
            kpi['Min przychód'] = round(df['income'].min(), 2)
        
        if 'expense' in df.columns:
            kpi['Suma kosztów'] = round(df['expense'].sum(), 2)
            kpi['Średni koszt'] = round(df['expense'].mean(), 2)
            kpi['Max koszt'] = round(df['expense'].max(), 2)
            kpi['Min koszt'] = round(df['expense'].min(), 2)
        
        if 'income' in df.columns and 'expense' in df.columns:
            total_income = df['income'].sum()
            total_expense = df['expense'].sum()
            
            kpi['Saldo'] = round(total_income - total_expense, 2)
            kpi['Zysk netto'] = round(total_income - total_expense, 2)
            
            # Marża zysku (%)
            if total_income > 0:
                kpi['Marża zysku (%)'] = round(((total_income - total_expense) / total_income) * 100, 2)
            else:
                kpi['Marża zysku (%)'] = 0
            
            # Wskaźnik rentowności (ROI)
            if total_expense > 0:
                kpi['ROI (%)'] = round(((total_income - total_expense) / total_expense) * 100, 2)
            else:
                kpi['ROI (%)'] = 0
            
            # Stosunek przychodów do kosztów
            if total_expense > 0:
                kpi['Stosunek przychód/koszt'] = round(total_income / total_expense, 2)
            else:
                kpi['Stosunek przychód/koszt'] = 0
        
        kpi['Liczba transakcji'] = len(df)
        
        # Liczba dni w okresie
        if 'date' in df.columns:
            dates = df['date'].dropna()
            if len(dates) > 0:
                date_range = (dates.max() - dates.min()).days + 1
                kpi['Liczba dni'] = date_range
                
                # Średnie dzienne
                if 'income' in df.columns:
                    kpi['Średni dzienny przychód'] = round(df['income'].sum() / max(date_range, 1), 2)
                if 'expense' in df.columns:
                    kpi['Średni dzienny koszt'] = round(df['expense'].sum() / max(date_range, 1), 2)
        
        return kpi
    
    def calculate_monthly_summary(self):
        """Oblicz podsumowanie miesięczne"""
        if 'month_name' not in self.df.columns:
            return None
        
        if 'income' in self.df.columns and 'expense' in self.df.columns:
            monthly = self.df.groupby('month_name').agg({
                'income': ['sum', 'mean', 'count'],
                'expense': ['sum', 'mean']
            }).reset_index()
            
            monthly.columns = ['Miesiąc', 'Suma przychodów', 'Średni przychód', 
                              'Liczba transakcji', 'Suma kosztów', 'Średni koszt']
            monthly['Saldo'] = monthly['Suma przychodów'] - monthly['Suma kosztów']
            monthly['Marża (%)'] = round((monthly['Saldo'] / monthly['Suma przychodów']) * 100, 2)
            
            return monthly
        return None
    
    def calculate_daily_summary(self):
        """Oblicz podsumowanie dzienne"""
        if 'day_name' not in self.df.columns:
            return None
        
        if 'income' in self.df.columns and 'expense' in self.df.columns:
            daily = self.df.groupby('day_name').agg({
                'income': ['sum', 'count'],
                'expense': 'sum'
            }).reset_index()
            
            daily.columns = ['Dzień', 'Suma przychodów', 'Liczba transakcji', 'Suma kosztów']
            daily['Saldo'] = daily['Suma przychodów'] - daily['Suma kosztów']
            
            return daily
        return None
    
    def calculate_trend(self):
        """Oblicz trend (wzrost/spadek) na podstawie danych czasowych"""
        if 'date' not in self.df.columns or 'income' not in self.df.columns:
            return None
        
        df_sorted = self.df.sort_values('date')
        
        # Podziel dane na dwie połowy
        mid_point = len(df_sorted) // 2
        first_half = df_sorted.iloc[:mid_point]
        second_half = df_sorted.iloc[mid_point:]
        
        trend = {}
        
        if len(first_half) > 0 and len(second_half) > 0:
            first_income = first_half['income'].sum()
            second_income = second_half['income'].sum()
            
            if first_income > 0:
                trend['Zmiana przychodów (%)'] = round(
                    ((second_income - first_income) / first_income) * 100, 2
                )
            
            if 'expense' in self.df.columns:
                first_expense = first_half['expense'].sum()
                second_expense = second_half['expense'].sum()
                
                if first_expense > 0:
                    trend['Zmiana kosztów (%)'] = round(
                        ((second_expense - first_expense) / first_expense) * 100, 2
                    )
        
        return trend
    
    def calculate_category_analysis(self):
        """Analiza według kategorii (jeśli istnieje kolumna category)"""
        category_cols = ['category', 'kategoria', 'Category', 'Kategoria']
        category_col = None
        
        for col in category_cols:
            if col in self.df.columns:
                category_col = col
                break
        
        if category_col is None or 'expense' not in self.df.columns:
            return None
        
        category_summary = self.df.groupby(category_col).agg({
            'expense': ['sum', 'mean', 'count']
        }).reset_index()
        
        category_summary.columns = ['Kategoria', 'Suma', 'Średnia', 'Liczba']
        category_summary['Procent (%)'] = round(
            (category_summary['Suma'] / category_summary['Suma'].sum()) * 100, 2
        )
        
        return category_summary.sort_values('Suma', ascending=False)
    
    def get_available_months(self):
        """Pobierz listę dostępnych miesięcy"""
        if 'month_name' in self.df.columns:
            return sorted(self.df['month_name'].dropna().unique().tolist())
        return []
    
    def get_available_days(self):
        """Pobierz listę dostępnych dni"""
        if 'day_name' in self.df.columns:
            return sorted(self.df['day_name'].dropna().unique().tolist())
        return []
