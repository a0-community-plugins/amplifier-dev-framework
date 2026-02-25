# Amplifier Repository Activity Analysis

Recipes for analyzing GitHub repository activity -- single repo analysis and multi-repo ecosystem activity reports.

## Single Repository Analysis

### Overview

Analyzes a single GitHub repository for commits and PRs in a date range. Defaults to the current working directory and "since yesterday".

### Running Repository Analysis

**In a session (recommended)**:
```
"run repo-activity-analysis"
"analyze this repo's activity for the last week"
```

**From CLI**:
```bash
# Analyze current repo since yesterday (default)
amplifier tool invoke recipes operation=execute \
  recipe_path=repo-activity-analysis.yaml

# Explicit repo
amplifier tool invoke recipes operation=execute \
  recipe_path=repo-activity-analysis.yaml \
  context='{"repo_url": "https://github.com/microsoft/amplifier-core"}'

# Custom date range
amplifier tool invoke recipes operation=execute \
  recipe_path=repo-activity-analysis.yaml \
  context='{"date_range": "last 7 days"}'

# Large repo with 5000+ commits
amplifier tool invoke recipes operation=execute \
  recipe_path=repo-activity-analysis.yaml \
  context='{"date_range": "last 30 days", "max_chunk_iterations": 200}'
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `repo_url` | (detect from CWD) | GitHub repo URL to analyze |
| `date_range` | `"since yesterday"` | Natural language date range |
| `working_dir` | `"./ai_working"` | Working directory for output |
| `include_deep_dive` | `true` | Deep analysis for unclear changes |

### How It Works

1. **Detect repo** -- Parse URL or detect from git remote
2. **Parse date range** -- Convert natural language to ISO date format
3. **Fetch commits** -- Retrieve commits with pagination, create token-budgeted chunks (~6000 tokens each)
4. **Analyze commit chunks** -- Foreach loop analyzes each chunk independently
5. **Synthesize commit analysis** -- Combine chunk results into unified analysis
6. **Fetch and analyze PRs** -- Retrieve merged and open PRs
7. **Deep dive** -- (Optional) Detailed analysis for unclear or complex changes
8. **Generate summary** -- Produce final analysis document

### Scaling

The recipe uses token-based chunking to handle large repositories:

```
max_commits = max_chunk_iterations * commits_per_chunk
Default: 100 * 30 = 3,000 commits
For larger repos: increase max_chunk_iterations proportionally
Example: 6,000 commits -> max_chunk_iterations: 200
```

### Model Selection

- **Haiku** for simple tasks: date parsing, commit chunk categorization
- **Sonnet** for complex tasks: synthesis, PR analysis, deep dives
- No opus needed -- repo analysis does not require maximum reasoning

### Output Contract

The recipe returns a structured success/failure response:

**Success**:
```json
{"success": true, "manifest_path": "...", "files_written": 5, "counts": {...}}
```

**Failure**:
```json
{"success": false, "error": "...", "failed_step": "...", "partial_files": [...]}
```

---

## Ecosystem Activity Report

### Overview

Analyzes activity across the Amplifier ecosystem by discovering repos from MODULES.md. Top-level entry point for comprehensive ecosystem analysis.

### Running Ecosystem Reports

**In a session (recommended)**:
```
"run the ecosystem-activity-report recipe"
"show me all ecosystem activity since yesterday"
"what has robotdad been working on this week?"
```

**From CLI**:
```bash
# Your activity today (default)
amplifier tool invoke recipes operation=execute \
  recipe_path=amplifier:recipes/ecosystem-activity-report.yaml

# All ecosystem activity since yesterday
amplifier tool invoke recipes operation=execute \
  recipe_path=amplifier:recipes/ecosystem-activity-report.yaml \
  context='{"activity_scope": "all", "date_range": "since yesterday"}'

# Specific user's activity last week
amplifier tool invoke recipes operation=execute \
  recipe_path=amplifier:recipes/ecosystem-activity-report.yaml \
  context='{"activity_scope": "robotdad", "date_range": "last week"}'
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `date_range` | `"today"` | Natural language date range |
| `activity_scope` | `""` (current user) | Who's activity: "all", username, "me and X" |
| `repo_filter` | `""` (all repos) | Regex pattern for repo names |
| `org_filter` | `"microsoft"` | GitHub organization filter |
| `working_dir` | `"./ai_working"` | Working directory |
| `report_filename` | `"ecosystem-activity-report.md"` | Output filename |
| `parallel_analysis` | `1` | Max concurrent repo analyses (1 = sequential) |
| `api_delay_seconds` | `0.5` | Delay between GitHub API calls |
| `api_retry_attempts` | `3` | Retry count for API calls |

### How It Works

1. **Discover GitHub user** -- Identify current authenticated user for filtering
2. **Parse date range** -- Convert natural language to structured date
3. **Read MODULES.md** -- Discover all ecosystem repositories
4. **Filter repos** -- Apply org and name filters
5. **Quick activity check** -- Determine which repos have activity in the date range
6. **Analyze active repos** -- Run single-repo analysis on each active repo
7. **Validate completeness** -- Ensure all expected analyses completed
8. **Synthesize report** -- Generate comprehensive markdown report

### Rate Limiting

The recipe is configured for reliability over speed:

- Sequential LLM calls (`max_concurrent_llm: 1`)
- 3-second minimum between call completions
- Adaptive backoff on 429 errors (starts at 10s, caps at 2 minutes)
- 500ms pacing within agent tool calls

### Output

```
ai_working/
  analyses/
    {repo-name}-commits.json
    {repo-name}-prs.json
    {repo-name}-analysis.json
    {repo-name}-summary.md
  reports/
    ecosystem-activity-report.md
```

## Tips

1. **Date ranges**: Use natural language -- "since yesterday", "last 7 days", "last week", "since 2024-12-01"
2. **gh CLI**: Ensure `gh` is installed and authenticated (`gh auth status`)
3. **Rate limits**: For many repos, you may hit GitHub API rate limits. The recipes include retry logic.
4. **Approval gates**: The ecosystem report has an approval gate after discovery -- review the plan before committing to a long analysis.

## Requirements

- `gh` CLI installed and authenticated
- Recipes bundle loaded (provides generic repo-activity-analysis recipe)
- Git CLI for detecting current repo in standalone mode
