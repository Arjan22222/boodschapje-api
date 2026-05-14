from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/zoek')
def zoek():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'geen zoekterm'}), 400
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    resultaat = {}

    try:
        ah_url = f'https://api.ah.nl/mobile-services/product/search/v2?query={query}&size=5'
        ah_resp = requests.get(ah_url, headers=headers, timeout=10)
        resultaat['ah'] = ah_resp.json()
    except Exception as e:
        resultaat['ah'] = {'error': str(e)}

    try:
        jumbo_url = f'https://mobileapi.jumbo.com/v17/search?q={query}&limit=5'
        jumbo_resp = requests.get(jumbo_url, headers=headers, timeout=10)
        resultaat['jumbo'] = jumbo_resp.json()
    except Exception as e:
        resultaat['jumbo'] = {'error': str(e)}

    return jsonify(resultaat)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
