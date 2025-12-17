-- Migration: Domain Content Extensions
-- Adds educational content, measurement categories, and extends config tables

-- Add content_metadata_jsonb to existing config tables for extensibility
ALTER TABLE drafting_schools 
ADD COLUMN IF NOT EXISTS content_metadata_jsonb JSONB NOT NULL DEFAULT '{}';

ALTER TABLE blocks 
ADD COLUMN IF NOT EXISTS content_metadata_jsonb JSONB NOT NULL DEFAULT '{}';

ALTER TABLE rule_graphs 
ADD COLUMN IF NOT EXISTS content_metadata_jsonb JSONB NOT NULL DEFAULT '{}';

ALTER TABLE transform_pipelines 
ADD COLUMN IF NOT EXISTS content_metadata_jsonb JSONB NOT NULL DEFAULT '{}';

ALTER TABLE ease_profiles 
ADD COLUMN IF NOT EXISTS content_metadata_jsonb JSONB NOT NULL DEFAULT '{}';

-- Create educational_content table
CREATE TABLE IF NOT EXISTS educational_content (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content_type VARCHAR(64) NOT NULL,
    content TEXT NOT NULL,
    language VARCHAR(8) NOT NULL DEFAULT 'en',
    priority INTEGER NOT NULL DEFAULT 0,
    drafting_school_id INTEGER REFERENCES drafting_schools(id),
    drafting_school_version VARCHAR(32),
    block_id INTEGER REFERENCES blocks(id),
    block_version VARCHAR(32),
    measurement_name VARCHAR(64),
    metadata_jsonb JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for educational_content
CREATE INDEX IF NOT EXISTS idx_educational_content_school 
ON educational_content(drafting_school_id, drafting_school_version);

CREATE INDEX IF NOT EXISTS idx_educational_content_block 
ON educational_content(block_id, block_version);

CREATE INDEX IF NOT EXISTS idx_educational_content_type 
ON educational_content(content_type);

CREATE INDEX IF NOT EXISTS idx_educational_content_priority 
ON educational_content(priority);

-- Create measurement_categories table
CREATE TABLE IF NOT EXISTS measurement_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    category VARCHAR(32) NOT NULL,
    description TEXT,
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    metadata_jsonb JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for config lookups
CREATE INDEX IF NOT EXISTS idx_drafting_schools_name_version 
ON drafting_schools(name, version);

CREATE INDEX IF NOT EXISTS idx_drafting_schools_active 
ON drafting_schools(is_active);

CREATE INDEX IF NOT EXISTS idx_blocks_name_version 
ON blocks(name, version);

-- Create grading_tables table
CREATE TABLE IF NOT EXISTS grading_tables (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(32) NOT NULL,
    config_jsonb JSONB NOT NULL,
    content_metadata_jsonb JSONB NOT NULL DEFAULT '{}',
    drafting_school_id INTEGER REFERENCES drafting_schools(id),
    drafting_school_version VARCHAR(32),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_grading_tables_school 
ON grading_tables(drafting_school_id, drafting_school_version);

