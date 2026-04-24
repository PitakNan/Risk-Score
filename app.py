from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from functools import wraps

app = Flask(__name__, static_folder='.')
CORS(app)
app.config['JSON_AS_ASCII'] = False
# Allow large payloads for Excel import
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

DB_PATH = 'dashboard.db'
ADMIN_CODE = "053890238-40"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != "Bearer dummy-token-for-now":
            return jsonify({"success": False, "message": "Token is missing or invalid"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return send_from_directory('.', 'Risk_Score_Dashboard.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Get Hospitals Metadata
        c.execute('SELECT * FROM hospitals')
        hospitals = {r['id']: {"name": r['name'], "prov": r['prov'], "type": r['type']} for r in c.fetchall()}
        
        # Get Records
        c.execute('SELECT * FROM records ORDER BY sort_key ASC')
        raw_records = c.fetchall()
        
        records = []
        for r in raw_records:
            h_info = hospitals.get(r['h_id'], {"name": "Unknown", "prov": "Unknown", "type": "Unknown"})
            records.append({
                "id": r['h_id'],
                "name": h_info['name'],
                "prov": h_info['prov'],
                "type": h_info['type'],
                "fy": r['fy'],
                "year": r['year'],
                "month": r['month'],
                "period": r['period'],
                "sort_key": r['sort_key'],
                "risk": r['risk'],
                "LiI": r['LiI'],
                "StI": r['StI'],
                "SuI": r['SuI'],
                "CR": r['CR'],
                "QR": r['QR'],
                "Cash": r['Cash'],
                "NWC": r['NWC'],
                "NI": r['NI'],
                "EBITDA": r['EBITDA'],
                "bumrung": r['bumrung']
            })
            
        # Get Unique lists for filters
        fys = sorted(list(set(r['fy'] for r in records)))
        provinces = sorted(list(set(r['prov'] for r in records)))
        
        # Generate period list for dropdown
        periods_map = {}
        for r in records:
            periods_map[r['sort_key']] = {"label": r['period'], "sort_key": r['sort_key'], "fy": r['fy']}
        periods = sorted(periods_map.values(), key=lambda x: x['sort_key'])

        conn.close()
        return jsonify({
            "records": records,
            "fiscal_years": fys,
            "provinces": provinces,
            "periods": periods
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('code') == ADMIN_CODE:
        return jsonify({"success": True, "token": "dummy-token-for-now"})
    return jsonify({"success": False, "message": "รหัสเข้าใช้งานไม่ถูกต้อง"}), 401

@app.route('/api/import', methods=['POST'])
@token_required
def import_data():
    data = request.json
    new_recs = data.get('records', [])
    if not new_recs:
        return jsonify({"success": False, "message": "No records found"}), 400
    
    try:
        conn = get_db()
        c = conn.cursor()
        
        # We handle overlap by deleting existing records for the periods (sort_keys) being imported
        keys_to_import = list(set(r['sort_key'] for r in new_recs))
        for k in keys_to_import:
            c.execute('DELETE FROM records WHERE sort_key = ?', (k,))
        
        # Insert new records
        for r in new_recs:
            c.execute('''INSERT INTO records 
                (h_id, fy, year, month, period, sort_key, risk, LiI, StI, SuI, CR, QR, Cash, NWC, NI, EBITDA, bumrung)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (r['id'], r['fy'], r['year'], r['month'], r['period'], r['sort_key'],
                 r['risk'], r['LiI'], r['StI'], r['SuI'],
                 r['CR'], r['QR'], r['Cash'], r['NWC'], r['NI'], r['EBITDA'], r['bumrung']))
        
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"นำเข้าข้อมูลสำเร็จ {len(new_recs)} รายการ"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
