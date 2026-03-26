# AI Pulse: Autonomous AI News Aggregator

AI Pulse is a real-time, autonomous AI news aggregator that scrapes, processes, and displays the latest breakthroughs in Artificial Intelligence. It features "The Elegant Void" aesthetic—a premium, minimalist dashboard designed for high-signal technical content.

## 🚀 Key Features
- **Multi-Source Scraping**: Automates news gathering from Hacker News, ArXiv (CS.AI), and top AI lab blogs (OpenAI, Anthropic).
- **AI-Powered Insights**: Uses **Gemini 2.0 Flash-Lite** to categorize articles, generate 150-character "Quick Takes", and calculate a **Hype Meter** score.
- **Hype Meter**: Distinguishes between grounded technical signal (1-3) and marketing fluff (8-10).
- **Autonomous Pipeline**: A GitHub Action runs the entire scraping and processing flow every 45 minutes.
- **The Elegant Void UI**: A Next.js 15+ dashboard with glassmorphism, Framer Motion animations, and a focus on visual excellence.

## 🛠️ Tech Stack
- **Frontend**: Next.js 15, React 19, Framer Motion, Lucide React.
- **Backend/Database**: Supabase (Postgres with Vector support enabled).
- **AI Engine**: Google Gemini 2.0 Flash-Lite.
- **Automation**: GitHub Actions (Ubuntu Runner).
- **Scraping**: Python 3.12, Playwright, Beautiful Soup 4.

## 📂 Project Structure
- `/frontend`: Next.js web application.
- `/brain`: Core AI processing logic (`processor.py`).
- `/scrapers`: Specialized scraping modules for different sources.
- `/supabase`: Database schema and migration files.
- `.github/workflows`: Automation pipeline configuration.

## ⚙️ Setup & Deployment

### Environment Variables
Create a `.env` file in the root and a `.env.local` in `/frontend`:
- `SUPABASE_URL`: Your Supabase Project URL.
- `SUPABASE_KEY`: Your Supabase Service Role Key (for the pipeline) or Anon Key (for the frontend).
- `GEMINI_API_KEY`: Your Google AI Studio API Key.

### Database Setup
Run the SQL found in `supabase/schema.sql` in your Supabase SQL Editor to initialize the `articles` table.

### Deployment
1. **GitHub Actions**: Add the environment variables as Repository Secrets in GitHub.
2. **Vercel**: Deploy the `/frontend` directory to Vercel, ensuring the framework is set to Next.js.

---
Built with ⚡ by Antigravity
