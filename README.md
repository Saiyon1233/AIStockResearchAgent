# AI Stock Research Agent

## Overview
This project is an AI stock research agent, powered by Gemini, that automates the process of gathering, analyzing, and presenting financial data and news related to a stock. It leverages machine learning and natural language processing to provide insights for investors.

## Features
- Fetches real-time financial data and news
- Performs AI-driven analysis (sentiment, trends, predictions)

## Project Structure
- `server.py`: Endpoint to analyze stock data
- `financial_data.py`: Handles financial data fetching and processing
- `news_fetcher.py`: Fetches and processes news articles
- `ai_analysis.py`: Performs AI-based analysis
- `requirements.txt`: Python dependencies
- `App.js`: Receives ticker and shows analysis
- `.env`: API keys

## Setup
1. Clone the repository to your local machine: git clone <repo-url>
2. Navigate to the project directory: aiStockResearchAgent
3. Install dependencies: pip install -r requirements.txt
4. Configure your API keys and settings in the relevant files
5. Run the server with cd backend and python main.py
6. Run the webpage with cd frontend and npm start

## Skills, Technologies and Tools Used
- Python
- Gemini AI
- Yahoo Finance
- News API
- dotenv
