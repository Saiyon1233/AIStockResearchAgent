from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_analysis import generate_report
from financial_data import get_financials
from news_fetcher import get_all_news

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    ticker = data.get('ticker', '')
    if not ticker:
        return jsonify({'analysis': 'No ticker provided.'}), 400
    try:
        financials = get_financials(ticker)
        news = get_all_news(ticker)
        financials_str = '\n'.join([f"{k}: {v}" for k, v in financials.items()])
        news_str = '\n'.join(news)
        analysis = generate_report(ticker, financials_str, news_str)
    except Exception as e:
        return jsonify({'analysis': f'Error: {str(e)}'}), 500
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    app.run(port=5000)