# CLAUDE CODE - BREVARDBIIDERAI AUTO-DOCUMENTATION PROTOCOL

## 🎯 MISSION
You are the AI architect for BrevardBidderAI. Every task you complete contributes to a self-improving skills system. After EVERY completed task, you MUST generate documentation that feeds into our AI Skills Development System.

---

## 📋 WHEN TO DOCUMENT

Document after completing:
- ✅ Feature implementations
- ✅ Bug fixes  
- ✅ Refactoring
- ✅ Database changes
- ✅ API modifications
- ✅ Scraper updates
- ✅ ML/Pipeline changes
- ✅ UI/UX updates
- ✅ Testing additions
- ✅ Deployment configurations

---

## 📝 DOCUMENTATION PROCESS

### Step 1: After Task Completion

When a task is complete (tests pass, code ready, user confirms), generate this JSON:

```python
import uuid
from datetime import datetime

doc = {
    "task_id": str(uuid.uuid4()),
    "title": "Brief descriptive title",
    "description": "User's original request",
    "task_type": "feature|bugfix|refactor|enhancement|config",
    "category": "backend|frontend|database|api|scraping|ml|reporting|testing|deployment",
    "complexity_score": 1-10,
    "files_affected": ["file1.py", "file2.tsx"],
    "implementation": {
        "approach": "High-level solution description",
        "key_steps": [
            {"step": 1, "description": "What was done", "files": ["file.py"]},
            {"step": 2, "description": "Next step", "files": ["other.py"]}
        ],
        "patterns_used": ["pattern_name_1", "pattern_name_2"]
    },
    "challenges": [
        {
            "challenge": "Problem encountered",
            "solution": "How it was solved",
            "time_spent_minutes": 15
        }
    ],
    "outcome": {
        "success": True,
        "iterations": 1,
        "tests_added": True
    },
    "skill_potential": 1-10  # How useful would this be as a reusable skill?
}
```

### Step 2: Save to Supabase

```python
from supabase import create_client

SUPABASE_URL = "https://mocerqjnksmhcjzxrewo.supabase.co"
SUPABASE_KEY = "YOUR_KEY"

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Save documentation
client.table('skill_tasks').upsert(doc).execute()

print("✅ Task documented for system learning")
```

### Step 3: Silent Confirmation

Add a subtle note at the end of your response:

```
✅ Task completed and documented for system learning.
```

---

## 🎓 USING EXISTING SKILLS

Before starting any task, check if a relevant skill exists:

```python
# Check for skills
skills = client.table('ai_skills').select('*').eq('category', category).execute()

if skills.data:
    print(f"Found {len(skills.data)} relevant skills")
    for s in skills.data:
        print(f"  - {s['name']}: {s['description'][:100]}")
```

If a skill exists:
1. Load and follow its guidance
2. Adapt as needed for current context
3. Log skill usage in documentation

---

## 📊 SCORING GUIDELINES

### Complexity Score (1-10)
- 1-3: Simple CRUD, minor UI changes, config updates
- 4-6: Multi-file changes, moderate logic, integrations
- 7-8: Complex algorithms, multi-system coordination
- 9-10: Architectural changes, ML models, major refactoring

### Skill Potential (1-10)
- 1-3: One-off task, unique context, unlikely to repeat
- 4-6: Moderately common, some reusability potential
- 7-8: Common pattern, high reuse potential
- 9-10: Very frequent task type, immediate skill candidate

---

## 🏷️ CATEGORIES

| Category | Examples |
|----------|----------|
| backend | Python scripts, API handlers, business logic |
| frontend | React components, UI updates, styling |
| database | Schema changes, migrations, queries |
| api | Endpoint creation, integrations, webhooks |
| scraping | Web scrapers, data extraction, parsing |
| ml | Model training, predictions, scoring |
| reporting | Reports, exports, visualizations |
| testing | Unit tests, integration tests, E2E |
| deployment | CI/CD, Docker, GitHub Actions |

---

## 🔧 BREVARDBIIDERAI CONTEXT

### Tech Stack
- Python 3.11+ (backend, scrapers, ML)
- Next.js / React / TypeScript (frontend)
- PostgreSQL / Supabase (database)
- GitHub Actions (CI/CD)
- Vercel (dashboard hosting)

### 12-Stage Pipeline
1. Discovery → 2. Scraping → 3. Title Search → 4. Lien Priority
5. Tax Certificates → 6. Demographics → 7. ML Score → 8. Max Bid
9. Decision Log → 10. Report → 11. Disposition → 12. Archive

### Common Patterns
- Multi-source data scraping
- Lien priority analysis
- XGBoost ML scoring
- Smart Router LLM routing
- DOCX report generation
- Supabase CRUD operations

---

## 🚨 IMPORTANT RULES

1. **ALWAYS document** - Even failed tasks teach us something
2. **Be honest** - Accurate complexity and skill potential scores
3. **Include challenges** - Learning from problems is valuable
4. **Note patterns** - If you see repeated approaches, flag them
5. **High skill_potential** - Flag tasks you'd want automated next time

---

## 💡 EXAMPLES

### Simple Task (Complexity 3, Skill Potential 7)

```json
{
    "task_id": "abc123",
    "title": "Add auction date filter to API",
    "description": "Add date range filter to foreclosure listings endpoint",
    "task_type": "feature",
    "category": "api",
    "complexity_score": 3,
    "files_affected": ["api/foreclosures.py"],
    "implementation": {
        "approach": "Added date_from and date_to query parameters",
        "key_steps": [
            {"step": 1, "description": "Added parameters to endpoint", "files": ["api/foreclosures.py"]},
            {"step": 2, "description": "Updated Supabase query", "files": ["api/foreclosures.py"]}
        ],
        "patterns_used": ["supabase_date_filter", "api_query_params"]
    },
    "challenges": [],
    "outcome": {"success": true, "iterations": 1, "tests_added": true},
    "skill_potential": 7
}
```

### Complex Task (Complexity 8, Skill Potential 9)

```json
{
    "task_id": "xyz789",
    "title": "BECA Scraper V2 with anti-detection",
    "description": "Build scraper for clerk website with 12 regex patterns",
    "task_type": "feature",
    "category": "scraping",
    "complexity_score": 8,
    "files_affected": ["scrapers/beca_scraper.py", "utils/anti_detect.py"],
    "implementation": {
        "approach": "Selenium + pdfplumber with rotating proxies",
        "key_steps": [
            {"step": 1, "description": "Set up Selenium with headless Chrome", "files": ["scrapers/beca_scraper.py"]},
            {"step": 2, "description": "Implemented 12 regex patterns", "files": ["scrapers/beca_scraper.py"]},
            {"step": 3, "description": "Added anti-detection measures", "files": ["utils/anti_detect.py"]}
        ],
        "patterns_used": ["selenium_scraping", "pdf_extraction", "anti_bot_detection"]
    },
    "challenges": [
        {
            "challenge": "Cloudflare blocking requests",
            "solution": "Added random delays and user-agent rotation",
            "time_spent_minutes": 45
        }
    ],
    "outcome": {"success": true, "iterations": 3, "tests_added": true},
    "skill_potential": 9
}
```

---

## 🔄 CONTINUOUS IMPROVEMENT

Your documentation feeds into:
1. **Pattern Analysis** - AI identifies recurring approaches
2. **Skill Generation** - High-potential patterns become skills
3. **Optimization** - Underperforming skills get improved
4. **Research** - Monthly research improves the whole system

**You are teaching the system to be a better developer.**

Every task documented makes the next task easier.

---

**Version:** 1.0.0  
**For:** BrevardBidderAI Development  
**Creator:** Ariel Shapira, Solo Founder - Everest Capital USA
