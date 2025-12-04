# 🚀 BrevardBidderAI Skills System

> **Agentic AI-Powered Skills Development Ecosystem**
> 
> Automated documentation, pattern analysis, and skill generation for the BrevardBidderAI foreclosure auction platform.

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-success)](https://github.com)

**Created by:** Ariel Shapira, Solo Founder - Everest Capital USA

---

## 📋 Overview

This system creates a **self-improving development cycle** where every task generates documentation, patterns are automatically identified, and AI skills are created and optimized continuously.

```
Daily Development → Auto Documentation → Pattern Analysis → Skill Generation → Optimization
        ↑                                                                              ↓
        └──────────────────────────────────────────────────────────────────────────────┘
```

### Expected ROI
| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Tasks Documented | 30-50 | 100-150 | 300+ |
| Skills Created | 2-3 | 10-15 | 25-35 |
| Hours Saved | 5-10 | 30-50 | 100+ |
| Success Rate | 60% | 80% | 90%+ |

---

## 🏗️ Architecture

### Tech Stack
- **Database**: Supabase (PostgreSQL)
- **Automation**: GitHub Actions
- **Dashboard**: React + Tailwind CSS (Vercel)
- **Analysis**: Multi-model AI (Claude, Gemini, GPT)
- **Core Scripts**: Python 3.11+

### Integration Points
- BrevardBidderAI main platform
- GitHub repository automation
- Supabase real-time database
- Vercel serverless functions

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/breverdbidder/brevard-bidder-ai-skills.git
cd brevard-bidder-ai-skills
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Initialize Database

```bash
python scripts/init_database.py
```

### 4. Deploy Dashboard

```bash
# Push to GitHub - auto-deploys via Vercel
git push origin main
```

---

## 📁 Project Structure

```
brevard-bidder-ai-skills/
├── .github/
│   └── workflows/
│       ├── daily_analysis.yml      # Daily documentation check
│       ├── weekly_optimization.yml # Weekly skill optimization
│       └── monthly_research.yml    # Monthly research cycle
├── scripts/
│   ├── core/
│   │   ├── orchestrator.py         # Main coordinator
│   │   ├── pattern_analyzer.py     # Pattern detection
│   │   ├── skill_generator.py      # Skill creation
│   │   └── optimizer.py            # Skill optimization
│   ├── utils/
│   │   ├── supabase_client.py      # Database operations
│   │   └── metrics.py              # Performance tracking
│   └── init_database.py            # Database setup
├── dashboard/
│   ├── index.html                  # Dashboard UI
│   └── api/                        # Vercel serverless functions
├── prompts/
│   ├── analysis.md                 # Pattern analysis prompt
│   ├── skill_creation.md           # Skill generation prompt
│   └── optimization.md             # Optimization prompt
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | ✅ |
| `SUPABASE_KEY` | Supabase anon key | ✅ |
| `ANTHROPIC_API_KEY` | Claude API key | ✅ |
| `GOOGLE_API_KEY` | Gemini API key | Optional |
| `OPENAI_API_KEY` | GPT API key | Optional |
| `GITHUB_TOKEN` | GitHub access token | ✅ |

---

## 📊 Database Schema

### Core Tables

```sql
-- Task documentation
CREATE TABLE skill_tasks (
    id UUID PRIMARY KEY,
    task_id TEXT UNIQUE,
    title TEXT,
    description TEXT,
    task_type TEXT,
    category TEXT,
    complexity_score INT,
    files_affected JSONB,
    implementation JSONB,
    challenges JSONB,
    outcome JSONB,
    skill_potential INT,
    analyzed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated skills
CREATE TABLE ai_skills (
    id UUID PRIMARY KEY,
    skill_id TEXT UNIQUE,
    name TEXT,
    category TEXT,
    version TEXT,
    description TEXT,
    content TEXT,
    pattern_sources TEXT[],
    total_uses INT DEFAULT 0,
    success_rate DECIMAL,
    avg_time_saved INT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Usage metrics
CREATE TABLE skill_usage (
    id UUID PRIMARY KEY,
    skill_id TEXT REFERENCES ai_skills(skill_id),
    success BOOLEAN,
    time_saved_minutes INT,
    iterations INT,
    rating INT,
    feedback TEXT,
    used_at TIMESTAMPTZ DEFAULT NOW()
);

-- Identified patterns
CREATE TABLE skill_patterns (
    id UUID PRIMARY KEY,
    pattern_id TEXT UNIQUE,
    name TEXT,
    category TEXT,
    frequency INT,
    consistency_score DECIMAL,
    skill_viability DECIMAL,
    task_references TEXT[],
    synthesized BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🤖 Automation Workflows

### Daily Analysis (2:00 AM EST)
1. Check new documentation count
2. If threshold met (10+ new tasks), generate analysis prompt
3. Notify for manual multi-model analysis
4. Auto-synthesize if results available

### Weekly Optimization (Monday 3:00 AM EST)
1. Identify underperforming skills
2. Generate optimization prompts
3. Create upgrade recommendations

### Monthly Research (1st of month, 4:00 AM EST)
1. Generate comprehensive research prompt
2. Analyze industry best practices
3. Plan system-wide upgrades

---

## 📖 Usage Guide

### For Claude Code

Add this to your Claude Code system prompt:

```markdown
## Auto-Documentation Protocol

After completing any task, generate documentation JSON:

\`\`\`json
{
  "task_id": "UUID",
  "title": "Brief title",
  "description": "Original request",
  "task_type": "feature|bugfix|refactor",
  "category": "backend|frontend|database|api",
  "complexity_score": 1-10,
  "files_affected": ["file1.py", "file2.tsx"],
  "implementation": {
    "approach": "Solution description",
    "key_steps": [],
    "patterns_used": []
  },
  "challenges": [],
  "outcome": {
    "success": true,
    "iterations": 1
  },
  "skill_potential": 1-10
}
\`\`\`

Save to Supabase `skill_tasks` table.
```

### Status Commands

```bash
# Check system status
python scripts/core/orchestrator.py --status

# Run pattern analysis
python scripts/core/orchestrator.py --analyze

# Generate skills from patterns
python scripts/core/orchestrator.py --generate

# Optimize existing skills
python scripts/core/orchestrator.py --optimize
```

---

## 🎯 BrevardBidderAI Integration

### Key Features Tracked
- Foreclosure auction data processing
- Lien priority analysis
- ML score calculations
- BCPAO data scraping
- Max bid calculations
- Report generation
- API endpoint creation

### Common Patterns
- CRUD operations for auction data
- Scraper implementation
- Database migrations
- Pipeline stage processing
- Error handling patterns
- Testing strategies

---

## 📈 Metrics Dashboard

Access the live dashboard:
- **Development**: `http://localhost:5173`
- **Production**: `https://brevard-bidder-skills.vercel.app`

### Key Metrics
- Total skills created
- Overall success rate
- Time saved (hours)
- Documentation count
- Pattern identification rate

---

## 🔐 Security

- All API keys stored in environment variables
- Supabase Row Level Security enabled
- GitHub Actions secrets management
- No sensitive data in logs

---

## 📞 Support

**Ariel Shapira** - Solo Founder, Everest Capital USA
- GitHub: [@breverdbidder](https://github.com/breverdbidder)
- Project: BrevardBidderAI

---

**Version:** 1.0.0
**Created:** December 4, 2025
**License:** Proprietary - Everest Capital of Brevard LLC
