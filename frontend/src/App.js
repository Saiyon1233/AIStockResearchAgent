import './App.css';
import React, { useState } from 'react';

function parseAnalysis(text) {
  // Remove markdown formatting and split into sections
  const sections = {};
  let currentSection = '';
  let lines = text.replace(/\*\*/g, '').replace(/\*/g, '').split(/\n|\r|\r\n/);
  lines.forEach(line => {
    if (/Financial Signals/i.test(line)) currentSection = 'Financial Signals';
    else if (/Recent Developments/i.test(line)) currentSection = 'Recent Developments';
    else if (/Key Risks/i.test(line)) currentSection = 'Key Risks';
    else if (/Investment Thesis/i.test(line)) currentSection = 'Investment Thesis';
    else if (/Investment Research Brief/i.test(line)) currentSection = 'Title';
    if (currentSection) {
      if (!sections[currentSection]) sections[currentSection] = [];
      if (!/Financial Signals|Recent Developments|Key Risks|Investment Thesis|Investment Research Brief/i.test(line)) {
        sections[currentSection].push(line.trim());
      }
    }
  });
  return sections;
}

function App() {
  const [ticker, setTicker] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setAnalysis('');
    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker }),
      });
      if (!response.ok) {
        throw new Error('Failed to fetch analysis');
      }
      const data = await response.json();
      setAnalysis(data.analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const sections = analysis ? parseAnalysis(analysis) : {};

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Stock Research Agent</h1>
        <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter stock ticker (e.g. AAPL)"
            style={{ padding: '0.5rem', fontSize: '1rem', marginRight: '1rem' }}
            required
          />
          <button type="submit" style={{ padding: '0.5rem 1rem', fontSize: '1rem' }}>
            {loading ? 'Analyzing...' : 'Get AI Analysis'}
          </button>
        </form>
        {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
        {analysis && (
          <div style={{ background: '#222', padding: '1.5rem', borderRadius: '12px', maxWidth: '700px', margin: '0 auto', color: '#fff', boxShadow: '0 4px 16px #0002' }}>
            <h2 style={{ marginBottom: '1rem' }}>Analysis for {ticker.toUpperCase()}</h2>
            {sections['Title'] && <h3 style={{ color: '#00d8ff', marginBottom: '1rem' }}>{sections['Title'][0]}</h3>}
            {['Financial Signals', 'Recent Developments', 'Key Risks', 'Investment Thesis'].map(section => (
              sections[section] && (
                <div key={section} style={{ marginBottom: '1.5rem' }}>
                  <h4 style={{ color: '#ffd700', marginBottom: '0.5rem' }}>{section}</h4>
                  <ul style={{ textAlign: 'left', paddingLeft: '1.5rem' }}>
                    {sections[section].map((item, idx) => item && <li key={idx} style={{ marginBottom: '0.5rem' }}>{item}</li>)}
                  </ul>
                </div>
              )
            ))}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
