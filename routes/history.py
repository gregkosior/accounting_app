from flask import Blueprint, render_template
import os

history_bp = Blueprint('history', __name__)


@history_bp.route('/history')
def history():
    entries = []
    if os.path.exists('analysis_history.txt'):
        with open('analysis_history.txt', encoding='utf-8') as f:
            block = {}
            for line in f:
                if line.strip() == '---':
                    if block:
                        entries.append(block)
                        block = {}
                elif line.startswith('Data:'):
                    block['date'] = line.replace('Data:', '').strip()
                elif line.startswith('Plik:'):
                    block['file'] = line.replace('Plik:', '').strip()
                elif ':' in line:
                    k, v = line.split(':', 1)
                    block[k.strip()] = v.strip()
            if block:
                entries.append(block)
    return render_template('history.html', entries=entries)

# Podgląd pojedynczej analizy po indeksie
@history_bp.route('/history/<int:idx>')
def history_detail(idx):
    entries = []
    if os.path.exists('analysis_history.txt'):
        with open('analysis_history.txt', encoding='utf-8') as f:
            block = {}
            for line in f:
                if line.strip() == '---':
                    if block:
                        entries.append(block)
                        block = {}
                elif line.startswith('Data:'):
                    block['date'] = line.replace('Data:', '').strip()
                elif line.startswith('Plik:'):
                    block['file'] = line.replace('Plik:', '').strip()
                elif ':' in line:
                    k, v = line.split(':', 1)
                    block[k.strip()] = v.strip()
            if block:
                entries.append(block)
    if 0 <= idx < len(entries):
        entry = entries[idx]
        return render_template('history_detail.html', entry=entry, idx=idx)
    return 'Nie znaleziono analizy', 404
