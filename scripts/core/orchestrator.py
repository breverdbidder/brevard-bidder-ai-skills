#!/usr/bin/env python3
"""
BrevardBidderAI Skills System - Main Orchestrator
Coordinates all system components for automated skill development

Created by: Ariel Shapira, Solo Founder - Everest Capital USA
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.supabase_client import get_client, TaskDoc, AISkill

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class SkillsOrchestrator:
    """Main orchestrator for the AI Skills Development System"""
    
    def __init__(self):
        self.db = get_client()
        self.analysis_threshold = int(os.getenv('ANALYSIS_THRESHOLD', '10'))
        self.min_skill_viability = float(os.getenv('MIN_SKILL_VIABILITY', '7.0'))
        logger.info("🚀 BrevardBidderAI Skills Orchestrator Initialized")
    
    def status(self) -> Dict:
        """Get comprehensive system status"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 BREVARDBIIDERAI SKILLS SYSTEM STATUS")
        logger.info("=" * 60)
        
        overview = self.db.get_system_overview()
        
        logger.info(f"📄 Total Tasks Documented: {overview['total_tasks']}")
        logger.info(f"🎯 Total Skills Created: {overview['total_skills']}")
        logger.info(f"🔍 Total Patterns Identified: {overview['total_patterns']}")
        logger.info(f"📈 Total Skill Uses: {overview['total_uses']}")
        logger.info(f"⏱️  Total Time Saved: {overview['total_time_saved_hours']} hours")
        logger.info(f"✅ Average Success Rate: {overview['avg_success_rate']*100:.1f}%")
        logger.info("")
        logger.info(f"📋 Pending Analysis: {overview['pending_analysis']} tasks")
        logger.info(f"🎚️  Analysis Threshold: {self.analysis_threshold} tasks")
        
        ready = overview['pending_analysis'] >= self.analysis_threshold
        logger.info(f"🚦 Ready for Analysis: {'YES ✅' if ready else 'NO ⏳'}")
        
        # Category breakdown
        categories = self.db.get_tasks_by_category()
        if categories:
            logger.info("\n📂 Tasks by Category:")
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                logger.info(f"   {cat}: {count}")
        
        # Skills breakdown
        skills_by_cat = self.db.get_skills_by_category()
        if skills_by_cat:
            logger.info("\n🎯 Skills by Category:")
            for cat, skills in skills_by_cat.items():
                logger.info(f"   {cat}: {len(skills)} skills")
        
        logger.info("=" * 60 + "\n")
        
        return overview
    
    def check_analysis_ready(self) -> bool:
        """Check if system is ready for pattern analysis"""
        pending = self.db.count_unanalyzed_tasks()
        ready = pending >= self.analysis_threshold
        
        if ready:
            logger.info(f"✅ Analysis ready: {pending} tasks pending (threshold: {self.analysis_threshold})")
        else:
            logger.info(f"⏳ Not ready: {pending}/{self.analysis_threshold} tasks")
        
        return ready
    
    def generate_analysis_prompt(self) -> str:
        """Generate prompt for multi-model pattern analysis"""
        tasks = self.db.get_unanalyzed_tasks(limit=50)
        
        if not tasks:
            logger.warning("No tasks available for analysis")
            return ""
        
        # Format tasks for analysis
        tasks_summary = []
        for t in tasks:
            tasks_summary.append({
                'task_id': t['task_id'],
                'title': t['title'],
                'type': t['task_type'],
                'category': t['category'],
                'complexity': t['complexity_score'],
                'skill_potential': t['skill_potential'],
                'files': t.get('files_affected', []),
                'approach': t.get('implementation', {}).get('approach', ''),
                'patterns_used': t.get('implementation', {}).get('patterns_used', [])
            })
        
        prompt = f"""# BREVARDBIIDERAI PATTERN ANALYSIS REQUEST

## CONTEXT
You are analyzing task documentation from the BrevardBidderAI foreclosure auction platform development.
Your goal is to identify recurring patterns suitable for creating reusable AI skills.

## BREVARDBIIDERAI CONTEXT
- **Platform**: Foreclosure auction intelligence system
- **Tech Stack**: Python, Next.js, TypeScript, PostgreSQL, Supabase
- **Key Features**: 
  - 12-stage pipeline (Discovery → Archive)
  - ML scoring (XGBoost)
  - Multi-source data scraping
  - Smart Router LLM routing
  - Automated report generation

## INPUT DATA
Analyzing {len(tasks)} task documentation records:

```json
{json.dumps(tasks_summary, indent=2)}
```

## YOUR TASK

### 1. Pattern Identification
Identify recurring patterns across tasks. For each pattern found:
- **Pattern Name**: Descriptive name
- **Category**: backend|frontend|database|api|scraping|ml|reporting
- **Frequency**: How many tasks use this pattern
- **Consistency Score**: 1-10 (how consistently implemented)
- **Skill Viability**: 1-10 (how suitable for skill creation)
- **Task References**: Which task_ids use this pattern

### 2. Skill Recommendations
For patterns with viability >= 7, recommend skills to create:
- **Skill Name**: Clear, action-oriented name
- **Description**: What the skill does
- **Key Steps**: Major steps in the skill
- **Inputs Required**: What info Claude needs
- **Expected Output**: What the skill produces
- **Reusability**: How often this would be used

### 3. System Insights
- What development patterns dominate?
- What areas need more documentation?
- What skills would provide highest ROI?

## OUTPUT FORMAT
Respond with JSON:

```json
{{
  "analysis_timestamp": "ISO-8601",
  "tasks_analyzed": {len(tasks)},
  "patterns_identified": [
    {{
      "pattern_id": "pattern_xxx",
      "name": "Pattern Name",
      "category": "category",
      "frequency": 5,
      "consistency_score": 8,
      "skill_viability": 9,
      "task_references": ["task_id_1", "task_id_2"],
      "description": "What this pattern does"
    }}
  ],
  "recommended_skills": [
    {{
      "skill_name": "Skill Name",
      "category": "category",
      "description": "What it does",
      "viability_score": 9,
      "estimated_time_saved_minutes": 30,
      "pattern_sources": ["pattern_xxx"],
      "key_steps": ["step1", "step2"],
      "inputs": ["input1", "input2"],
      "outputs": ["output1"]
    }}
  ],
  "insights": {{
    "dominant_patterns": ["pattern1", "pattern2"],
    "documentation_gaps": ["area1", "area2"],
    "high_roi_opportunities": ["skill1", "skill2"]
  }}
}}
```

Provide thorough analysis. This drives our skill development priority.
"""
        
        # Save prompt to file
        output_dir = Path(__file__).parent.parent.parent / 'prompts' / 'generated'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"analysis_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = output_dir / filename
        output_path.write_text(prompt)
        
        logger.info(f"📝 Analysis prompt saved: {output_path}")
        logger.info("")
        logger.info("⏸️  MANUAL ACTION REQUIRED:")
        logger.info("   1. Submit prompt to Claude, Gemini, and GPT")
        logger.info("   2. Save results to prompts/responses/")
        logger.info("   3. Run: python orchestrator.py --synthesize")
        
        return prompt
    
    def synthesize_analyses(self, responses_dir: Optional[str] = None) -> Dict:
        """Synthesize pattern analyses from multiple AI models"""
        if responses_dir is None:
            responses_dir = Path(__file__).parent.parent.parent / 'prompts' / 'responses'
        else:
            responses_dir = Path(responses_dir)
        
        if not responses_dir.exists():
            logger.error(f"Responses directory not found: {responses_dir}")
            return {}
        
        # Load all analysis files
        analyses = {}
        for model in ['claude', 'gemini', 'gpt']:
            for ext in ['.json', '.md']:
                file_path = responses_dir / f"analysis_{model}{ext}"
                if file_path.exists():
                    content = file_path.read_text()
                    try:
                        # Extract JSON from markdown if needed
                        if ext == '.md':
                            import re
                            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                            if json_match:
                                content = json_match.group(1)
                        analyses[model] = json.loads(content)
                        logger.info(f"✅ Loaded {model} analysis")
                    except json.JSONDecodeError as e:
                        logger.warning(f"Could not parse {model} analysis: {e}")
        
        if not analyses:
            logger.error("No valid analyses found. Please complete manual analysis first.")
            return {}
        
        # Synthesize patterns across models
        all_patterns = {}
        for model, analysis in analyses.items():
            for pattern in analysis.get('patterns_identified', []):
                pid = pattern.get('pattern_id') or pattern.get('name', '').lower().replace(' ', '_')
                if pid not in all_patterns:
                    all_patterns[pid] = {
                        'pattern_id': pid,
                        'name': pattern.get('name', pid),
                        'category': pattern.get('category', 'general'),
                        'frequency': pattern.get('frequency', 1),
                        'consistency_score': pattern.get('consistency_score', 5),
                        'skill_viability': pattern.get('skill_viability', 5),
                        'task_references': pattern.get('task_references', []),
                        'models_identified': [model]
                    }
                else:
                    # Merge: higher scores, more models = better confidence
                    existing = all_patterns[pid]
                    existing['frequency'] = max(existing['frequency'], pattern.get('frequency', 1))
                    existing['consistency_score'] = max(existing['consistency_score'], pattern.get('consistency_score', 5))
                    existing['skill_viability'] = max(existing['skill_viability'], pattern.get('skill_viability', 5))
                    existing['task_references'] = list(set(existing['task_references'] + pattern.get('task_references', [])))
                    existing['models_identified'].append(model)
        
        # Boost viability for patterns found by multiple models
        for pid, pattern in all_patterns.items():
            model_count = len(pattern['models_identified'])
            if model_count >= 2:
                pattern['skill_viability'] = min(10, pattern['skill_viability'] + 0.5)
            if model_count >= 3:
                pattern['skill_viability'] = min(10, pattern['skill_viability'] + 0.5)
        
        # Save patterns to database
        viable_patterns = []
        for pattern in all_patterns.values():
            self.db.save_pattern(pattern)
            if pattern['skill_viability'] >= self.min_skill_viability:
                viable_patterns.append(pattern)
        
        logger.info(f"🔍 Identified {len(all_patterns)} patterns total")
        logger.info(f"🎯 {len(viable_patterns)} patterns viable for skill creation")
        
        # Synthesize skill recommendations
        all_skills = {}
        for model, analysis in analyses.items():
            for skill in analysis.get('recommended_skills', []):
                name = skill.get('skill_name', '').lower().replace(' ', '_')
                if name not in all_skills:
                    all_skills[name] = {
                        **skill,
                        'models_recommended': [model]
                    }
                else:
                    all_skills[name]['models_recommended'].append(model)
        
        # Mark analyzed tasks
        analyzed_ids = set()
        for analysis in analyses.values():
            tasks = self.db.get_unanalyzed_tasks()
            for t in tasks[:analysis.get('tasks_analyzed', 0)]:
                analyzed_ids.add(t['task_id'])
        
        if analyzed_ids:
            self.db.mark_tasks_analyzed(list(analyzed_ids))
        
        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'models_used': list(analyses.keys()),
            'patterns_found': len(all_patterns),
            'viable_patterns': len(viable_patterns),
            'skills_recommended': len(all_skills),
            'tasks_marked_analyzed': len(analyzed_ids)
        }
        
        logger.info("\n✅ Synthesis Complete!")
        logger.info(f"   Patterns saved: {len(all_patterns)}")
        logger.info(f"   Skills recommended: {len(all_skills)}")
        logger.info(f"   Tasks marked analyzed: {len(analyzed_ids)}")
        
        if viable_patterns:
            logger.info("\n🎯 Ready for skill generation!")
            logger.info("   Run: python orchestrator.py --generate")
        
        return synthesis
    
    def generate_skills(self) -> List[Dict]:
        """Generate skills from viable patterns"""
        patterns = self.db.get_pending_patterns(min_viability=self.min_skill_viability)
        
        if not patterns:
            logger.info("No viable patterns pending skill creation")
            return []
        
        logger.info(f"🔨 Generating prompts for {len(patterns)} skills...")
        
        generated = []
        output_dir = Path(__file__).parent.parent.parent / 'prompts' / 'skills'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for pattern in patterns:
            prompt = self._create_skill_prompt(pattern)
            
            filename = f"skill_{pattern['pattern_id']}_{datetime.now().strftime('%Y%m%d')}.md"
            output_path = output_dir / filename
            output_path.write_text(prompt)
            
            generated.append({
                'pattern_id': pattern['pattern_id'],
                'name': pattern['name'],
                'prompt_file': str(output_path)
            })
            
            logger.info(f"   📝 {pattern['name']} → {filename}")
        
        logger.info("")
        logger.info("⏸️  MANUAL ACTION REQUIRED:")
        logger.info(f"   1. Review skill prompts in {output_dir}")
        logger.info("   2. Submit each to Claude Code")
        logger.info("   3. Save generated skills to skills/ directory")
        
        return generated
    
    def _create_skill_prompt(self, pattern: Dict) -> str:
        """Create a skill generation prompt from a pattern"""
        # Get related tasks for context
        task_refs = pattern.get('task_references', [])
        
        prompt = f"""# SKILL CREATION REQUEST

## Pattern Being Converted
- **Name**: {pattern['name']}
- **Category**: {pattern['category']}
- **Viability Score**: {pattern['skill_viability']}/10
- **Frequency**: {pattern['frequency']} occurrences
- **Consistency**: {pattern['consistency_score']}/10

## Related Tasks
Task IDs: {', '.join(task_refs[:5])}

## SKILL REQUIREMENTS

Create a complete AI skill following this structure:

### SKILL.md Structure
```markdown
---
name: {pattern['name'].lower().replace(' ', '-')}
description: [Comprehensive description including when to use this skill]
---

# {pattern['name']}

## Overview
[What this skill does and why it's useful]

## When to Use
[Specific triggers and scenarios]

## Process
[Step-by-step workflow]

## Inputs Required
[What Claude needs to execute this skill]

## Outputs
[What the skill produces]

## Examples
[Concrete usage examples]

## Common Issues
[Known challenges and solutions]
```

### Requirements
1. Keep SKILL.md under 500 lines
2. Include practical code examples
3. Reference BrevardBidderAI context where relevant
4. Make it immediately actionable
5. Include error handling guidance

### BrevardBidderAI Context
- Foreclosure auction intelligence platform
- 12-stage pipeline processing
- Multi-source data aggregation
- ML scoring with XGBoost
- Supabase database
- Python + TypeScript stack

Generate a production-ready skill that will save time on repetitive {pattern['category']} tasks.
"""
        return prompt
    
    def optimize_skills(self) -> List[Dict]:
        """Identify and generate optimization prompts for underperforming skills"""
        candidates = self.db.get_underperforming_skills(
            min_uses=5,
            max_success_rate=0.8
        )
        
        if not candidates:
            logger.info("✅ All skills performing well! No optimization needed.")
            return []
        
        logger.info(f"🔧 Found {len(candidates)} skills needing optimization:")
        
        output_dir = Path(__file__).parent.parent.parent / 'prompts' / 'optimization'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        optimizations = []
        for skill in candidates:
            usage_stats = self.db.get_usage_stats(skill['skill_id'])
            
            prompt = self._create_optimization_prompt(skill, usage_stats)
            
            filename = f"optimize_{skill['skill_id']}_{datetime.now().strftime('%Y%m%d')}.md"
            output_path = output_dir / filename
            output_path.write_text(prompt)
            
            optimizations.append({
                'skill_id': skill['skill_id'],
                'name': skill['name'],
                'success_rate': skill['success_rate'],
                'prompt_file': str(output_path)
            })
            
            logger.info(f"   📝 {skill['name']} (success: {skill['success_rate']*100:.0f}%)")
        
        return optimizations
    
    def _create_optimization_prompt(self, skill: Dict, usage_stats: Dict) -> str:
        """Create an optimization prompt for an underperforming skill"""
        prompt = f"""# SKILL OPTIMIZATION REQUEST

## Skill Details
- **ID**: {skill['skill_id']}
- **Name**: {skill['name']}
- **Category**: {skill['category']}
- **Version**: {skill['version']}

## Current Performance
- Total Uses: {usage_stats.get('total_uses', 0)}
- Success Rate: {usage_stats.get('success_rate', 0)*100:.1f}%
- Avg Time Saved: {usage_stats.get('avg_time_saved', 0)} minutes
- Avg Rating: {usage_stats.get('avg_rating', 0):.1f}/5
- Avg Iterations: {usage_stats.get('avg_iterations', 0):.1f}

## Current Content
```markdown
{skill.get('content', 'Content not available')}
```

## OPTIMIZATION TASK

Analyze why this skill is underperforming and provide improvements:

### 1. Root Cause Analysis
- Why is the success rate low?
- What causes multiple iterations?
- Where does the skill fail?

### 2. Recommended Changes
- Specific content improvements
- Additional examples needed
- Error handling additions
- Clarity improvements

### 3. Updated SKILL.md
Provide the complete updated skill content.

### 4. Validation Criteria
How to verify the optimization worked.

Focus on:
- Clearer instructions
- Better error handling
- More comprehensive examples
- Reduced ambiguity
"""
        return prompt


def main():
    parser = argparse.ArgumentParser(
        description='BrevardBidderAI Skills System Orchestrator'
    )
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--analyze', action='store_true', help='Generate analysis prompt')
    parser.add_argument('--synthesize', action='store_true', help='Synthesize multi-model analyses')
    parser.add_argument('--generate', action='store_true', help='Generate skills from patterns')
    parser.add_argument('--optimize', action='store_true', help='Optimize underperforming skills')
    parser.add_argument('--responses-dir', type=str, help='Directory with analysis responses')
    
    args = parser.parse_args()
    
    orchestrator = SkillsOrchestrator()
    
    if args.status:
        orchestrator.status()
    elif args.analyze:
        if orchestrator.check_analysis_ready():
            orchestrator.generate_analysis_prompt()
        else:
            logger.info("Not enough tasks for analysis. Continue documenting!")
    elif args.synthesize:
        orchestrator.synthesize_analyses(args.responses_dir)
    elif args.generate:
        orchestrator.generate_skills()
    elif args.optimize:
        orchestrator.optimize_skills()
    else:
        # Default: show status
        orchestrator.status()


if __name__ == "__main__":
    main()
