#!/usr/bin/env python3
"""
BrevardBidderAI Skills System - Database Initialization
Creates required tables in Supabase

Created by: Ariel Shapira, Solo Founder - Everest Capital USA
"""

import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.supabase_client import get_client

# SQL for creating tables (for reference - execute via Supabase dashboard)
CREATE_TABLES_SQL = """
-- =========================================
-- BREVARDBIIDERAI AI SKILLS SYSTEM TABLES
-- =========================================
-- Run this SQL in Supabase SQL Editor

-- Task Documentation Table
CREATE TABLE IF NOT EXISTS skill_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT CHECK (task_type IN ('feature', 'bugfix', 'refactor', 'enhancement', 'config')),
    category TEXT CHECK (category IN ('backend', 'frontend', 'database', 'api', 'testing', 'deployment', 'scraping', 'ml', 'reporting')),
    complexity_score INT CHECK (complexity_score BETWEEN 1 AND 10),
    files_affected JSONB DEFAULT '[]'::jsonb,
    implementation JSONB DEFAULT '{}'::jsonb,
    challenges JSONB DEFAULT '[]'::jsonb,
    outcome JSONB DEFAULT '{}'::jsonb,
    skill_potential INT CHECK (skill_potential BETWEEN 1 AND 10),
    analyzed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_skill_tasks_analyzed ON skill_tasks(analyzed);
CREATE INDEX IF NOT EXISTS idx_skill_tasks_category ON skill_tasks(category);
CREATE INDEX IF NOT EXISTS idx_skill_tasks_potential ON skill_tasks(skill_potential);

-- AI Skills Table
CREATE TABLE IF NOT EXISTS ai_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    version TEXT DEFAULT '1.0.0',
    description TEXT,
    content TEXT,
    pattern_sources TEXT[] DEFAULT '{}',
    total_uses INT DEFAULT 0,
    success_rate DECIMAL(5,3) DEFAULT 0,
    avg_time_saved INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_skills_category ON ai_skills(category);
CREATE INDEX IF NOT EXISTS idx_ai_skills_success ON ai_skills(success_rate);

-- Skill Usage Tracking Table
CREATE TABLE IF NOT EXISTS skill_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id TEXT REFERENCES ai_skills(skill_id) ON DELETE CASCADE,
    success BOOLEAN NOT NULL,
    time_saved_minutes INT DEFAULT 0,
    iterations INT DEFAULT 1,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    used_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_skill_usage_skill ON skill_usage(skill_id);
CREATE INDEX IF NOT EXISTS idx_skill_usage_date ON skill_usage(used_at);

-- Pattern Identification Table
CREATE TABLE IF NOT EXISTS skill_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    frequency INT DEFAULT 1,
    consistency_score DECIMAL(3,1) CHECK (consistency_score BETWEEN 1 AND 10),
    skill_viability DECIMAL(3,1) CHECK (skill_viability BETWEEN 1 AND 10),
    task_references TEXT[] DEFAULT '{}',
    synthesized BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_patterns_viability ON skill_patterns(skill_viability);
CREATE INDEX IF NOT EXISTS idx_patterns_synthesized ON skill_patterns(synthesized);

-- Enable Row Level Security (optional)
-- ALTER TABLE skill_tasks ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE ai_skills ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE skill_usage ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE skill_patterns ENABLE ROW LEVEL SECURITY;

-- Create a view for dashboard metrics
CREATE OR REPLACE VIEW skills_dashboard_metrics AS
SELECT 
    (SELECT COUNT(*) FROM skill_tasks) as total_tasks,
    (SELECT COUNT(*) FROM skill_tasks WHERE analyzed = FALSE) as pending_analysis,
    (SELECT COUNT(*) FROM ai_skills) as total_skills,
    (SELECT COUNT(*) FROM skill_patterns) as total_patterns,
    (SELECT COALESCE(SUM(total_uses), 0) FROM ai_skills) as total_uses,
    (SELECT COALESCE(AVG(success_rate), 0) FROM ai_skills WHERE total_uses > 0) as avg_success_rate,
    (SELECT COALESCE(SUM(avg_time_saved * total_uses), 0) / 60.0 FROM ai_skills) as total_hours_saved;

-- Grant access (adjust as needed)
-- GRANT SELECT ON skills_dashboard_metrics TO anon;
-- GRANT ALL ON skill_tasks TO anon;
-- GRANT ALL ON ai_skills TO anon;
-- GRANT ALL ON skill_usage TO anon;
-- GRANT ALL ON skill_patterns TO anon;
"""


def check_tables_exist(client) -> dict:
    """Check which tables exist"""
    tables = ['skill_tasks', 'ai_skills', 'skill_usage', 'skill_patterns']
    status = {}
    
    for table in tables:
        try:
            result = client.client.table(table).select('id').limit(1).execute()
            status[table] = True
        except Exception as e:
            if 'does not exist' in str(e) or '42P01' in str(e):
                status[table] = False
            else:
                # Table might exist but has no data
                status[table] = True
    
    return status


def main():
    print("\n🚀 BrevardBidderAI Skills System - Database Setup")
    print("=" * 60)
    
    client = get_client()
    
    print("\n📊 Checking existing tables...")
    table_status = check_tables_exist(client)
    
    all_exist = all(table_status.values())
    
    for table, exists in table_status.items():
        status = "✅ EXISTS" if exists else "❌ MISSING"
        print(f"   {table}: {status}")
    
    if all_exist:
        print("\n✅ All tables exist! Database is ready.")
        
        # Show current stats
        overview = client.get_system_overview()
        print(f"\n📈 Current Stats:")
        print(f"   Tasks documented: {overview['total_tasks']}")
        print(f"   Skills created: {overview['total_skills']}")
        print(f"   Patterns identified: {overview['total_patterns']}")
    else:
        print("\n⚠️  Some tables are missing!")
        print("\n📋 To create tables, run the following SQL in Supabase Dashboard:")
        print("   1. Go to: https://supabase.com/dashboard")
        print("   2. Select your project")
        print("   3. Go to SQL Editor")
        print("   4. Paste and run the SQL below:")
        print("\n" + "-" * 60)
        print(CREATE_TABLES_SQL)
        print("-" * 60)
        
        # Save SQL to file
        sql_file = Path(__file__).parent / 'schema.sql'
        sql_file.write_text(CREATE_TABLES_SQL)
        print(f"\n💾 SQL also saved to: {sql_file}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
