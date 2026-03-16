import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_report(ticker, financials, history, risk_report, news, sentiments):

    prompt = f"""
                You are a professional equity research analyst writing a concise institutional-style briefing.

                Company: {ticker}

                Financial Data:
                {financials}

                Historical Analysis:
                {history}

                Risk Analysis:
                {risk_report}

                Recent News:
                {news}

                Sentiment Analysis:
                {sentiments}

                Your task is to synthesize the information above into a concise investment research brief.

                Step 1: Identify the 6-8 most important signals from the data above. Focus only on signals that materially affect growth, valuation, competitive position, or risk.

                Step 2: Using those signals, write a concise investment research brief that is concise and analytical, and is 100% signal and no narratives.

                Sections:

                Financial Signals
                - Identify the 4-5 most important financial indicators.
                - Prioritize metrics related to growth, profitability, valuation, and cash flow.
                - When referencing a metric, briefly interpret its implication (e.g., growth acceleration, margin strength, valuation compression).
                - Prefer meaningful metrics such as revenue growth, ROE, ROA, margins, free cash flow, and forward valuation.
                - Avoid generic statements like "indicates strong performance."

                Recent Developments
                - Identify the 3-4 most important business or strategic developments.
                - Focus on developments that affect competitive positioning, revenue growth, or major strategic shifts.
                - Use news and sentiment only if they materially impact the company's outlook.
                - Avoid repeating financial metrics already discussed above.

                Key Risks
                - Identify the 3-4 most material downside risks.
                - Risks must be supported by either financial data, risk analysis, or credible news developments.
                - Do not invent macro risks unrelated to the company's business model.
                - Avoid generic risks like "market volatility" unless directly supported by data.

                Investment Thesis
                - Provide a short synthesis explaining the investment case.
                - Combine financial strength, strategic developments, and key risks into a clear narrative.
                - Focus on what drives long-term performance or valuation.
                - Avoid marketing language or hype.

                Rules:
                - Avoid generic financial commentary.
                - Do not mention 52-week highs or trivial price movements.
                - Do not repeat the same metric across multiple sections.
                - Each bullet point must reference a concrete metric, event, or strategic development.
                - Prefer insight and interpretation over description.
            """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text