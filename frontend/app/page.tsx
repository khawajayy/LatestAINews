import { useState, useEffect } from "react";
import NewsCard from "../components/NewsCard";
import { Filter } from "lucide-react";
import { supabase } from "../utils/supabaseClient";

export default function Home() {
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [signalOnly, setSignalOnly] = useState(false);

  useEffect(() => {
    async function fetchNews() {
      setLoading(true);
      const { data, error } = await supabase
        .from('articles')
        .select('*')
        .order('created_at', { ascending: false });
      
      if (error) {
        console.error('Error fetching news:', error);
      } else {
        setNews(data || []);
      }
      setLoading(false);
    }

    fetchNews();
  }, []);

  const filteredNews = signalOnly 
    ? news.filter(item => item.hype_score <= 5)
    : news;

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
        {loading ? (
          <div style={{ textAlign: 'center', gridColumn: '1 / -1', padding: '4rem', opacity: 0.5 }}>
            <p className="animate-pulse">Loading AI Pulse signal...</p>
          </div>
        ) : filteredNews.length > 0 ? (
          filteredNews.map((item, index) => (
            <NewsCard key={index} item={item} />
          ))
        ) : (
          <div style={{ textAlign: 'center', gridColumn: '1 / -1', padding: '4rem', opacity: 0.5 }}>
            <p>No news found. Check back later.</p>
          </div>
        )}
      </div>
      
      <footer style={{ marginTop: '5rem', textAlign: 'center', opacity: 0.4, fontSize: '0.8rem' }}>
        &copy; 2026 AI Pulse Engine. Refreshed every 45 minutes.
      </footer>
    </main>
  );
}
