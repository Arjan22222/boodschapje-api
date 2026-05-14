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
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        ah_url = f'https://api.ah.nl/mobile-services/product/search/v2?query={query}&size=5'
        ah_resp = requests.get(ah_url, headers=headers, timeout=5)
        ah_data = ah_resp.json()

        jumbo_url = f'https://mobileapi.jumbo.com/v17/search?q={query}&limit=5'
        jumbo_resp = requests.get(jumbo_url, headers=headers, timeout=5)
        jumbo_data = jumbo_resp.json()

        return jsonify({'ah': ah_data, 'jumbo': jumbo_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
