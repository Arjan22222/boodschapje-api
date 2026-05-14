from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

@app.route('/zoek')
def zoek():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'geen zoekterm'}), 400

    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
    
    try:
        url = f'https://spaartje.com/zoeken?q={query}'
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        producten = []
        for item in soup.select('.product-card')[:5]:
            naam = item.select_one('.product-name')
            prijs = item.select_one('.price')
            winkel = item.select_one('.store-name')
            if naam and prijs:
                producten.append({
                    'naam': naam.text.strip(),
                    'prijs': prijs.text.strip(),
                    'winkel': winkel.text.strip() if winkel else 'onbekend'
                })
        return jsonify({'producten': producten})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
