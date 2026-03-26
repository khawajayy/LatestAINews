"use client";
import HypeMeter from "./HypeMeter";
import { ExternalLink, Zap, AlertTriangle, ShieldCheck } from "lucide-react";

interface NewsItem {
  title: string;
  summary: string;
  category: string;
  hype_score: number;
  hype_label: string;
  source: string;
  url: string;
}

export default function NewsCard({ item }: { item: NewsItem }) {
  const getLabelColor = () => {
    if (item.hype_score <= 3) return "var(--neon-cyan)";
    if (item.hype_score >= 8) return "var(--neon-orange)";
    return "var(--neon-purple)";
  };

  const labelColor = getLabelColor();

  return (
    <div className="glass-card news-card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div className="category-blob" style={{ 
              width: '8px', height: '8px', borderRadius: '50%', background: labelColor,
              boxShadow: `0 0 10px ${labelColor}`
          }} />
          <span className="category-tag" style={{ 
              fontSize: '0.75rem', fontWeight: 'bold', letterSpacing: '0.05em', color: labelColor
          }}>
            {item.category}
          </span>
        </div>
        <span className="source-tag" style={{ fontSize: '0.7rem', opacity: 0.5 }}>{item.source}</span>
      </div>
      
      <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.75rem', lineHeight: 1.3, color: '#fff' }}>
        {item.title}
      </h3>
      
      <p style={{ fontSize: '0.9rem', color: 'rgba(255,255,255,0.7)', marginBottom: '1.5rem', lineHeight: 1.5, flexGrow: 1 }}>
        {item.summary}
      </p>
      
      <div className="card-footer" style={{ 
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', 
        paddingTop: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.05)' 
      }}>
        <HypeMeter score={item.hype_score} />
        
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '10px' }}>
          <div style={{ 
            padding: '4px 12px', borderRadius: '4px', background: `${labelColor}15`,
            border: `1px solid ${labelColor}33`, fontSize: '0.75rem', fontWeight: 'bold', color: labelColor
          }}>
            {item.hype_label.toUpperCase()}
          </div>
          <a href={item.url} target="_blank" rel="noopener noreferrer" className="read-source-btn" style={{ 
             color: 'var(--neon-cyan)', display: 'flex', alignItems: 'center', gap: '6px', 
             textDecoration: 'none', fontSize: '0.85rem', fontWeight: '500',
             padding: '4px 0', borderBottom: '1px solid transparent', transition: 'all 0.2s'
          }}>
            Read Source <ExternalLink size={14} />
          </a>
        </div>
      </div>
    </div>
  );
}
