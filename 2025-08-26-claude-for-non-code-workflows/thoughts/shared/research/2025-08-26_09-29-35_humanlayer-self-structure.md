---
date: 2025-08-26T09:29:35-07:00
researcher: dexhorthy
git_commit: e19d55aa22a632b2e94d1c7b6ac322b3a47df41a
branch: main
repository: humanlayer/self
topic: "Structure and Usage of tools/ and company/ directories"
tags: [research, codebase, tools, company, crm, sops, frontmatter, context-management]
status: complete
last_updated: 2025-08-26
last_updated_by: dexhorthy
---

# Research: Structure and Usage of tools/ and company/ directories in humanlayer/self

**Date**: 2025-08-26T09:29:35-07:00
**Researcher**: dexhorthy
**Git Commit**: e19d55aa22a632b2e94d1c7b6ac322b3a47df41a
**Branch**: main
**Repository**: humanlayer/self

## Research Question
Research the STRUCTURE AND USAGE of ../__PATH__
- Tools that exist and their purposes
- Make print-context and print-index functionality
- Structure of dailies, release notes, and SOPs
- Running notes file formats
- CRM structure
- How frontmatter is used for slicing with scripts


## Detailed Findings

### Tools Directory Architecture

#### Organization Structure
The tools/ directory follows a service-based organization pattern:
- **Communication Tools**: `/gmail/` - Python-based Gmail API for investor updates
- **Project Management**: `/linear/` - TypeScript tool for issue tracking and daily reviews
- **Calendar Integration**: `/calendar/` - Google Calendar API for meeting context
- **Task Management**: `/omnifocus/` - macOS integration via JXA scripts
- **Marketing**: `/loops/` - CSV processing for email platform
- **Media**: `/video/`, `/youtube/` - Video processing and upload utilities
- **Context Tracking**: `recent-files.ts` - Tracks markdown file modifications

#### Key Design Principles
- **Technology Stack Distribution**:
  - Python tools use `uv` for dependency management (e.g., Gmail)
  - TypeScript/Node.js tools use Bun runtime (Linear, Calendar, YouTube)
  - Shell scripts for simple wrappers and examples
  - JXA for macOS-specific integrations (OmniFocus)

- **Common Patterns**:
  - Audit logging to `journal-tools.yaml` for activity tracking
  - Makefile-based build system with consistent commands
  - CLI-first design with `--summary` requirements for AI agents
  - Output to `data/raw/YYYY-MM-DD-descriptive-name.md` format

### Company Directory Structure

#### Major Components
1. **Standard Operating Procedures (`/sops/`)**
   - Dual-purpose documents for humans and AI agents
   - Frequency-based organization (daily, weekly, monthly)
   - Key SOPs: daily-review-rw, weekly-planning, release-notes, investor-updates

2. **CRM System (`/crm/`)**
   - Three-tier structure: accounts (top/other), contacts, events
   - MEDDICC sales methodology templates
   - Event naming: `YYYY-MM-DD__ACCOUNT__TYPE_SUMMARY_attendees.md`
   - Cross-linking between entities

3. **Getting Things Done (`/gtd/`)**
   - Core files: next_actions, today_plan, finished_items, waiting, deferred
   - Project organization with active/archived separation
   - @context tags and urgency levels

4. **Data Management (`/data/`)**
   - Three-tier processing: raw → processed → golden
   - Content types: Linear summaries, waitlist exports, transcripts
   - Golden data as single source of truth

5. **Daily Operations (`/dailies/`)**
   - Comprehensive daily review documents
   - Two-phase process: READ (gather) → WRITE (update)
   - Integration with GTD and CRM systems

### Make print-context and print-index

#### make print-context
**Purpose**: Consolidates key company context for AI agent consumption

**Implementation**:
```makefile
# Outputs in order:
company/humanlayer.md              # Company identity
company/manifest.md                # Asset registry
company/metrics/README.md          # Metrics overview
head -100 company/all-hands-meeting-notes.md
head -200 company/weekly-updates.md
head -200 company/monthly-investor-updates.md
head -100 company/quarterly-goals.md
company/tools.md                   # Full file
head -100 company/journal.md
```

**Strategy**: Provides curated, truncated context to prevent information overload while preserving essential business state.

#### make print-index
**Purpose**: Generates comprehensive file index with frontmatter metadata

**Implementation**: Calls `hack/index-files.ts company`
- Recursively scans for `.md` files
- Extracts YAML frontmatter
- Outputs structured index: `===path/to/file.md===` + YAML
- Excludes: .git, node_modules, build directories

#### make print-crm-index
**Purpose**: Specialized CRM indexer with visual directory tree

**Implementation**: Calls `hack/crm-index.ts`
- Generates ASCII tree structure
- Lists all CRM files with frontmatter
- Visual navigation aid for relationship tracking

### Frontmatter System and Slicing Scripts

#### Standard Frontmatter Structure
```yaml
---
summary: Brief description
last_updated: YYYY-MM-DD
last_updated_by: username
last_update: Description of changes
[additional_fields]: context-specific
---
```

#### File-Type Specific Fields
- **SOPs**: `sop__frequency`, `sop__timing`, `sop__dependencies`
- **CRM Contacts**: `name`, `title`, `email`, `linkedin`, `tags`
- **CRM Events**: `event_type`, `contact`, `account`, `outcome`
- **Communications**: `to`, `subject` for email tracking

#### Slicing Scripts

1. **Frontmatter Validation** (`hack/check-frontmatter.ts`)
   - Validates required fields and date formats
   - Warns about short descriptions
   - Supports `.frontmatterignore` patterns

2. **Recent Files Tracker** (`tools/recent-files.ts`)
   - Filters by `last_updated` date ranges
   - Groups chronologically
   - Used in daily review workflows

3. **File Indexing** (`hack/index-files.ts`)
   - Extracts all frontmatter for search/filter
   - Creates searchable metadata catalog
   - Enables content discovery

4. **SOP Frequency Filtering**
   - Filters by `sop__frequency` field
   - Enables automated task scheduling
   - Supports: daily, weekly, monthly, as-needed, passive
