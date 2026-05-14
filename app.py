from flask import Flask, jsonify, request
from flask_cors import CORS
from supermarktconnector.ah import AHConnector
from supermarktconnector.jumbo import JumboConnector
import os

app = Flask(__name__)
CORS(app)
ah = AHConnector()
jumbo = JumboConnector()

@app.route('/zoek')
def zoek():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'geen zoekterm'}), 400
    try:
        ah_data = ah.search_products(query=query, size=3)
        jumbo_data = jumbo.search_products(query=query, size=3, page=0)
        return jsonify({'ah': ah_data, 'jumbo': jumbo_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
