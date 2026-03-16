from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_analysis import generate_report
from financial_data import get_financials, historical_analysis, risk_analysis
from news_fetcher import get_all_news, sentiment_analysis
import traceback

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
        history = historical_analysis(ticker)
        risk_report = risk_analysis(financials)
        sentiments = sentiment_analysis(news)
        financials_str = '\n'.join([f"{k}: {v}" for k, v in financials.items()])
        news_str = "\n".join([f"{item.get('title','')} ({item.get('published','')}) - {item.get('link','')}" for item in news])
        history_str = "\n".join([f"{k}: {v}" for k, v in history.items()]) if history else "No historical data available"
        risk_report_str = '\n'.join([f"{k}: {v}" for k, v in risk_report.items()])
        sentiments_str = '\n'.join([f"{item['title']}: {item['sentiment']}" for item in sentiments])
        analysis = generate_report(ticker, financials_str, history_str, risk_report_str, news_str, sentiments_str)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'analysis': f'Error: {str(e)}'}), 500
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    app.run(port=5000, debug=True)