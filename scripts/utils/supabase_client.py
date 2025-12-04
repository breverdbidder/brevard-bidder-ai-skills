#!/usr/bin/env python3
"""
BrevardBidderAI Skills System - Supabase Client (Adapted)
Uses existing tables with specific activity_type/insight_type values.
No new tables required!

Storage Strategy:
- activities (activity_type='skill_task') → task documentation
- insights (insight_type='ai_skill') → skills  
- insights (insight_type='skill_pattern') → patterns
- activities (activity_type='skill_usage') → usage tracking
"""

import os
import json
import requests
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any

# Credentials from environment or hardcoded for autonomous operation
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://mocerqjnksmhcjzxrewo.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vY2VycWpua3NtaGNqenhyZXdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDUzMjUyNiwiZXhwIjoyMDgwMTA4NTI2fQ.fL255mO0V8-rrU0Il3L41cIdQXUau-HRQXiamTqp9nE")


@dataclass
class TaskDoc:
    """Task documentation for AI Skills learning"""
    task_id: str
    title: str
    description: str
    task_type: str  # feature|bugfix|refactor|enhancement|config
    category: str   # backend|frontend|database|api|scraping|ml|reporting|testing|deployment
    complexity_score: int  # 1-10
    files_affected: List[str]
    implementation: Dict[str, Any]
    challenges: List[Dict[str, Any]]
    outcome: Dict[str, Any]
    skill_potential: int  # 1-10
    analyzed: bool = False
    created_at: Optional[str] = None


@dataclass  
class AISkill:
    """Generated AI skill from pattern analysis"""
    skill_id: str
    name: str
    category: str
    version: str
    description: str
    content: str  # The actual skill markdown
    pattern_sources: List[str]  # task_ids that contributed
    total_uses: int = 0
    success_rate: float = 0.0
    avg_time_saved: float = 0.0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class SkillUsage:
    """Track skill usage for optimization"""
    skill_id: str
    success: bool
    time_saved_minutes: int
    iterations: int
    rating: int  # 1-5
    feedback: Optional[str] = None
    used_at: Optional[str] = None


class SupabaseSkillsClient:
    """Client for AI Skills System using existing Supabase tables"""
    
    def __init__(self):
        self.url = SUPABASE_URL
        self.headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """Make authenticated request to Supabase"""
        url = f"{self.url}/rest/v1/{endpoint}"
        r = requests.request(method, url, headers=self.headers, json=data, params=params)
        if r.status_code >= 400:
            raise Exception(f"Supabase error {r.status_code}: {r.text}")
        return r.json() if r.text else {}
    
    # ========== TASK DOCUMENTATION ==========
    
    def save_task(self, task: TaskDoc) -> dict:
        """Save task documentation to activities table"""
        record = {
            "activity_type": "skill_task",
            "platform": "ai_skills_system",
            "domain": task.category.upper(),
            "notes": json.dumps({
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "task_type": task.task_type,
                "category": task.category,
                "complexity_score": task.complexity_score,
                "files_affected": task.files_affected,
                "implementation": task.implementation,
                "challenges": task.challenges,
                "outcome": task.outcome,
                "skill_potential": task.skill_potential,
                "analyzed": task.analyzed
            }),
            "focus_quality": task.complexity_score,
            "energy_level": task.skill_potential
        }
        return self._request("POST", "activities", record)
    
    def get_unanalyzed_tasks(self, limit: int = 50) -> List[dict]:
        """Get tasks not yet analyzed for patterns"""
        params = {
            "activity_type": "eq.skill_task",
            "order": "created_at.desc",
            "limit": limit
        }
        results = self._request("GET", "activities", params=params)
        tasks = []
        for r in results:
            try:
                data = json.loads(r.get("notes", "{}"))
                if not data.get("analyzed", False):
                    tasks.append(data)
            except:
                pass
        return tasks
    
    def mark_tasks_analyzed(self, task_ids: List[str]):
        """Mark tasks as analyzed"""
        # We'd need to update each record - simplified for now
        pass
    
    # ========== AI SKILLS ==========
    
    def save_skill(self, skill: AISkill) -> dict:
        """Save AI skill to insights table"""
        record = {
            "insight_type": "ai_skill",
            "title": skill.name,
            "description": skill.description,
            "source": "ai_skills_system",
            "priority": "High",
            "status": "Active",
            "confidence": skill.success_rate,
            "action_taken": json.dumps({
                "skill_id": skill.skill_id,
                "category": skill.category,
                "version": skill.version,
                "content": skill.content,
                "pattern_sources": skill.pattern_sources,
                "total_uses": skill.total_uses,
                "avg_time_saved": skill.avg_time_saved
            }),
            "recurrence_count": skill.total_uses
        }
        return self._request("POST", "insights", record)
    
    def get_all_skills(self) -> List[dict]:
        """Get all AI skills"""
        params = {
            "insight_type": "eq.ai_skill",
            "status": "eq.Active",
            "order": "created_at.desc"
        }
        results = self._request("GET", "insights", params=params)
        skills = []
        for r in results:
            try:
                data = json.loads(r.get("action_taken", "{}"))
                data["name"] = r.get("title")
                data["description"] = r.get("description")
                data["success_rate"] = r.get("confidence", 0)
                data["total_uses"] = r.get("recurrence_count", 0)
                skills.append(data)
            except:
                pass
        return skills
    
    def get_underperforming_skills(self, min_uses: int = 5, max_success_rate: float = 0.8) -> List[dict]:
        """Get skills that need optimization"""
        all_skills = self.get_all_skills()
        return [s for s in all_skills if s.get("total_uses", 0) >= min_uses and s.get("success_rate", 1) < max_success_rate]
    
    # ========== SKILL USAGE ==========
    
    def log_skill_usage(self, usage: SkillUsage) -> dict:
        """Log skill usage for tracking"""
        record = {
            "activity_type": "skill_usage",
            "platform": "ai_skills_system",
            "domain": "BUSINESS",
            "notes": json.dumps({
                "skill_id": usage.skill_id,
                "success": usage.success,
                "time_saved_minutes": usage.time_saved_minutes,
                "iterations": usage.iterations,
                "rating": usage.rating,
                "feedback": usage.feedback
            }),
            "focus_quality": usage.rating * 2,
            "duration_minutes": usage.time_saved_minutes
        }
        return self._request("POST", "activities", record)
    
    # ========== PATTERNS ==========
    
    def save_pattern(self, pattern: dict) -> dict:
        """Save identified pattern"""
        record = {
            "insight_type": "skill_pattern",
            "title": pattern.get("name"),
            "description": pattern.get("description", ""),
            "source": "ai_skills_system",
            "priority": "Medium",
            "status": "Pending" if not pattern.get("synthesized") else "Processed",
            "confidence": pattern.get("viability_score", 0) / 10,
            "action_taken": json.dumps(pattern)
        }
        return self._request("POST", "insights", record)
    
    def get_pending_patterns(self) -> List[dict]:
        """Get patterns pending skill creation"""
        params = {
            "insight_type": "eq.skill_pattern",
            "status": "eq.Pending",
            "order": "confidence.desc"
        }
        results = self._request("GET", "insights", params=params)
        patterns = []
        for r in results:
            try:
                data = json.loads(r.get("action_taken", "{}"))
                patterns.append(data)
            except:
                pass
        return patterns
    
    # ========== METRICS ==========
    
    def get_system_metrics(self) -> dict:
        """Get overall system metrics"""
        skills = self.get_all_skills()
        
        total_uses = sum(s.get("total_uses", 0) for s in skills)
        total_time_saved = sum(s.get("avg_time_saved", 0) * s.get("total_uses", 0) for s in skills)
        avg_success = sum(s.get("success_rate", 0) for s in skills) / len(skills) if skills else 0
        
        # Count tasks
        task_count_params = {"activity_type": "eq.skill_task", "select": "id"}
        tasks = self._request("GET", "activities", params=task_count_params)
        
        return {
            "total_skills": len(skills),
            "total_uses": total_uses,
            "total_time_saved_hours": total_time_saved / 60,
            "avg_success_rate": avg_success,
            "tasks_documented": len(tasks),
            "skills_by_category": self._group_by_category(skills)
        }
    
    def _group_by_category(self, skills: List[dict]) -> dict:
        """Group skills by category"""
        groups = {}
        for s in skills:
            cat = s.get("category", "other")
            groups[cat] = groups.get(cat, 0) + 1
        return groups


# Convenience function
def get_client() -> SupabaseSkillsClient:
    return SupabaseSkillsClient()


if __name__ == "__main__":
    # Test connection
    client = get_client()
    metrics = client.get_system_metrics()
    print("✅ AI Skills System Connected!")
    print(f"   Skills: {metrics['total_skills']}")
    print(f"   Tasks Documented: {metrics['tasks_documented']}")
    print(f"   Time Saved: {metrics['total_time_saved_hours']:.1f}h")
