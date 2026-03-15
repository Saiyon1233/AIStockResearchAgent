import yfinance as yf

# Retrieve financial data for a given stock ticker
def get_financials(ticker):

    stock = yf.Ticker(ticker)

    try:
        info = stock.info
    except Exception:
        info = {}

    data = {
        "company": info.get("longName"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "pe_ratio_forward": info.get("forwardPE"),
        "pb_ratio": info.get("priceToBook"),
        "revenue_growth": info.get("revenueGrowth"),
        "gross_margin": info.get("grossMargin"),
        "operating_margin": info.get("operatingMargin"),
        "net_margin": info.get("netMargin"),
        "current_price": info.get("currentPrice"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "current_ratio": info.get("currentRatio"),
        "quick_ratio": info.get("quickRatio"),
        "debt_ratio": info.get("debtRatio"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_equity": info.get("returnOnEquity"),
        "return_on_assets": info.get("returnOnAssets"),
        "dividend_yield": info.get("dividendYield"),
        "dividend_rate": info.get("dividendRate"),
        "dividend_payout_ratio": info.get("dividendPayoutRatio"),
        "interest_coverage": info.get("interestCoverage"),
        "free_cash_flow": info.get("freeCashflow"),
        "beta": info.get("beta")
    }

    return data

# Retrieves historical stock price data for a given ticker
def get_historical_data(ticker):
    stock = yf.Ticker(ticker)
    try:
        history = stock.history(period="max")
    except Exception:
        history = None
    return history

# Performs a risk analysis based on financial metrics
def risk_analysis(financials):
    rules = [
        ("current_ratio", lambda x: x < 1, "Low liquidity", 2),
        ("quick_ratio", lambda x: x < 1, "Weak quick ratio", 1),
        ("debt_to_equity", lambda x: x > 2, "High leverage", 2),
        ("interest_coverage", lambda x: x < 1.5, "Low interest coverage", 2),
        ("net_margin", lambda x: x < 0, "Negative profitability", 3),
        ("return_on_equity", lambda x: x < 0.05, "Low return on equity", 1),
        ("free_cash_flow", lambda x: x < 0, "Negative free cash flow", 2),
        ("beta", lambda x: x > 1.5, "High volatility", 1),
    ]
    
    risk_score = 0
    risks = []
    
    for metric, condition, message, weight in rules:
        value = financials.get(metric)
        if value is not None and condition(value):
            risks.append(message)
            risk_score += weight

    if risk_score >= 6:
        level = "High Risk"
    elif risk_score >= 3:
        level = "Medium Risk"
    else:
        level = "Low Risk"

    risk_report = {
        "risk_score": risk_score,
        "risk_level": level,
        "risk_flags": risks
    }

    return risk_report