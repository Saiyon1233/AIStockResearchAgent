import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_report(ticker, financials, news):

    prompt = f"""
                You are an investment analyst.

                Company: {ticker}

                Financial Data:
                {financials}

                Recent News:
                {news}

                Write a concise investment research brief using bullet points.

                Sections:
                - Financial Signals
                - Recent Developments
                - Key Risks
                - Investment Thesis
            """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text