"use client";
import { motion } from "framer-motion";

export default function HypeMeter({ score }: { score: number }) {
  // Score 1-10. Map to -90 to 90 degrees for the needle.
  const angle = ((score - 1) / 9) * 180 - 90;
  
  const getHypeColor = (s: number) => {
    if (s <= 3) return "var(--neon-cyan)";
    if (s <= 7) return "var(--neon-purple)";
    return "var(--neon-orange)";
  };

  const color = getHypeColor(score);

  return (
    <div className="hype-meter-wrapper" style={{ 
      display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
      position: 'relative'
    }}>
      {/* Score Badge - Moved outside the arc to avoid conflict */}
      <div style={{
        padding: '2px 10px',
        borderRadius: '12px',
        background: 'rgba(255,255,255,0.05)',
        border: `1px solid ${color}44`,
        fontSize: '0.75rem',
        fontWeight: 'bold',
        color: color,
        textShadow: `0 0 8px ${color}66`
      }}>
        {score}/10
      </div>

      <div style={{ position: 'relative', width: '100px', height: '50px' }}>
        <svg width="100" height="55" viewBox="0 0 100 55" style={{ overflow: 'visible' }}>
          {/* Background Arc */}
          <path 
            d="M 10 50 A 40 40 0 0 1 90 50" 
            fill="none" 
            stroke="rgba(255,255,255,0.05)" 
            strokeWidth="6" 
            strokeLinecap="round" 
          />
          
          {/* Subtle Progress Trace */}
          <motion.path 
            d="M 10 50 A 40 40 0 0 1 90 50" 
            fill="none" 
            stroke={color} 
            strokeWidth="2" 
            strokeLinecap="round"
            strokeDasharray="125.6" 
            initial={{ strokeDashoffset: 125.6 }}
            animate={{ strokeDashoffset: 125.6 - ((score-1)/9) * 125.6 }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            style={{ opacity: 0.2 }}
          />

          {/* Pivot Base */}
          <circle cx="50" cy="50" r="4" fill="#121212" stroke={color} strokeWidth="1" />

          {/* Needle - Adjusted length and width for better visual impact */}
          <motion.line
            x1="50" y1="50" x2="50" y2="18"
            stroke={color}
            strokeWidth="2.5"
            strokeLinecap="round"
            initial={{ rotate: -90 }}
            animate={{ rotate: angle }}
            style={{ originX: "50px", originY: "50px" }}
            transition={{ type: "spring", stiffness: 50, damping: 12 }}
          />
        </svg>
      </div>

      <span style={{ 
        fontSize: '0.6rem', letterSpacing: '0.15em', opacity: 0.4, 
        textTransform: 'uppercase', fontWeight: '600', marginTop: '4px'
      }}>
        Signal Level
      </span>
    </div>
  );
}
