import yfinance as yf

def get_financials(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    data = {
        "company": info.get("longName"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "pe_ratio_forward": info.get("forwardPE"),
        "pb_ratio": info.get("priceToBook"),
        "revenue_growth": info.get("revenueGrowth"),
        "gross_margins": info.get("grossMargins"),
        "operating_margins": info.get("operatingMargins"),
        "net_margins": info.get("netMargins"),
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
        "cashflow": info.get("cashflow"),
    }

    return data