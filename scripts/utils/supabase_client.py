#!/usr/bin/env python3
"""
BrevardBidderAI Skills System - Supabase Client
Database operations for the AI Skills Development System

Created by: Ariel Shapira, Solo Founder - Everest Capital USA
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

try:
    from supabase import create_client, Client
except ImportError:
    print("Installing supabase-py...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'supabase', '--quiet'])
    from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BrevardBidderAI Supabase Configuration
# Set these in your environment or .env file
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://mocerqjnksmhcjzxrewo.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# Check for .env file in project root
from pathlib import Path
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists() and not SUPABASE_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    except ImportError:
        pass

if not SUPABASE_KEY:
    logger.warning("⚠️ SUPABASE_KEY not set. Set in environment or .env file.")


@dataclass
class TaskDoc:
    """Task documentation structure"""
    task_id: str
    title: str
    description: str
    task_type: str  # feature, bugfix, refactor, enhancement
    category: str  # backend, frontend, database, api, testing, deployment
    complexity_score: int  # 1-10
    files_affected: List[str]
    implementation: Dict[str, Any]
    challenges: List[Dict[str, Any]]
    outcome: Dict[str, Any]
    skill_potential: int  # 1-10
    analyzed: bool = False


@dataclass
class AISkill:
    """AI Skill structure"""
    skill_id: str
    name: str
    category: str
    version: str
    description: str
    content: str
    pattern_sources: List[str]
    total_uses: int = 0
    success_rate: float = 0.0
    avg_time_saved: int = 0


@dataclass
class SkillUsage:
    """Skill usage record"""
    skill_id: str
    success: bool
    time_saved_minutes: int
    iterations: int
    rating: int  # 1-5
    feedback: Optional[str] = None


class SupabaseSkillsClient:
    """Supabase client for AI Skills System"""
    
    def __init__(self, url: str = SUPABASE_URL, key: str = SUPABASE_KEY):
        self.client: Client = create_client(url, key)
        logger.info(f"✅ Connected to Supabase: {url}")
    
    # ==================== TASK DOCUMENTATION ====================
    
    def save_task(self, task: TaskDoc) -> Dict:
        """Save a task documentation record"""
        data = {
            'task_id': task.task_id,
            'title': task.title,
            'description': task.description,
            'task_type': task.task_type,
            'category': task.category,
            'complexity_score': task.complexity_score,
            'files_affected': task.files_affected,
            'implementation': task.implementation,
            'challenges': task.challenges,
            'outcome': task.outcome,
            'skill_potential': task.skill_potential,
            'analyzed': task.analyzed,
            'created_at': datetime.now().isoformat()
        }
        
        result = self.client.table('skill_tasks').upsert(data).execute()
        logger.info(f"📝 Saved task: {task.task_id}")
        return result.data[0] if result.data else {}
    
    def get_unanalyzed_tasks(self, limit: int = 50) -> List[Dict]:
        """Get tasks that haven't been analyzed yet"""
        result = self.client.table('skill_tasks')\
            .select('*')\
            .eq('analyzed', False)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        return result.data
    
    def count_unanalyzed_tasks(self) -> int:
        """Count tasks pending analysis"""
        result = self.client.table('skill_tasks')\
            .select('id', count='exact')\
            .eq('analyzed', False)\
            .execute()
        return result.count or 0
    
    def mark_tasks_analyzed(self, task_ids: List[str]) -> None:
        """Mark tasks as analyzed"""
        for task_id in task_ids:
            self.client.table('skill_tasks')\
                .update({'analyzed': True})\
                .eq('task_id', task_id)\
                .execute()
        logger.info(f"✅ Marked {len(task_ids)} tasks as analyzed")
    
    def get_tasks_by_category(self) -> Dict[str, int]:
        """Get task count breakdown by category"""
        result = self.client.table('skill_tasks').select('category').execute()
        breakdown = {}
        for row in result.data:
            cat = row['category']
            breakdown[cat] = breakdown.get(cat, 0) + 1
        return breakdown
    
    def get_high_potential_tasks(self, min_score: int = 7) -> List[Dict]:
        """Get tasks with high skill creation potential"""
        result = self.client.table('skill_tasks')\
            .select('*')\
            .gte('skill_potential', min_score)\
            .order('skill_potential', desc=True)\
            .execute()
        return result.data
    
    # ==================== AI SKILLS ====================
    
    def save_skill(self, skill: AISkill) -> Dict:
        """Save or update an AI skill"""
        data = {
            'skill_id': skill.skill_id,
            'name': skill.name,
            'category': skill.category,
            'version': skill.version,
            'description': skill.description,
            'content': skill.content,
            'pattern_sources': skill.pattern_sources,
            'total_uses': skill.total_uses,
            'success_rate': skill.success_rate,
            'avg_time_saved': skill.avg_time_saved,
            'updated_at': datetime.now().isoformat()
        }
        
        result = self.client.table('ai_skills').upsert(data).execute()
        logger.info(f"🎯 Saved skill: {skill.skill_id}")
        return result.data[0] if result.data else {}
    
    def get_all_skills(self) -> List[Dict]:
        """Get all AI skills"""
        result = self.client.table('ai_skills')\
            .select('*')\
            .order('updated_at', desc=True)\
            .execute()
        return result.data
    
    def get_skill(self, skill_id: str) -> Optional[Dict]:
        """Get a specific skill by ID"""
        result = self.client.table('ai_skills')\
            .select('*')\
            .eq('skill_id', skill_id)\
            .single()\
            .execute()
        return result.data
    
    def get_skills_by_category(self) -> Dict[str, List[Dict]]:
        """Get skills organized by category"""
        skills = self.get_all_skills()
        by_category = {}
        for skill in skills:
            cat = skill['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(skill)
        return by_category
    
    def get_underperforming_skills(self, 
                                    min_uses: int = 5,
                                    max_success_rate: float = 0.8,
                                    max_rating: float = 3.5) -> List[Dict]:
        """Get skills that need optimization"""
        result = self.client.table('ai_skills')\
            .select('*')\
            .gte('total_uses', min_uses)\
            .lt('success_rate', max_success_rate)\
            .execute()
        return result.data
    
    # ==================== SKILL USAGE ====================
    
    def log_usage(self, usage: SkillUsage) -> Dict:
        """Log skill usage"""
        data = {
            'skill_id': usage.skill_id,
            'success': usage.success,
            'time_saved_minutes': usage.time_saved_minutes,
            'iterations': usage.iterations,
            'rating': usage.rating,
            'feedback': usage.feedback,
            'used_at': datetime.now().isoformat()
        }
        
        result = self.client.table('skill_usage').insert(data).execute()
        
        # Update skill aggregate metrics
        self._update_skill_metrics(usage.skill_id)
        
        logger.info(f"📊 Logged usage for skill: {usage.skill_id}")
        return result.data[0] if result.data else {}
    
    def _update_skill_metrics(self, skill_id: str) -> None:
        """Update aggregate metrics for a skill"""
        # Get all usage records for this skill
        result = self.client.table('skill_usage')\
            .select('*')\
            .eq('skill_id', skill_id)\
            .execute()
        
        if not result.data:
            return
        
        usages = result.data
        total_uses = len(usages)
        successes = sum(1 for u in usages if u['success'])
        success_rate = successes / total_uses if total_uses > 0 else 0
        avg_time_saved = sum(u['time_saved_minutes'] for u in usages) // total_uses if total_uses > 0 else 0
        
        self.client.table('ai_skills')\
            .update({
                'total_uses': total_uses,
                'success_rate': round(success_rate, 3),
                'avg_time_saved': avg_time_saved,
                'updated_at': datetime.now().isoformat()
            })\
            .eq('skill_id', skill_id)\
            .execute()
    
    def get_usage_stats(self, skill_id: str, days: int = 30) -> Dict:
        """Get usage statistics for a skill"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        result = self.client.table('skill_usage')\
            .select('*')\
            .eq('skill_id', skill_id)\
            .gte('used_at', since)\
            .execute()
        
        usages = result.data
        if not usages:
            return {'total_uses': 0, 'success_rate': 0, 'avg_time_saved': 0}
        
        return {
            'total_uses': len(usages),
            'success_rate': sum(1 for u in usages if u['success']) / len(usages),
            'avg_time_saved': sum(u['time_saved_minutes'] for u in usages) // len(usages),
            'avg_rating': sum(u['rating'] for u in usages) / len(usages),
            'avg_iterations': sum(u['iterations'] for u in usages) / len(usages)
        }
    
    # ==================== PATTERNS ====================
    
    def save_pattern(self, pattern: Dict) -> Dict:
        """Save an identified pattern"""
        data = {
            'pattern_id': pattern['pattern_id'],
            'name': pattern['name'],
            'category': pattern['category'],
            'frequency': pattern['frequency'],
            'consistency_score': pattern['consistency_score'],
            'skill_viability': pattern['skill_viability'],
            'task_references': pattern['task_references'],
            'synthesized': False,
            'created_at': datetime.now().isoformat()
        }
        
        result = self.client.table('skill_patterns').upsert(data).execute()
        logger.info(f"🔍 Saved pattern: {pattern['pattern_id']}")
        return result.data[0] if result.data else {}
    
    def get_pending_patterns(self, min_viability: float = 7.0) -> List[Dict]:
        """Get patterns ready for skill creation"""
        result = self.client.table('skill_patterns')\
            .select('*')\
            .eq('synthesized', False)\
            .gte('skill_viability', min_viability)\
            .order('skill_viability', desc=True)\
            .execute()
        return result.data
    
    def mark_pattern_synthesized(self, pattern_id: str) -> None:
        """Mark a pattern as used for skill creation"""
        self.client.table('skill_patterns')\
            .update({'synthesized': True})\
            .eq('pattern_id', pattern_id)\
            .execute()
        logger.info(f"✅ Pattern {pattern_id} marked as synthesized")
    
    # ==================== SYSTEM METRICS ====================
    
    def get_system_overview(self) -> Dict:
        """Get overall system metrics"""
        tasks = self.client.table('skill_tasks').select('id', count='exact').execute()
        skills = self.client.table('ai_skills').select('*').execute()
        patterns = self.client.table('skill_patterns').select('id', count='exact').execute()
        
        skill_data = skills.data or []
        total_uses = sum(s.get('total_uses', 0) for s in skill_data)
        total_time_saved = sum(s.get('avg_time_saved', 0) * s.get('total_uses', 0) for s in skill_data)
        avg_success_rate = (
            sum(s.get('success_rate', 0) for s in skill_data) / len(skill_data)
            if skill_data else 0
        )
        
        return {
            'total_tasks': tasks.count or 0,
            'total_skills': len(skill_data),
            'total_patterns': patterns.count or 0,
            'total_uses': total_uses,
            'total_time_saved_hours': round(total_time_saved / 60, 1),
            'avg_success_rate': round(avg_success_rate, 3),
            'pending_analysis': self.count_unanalyzed_tasks()
        }
    
    def log_system_event(self, event_type: str, details: Dict) -> None:
        """Log a system event to activities table"""
        data = {
            'activity_type': f'skills_system_{event_type}',
            'description': json.dumps(details),
            'created_at': datetime.now().isoformat()
        }
        
        try:
            self.client.table('activities').insert(data).execute()
            logger.info(f"📋 Logged event: {event_type}")
        except Exception as e:
            logger.warning(f"Could not log event: {e}")


# Singleton instance
_client: Optional[SupabaseSkillsClient] = None

def get_client() -> SupabaseSkillsClient:
    """Get or create the Supabase client singleton"""
    global _client
    if _client is None:
        _client = SupabaseSkillsClient()
    return _client


if __name__ == "__main__":
    # Test connection
    client = get_client()
    overview = client.get_system_overview()
    print("\n🚀 BrevardBidderAI Skills System - Database Connection Test")
    print("=" * 60)
    print(f"📄 Total Tasks Documented: {overview['total_tasks']}")
    print(f"🎯 Total Skills Created: {overview['total_skills']}")
    print(f"🔍 Total Patterns Identified: {overview['total_patterns']}")
    print(f"⏱️  Total Time Saved: {overview['total_time_saved_hours']} hours")
    print(f"✅ Average Success Rate: {overview['avg_success_rate']*100:.1f}%")
    print(f"📊 Pending Analysis: {overview['pending_analysis']} tasks")
    print("=" * 60)
