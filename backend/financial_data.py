from os import close
import yfinance as yf
import numpy as np

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

# Perform historical analysis on stock price data
def historical_analysis(ticker):
    stock = yf.Ticker(ticker)
    try:
        history = stock.history(period="max")
    except Exception:
        history = None
        return None
    
    # Calculate Moving Averages
    history["ma50"] = history["Close"].rolling(50).mean()
    history["ma200"] = history["Close"].rolling(200).mean()
    
    # Calculate trend signal
    trend_signal = 1 if history["ma50"].iloc[-1] > history["ma200"].iloc[-1] else -1
    
    # Calculate RSI
    delta = history["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    current_rsi = rsi.iloc[-1]
    
    # Calculate volatility
    returns = history["Close"].pct_change()
    volatility = returns.std() * (252 ** 0.5)
    
    # Calculate 1 year return
    one_year_return = history["Close"].iloc[-1] / history["Close"].iloc[-252] - 1
    
    # Calculate Sharpe Ratio
    sharpe_ratio = ((returns.mean() - 0.02) / returns.std()) * (252 ** 0.5)
    
    # Maximum drawdown
    max_drawdown = (history["Close"] / history["Close"].cummax() - 1).min()
    
    indicators = {
        "rsi": current_rsi,
        "volatility": volatility,
        "sharpe": sharpe_ratio,
        "drawdown": max_drawdown,
        "trend_signal": trend_signal,
        "one_year_return": one_year_return,
    }
        
    rules = [
        ("rsi", lambda x: x > 70, "Overbought conditions", 1),
        ("rsi", lambda x: x < 30, "Oversold conditions", 1),
        ("volatility", lambda x: x > 0.5, "High volatility", 2),
        ("drawdown", lambda x: x < -0.4, "Large historical drawdown", 2),
        ("trend_signal", lambda x: x < 0, "Bearish moving average crossover", 2),
        ("one_year_return", lambda x: x < -0.2, "Negative yearly momentum", 1),
    ]
    
    hist_score = 0
    metrics = []
    
    for metric, condition, message, weight in rules:
        value = indicators.get(metric)
        if value is not None and condition(value):
            metrics.append(message)
            hist_score += weight

    if hist_score >= 6:
        level = "High Risk"
    elif hist_score >= 3:
        level = "Medium Risk"
    else:
        level = "Low Risk"

    hist_report = {
        "hist_score": hist_score,
        "hist_level": level,
        "hist_flags": metrics
    }
    
    return hist_report

# Retrieves analyst recommendations for a given stock ticker
def get_analyst_recommendations(ticker):
    stock = yf.Ticker(ticker)
    try:
        recommendations = stock.recommendations
    except Exception:
        recommendations = None
        
    recent = recommendations.tail(10)
    
    return recent


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