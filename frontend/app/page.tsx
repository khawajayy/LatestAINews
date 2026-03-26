"use client";
import { useState } from "react";
import NewsCard from "../components/NewsCard";
import { Filter } from "lucide-react";

const MOCK_DATA = [
  {
    title: "OpenAI Unveils Sora: A Revolutionary Text-to-Video Model",
    summary: "Sora can generate highly detailed scenes with complex camera motion and multiple characters.",
    category: "LLM",
    hype_score: 4,
    hype_label: "Balanced",
    source: "OpenAI Blog",
    url: "https://openai.com/sora"
  },
  {
    title: "AGI Achieved Internal Leak: The End of Human Labor?",
    summary: "Anonymous sources claim Internal Model X has reached superhuman reasoning capabilities.",
    category: "AGENTS",
    hype_score: 10,
    hype_label: "Maximum Hype",
    source: "X (@HypeNews)",
    url: "https://x.com/rowancheung"
  },
  {
    title: "Direct Preferences Optimization: A Technical Deep Dive",
    summary: "Exploring the mathematical foundations of DPO for aligning large language models.",
    category: "LLM",
    hype_score: 1,
    hype_label: "Pure Signal",
    source: "ArXiv",
    url: "https://arxiv.org/abs/2305.18290"
  }
];

export default function Home() {
  const [signalOnly, setSignalOnly] = useState(false);

  const filteredNews = signalOnly 
    ? MOCK_DATA.filter(item => item.hype_score <= 5)
    : MOCK_DATA;

  return (
    <main className="dashboard-container">
      <header className="title-section">
        <h1>AI PULSE</h1>
        <p style={{ opacity: 0.6 }}>Autonomous Real-time News Aggregator</p>
      </header>

      <section className="filter-bar" style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '1rem' }}>
        <span style={{ fontSize: '0.9rem', opacity: 0.8, display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Filter size={16} /> Filter:
        </span>
        <button 
          onClick={() => setSignalOnly(!signalOnly)}
          style={{
            background: signalOnly ? 'var(--neon-cyan)' : 'var(--glass-bg)',
            color: signalOnly ? 'black' : 'white',
            border: '1px solid var(--neon-cyan)',
            padding: '6px 16px',
            borderRadius: '20px',
            cursor: 'pointer',
            fontWeight: 'bold',
            transition: 'all 0.2s'
          }}
        >
          {signalOnly ? "Signal Only Active" : "Show All (Hype Included)"}
        </button>
      </section>

      <div className="news-grid">
        {filteredNews.map((item, index) => (
          <NewsCard key={index} item={item} />
        ))}
      </div>
      
      <footer style={{ marginTop: '5rem', textAlign: 'center', opacity: 0.4, fontSize: '0.8rem' }}>
        &copy; 2026 AI Pulse Engine. Refreshed every 45 minutes.
      </footer>
    </main>
  );
}
