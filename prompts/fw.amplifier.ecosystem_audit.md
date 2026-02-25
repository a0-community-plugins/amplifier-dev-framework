# Amplifier Ecosystem Audit

Audit all public Amplifier ecosystem repositories for compliance with standards and guidelines. This covers both full ecosystem audits and individual repository audits.

## Ecosystem Audit Overview

The ecosystem audit discovers all public repositories starting with "amplifier" in the Microsoft GitHub organization and audits each for compliance with:

- Listed in MODULES.md for discoverability
- Required Microsoft boilerplate files present and matching
- README.md Contributing and Trademarks sections
- GitHub Issues status
- Repository activity stats

## Running an Ecosystem Audit

### Full Ecosystem Audit

```bash
# Discover and audit all amplifier repos
amplifier recipes execute amplifier-ecosystem-audit.yaml

# With fix PR creation enabled
amplifier recipes execute amplifier-ecosystem-audit.yaml \
  --context '{"create_fix_prs": "true"}'

# Audit specific repos only (skip discovery)
amplifier recipes execute amplifier-ecosystem-audit.yaml \
  --context '{"repos": ["amplifier-core", "amplifier-foundation"]}'

# Include community (non-Microsoft) repos
amplifier recipes execute amplifier-ecosystem-audit.yaml \
  --context '{"include_community": "true"}'
```

### Single Repository Audit

```bash
# Basic audit
amplifier recipes execute repo-audit.yaml \
  --context '{"repo_name": "amplifier-core"}'

# Audit with fix PR creation
amplifier recipes execute repo-audit.yaml \
  --context '{"repo_name": "amplifier-module-tool-web", "create_fix_pr": "true"}'

# Audit a non-Microsoft repo
amplifier recipes execute repo-audit.yaml \
  --context '{"repo_owner": "robotdad", "repo_name": "amplifier-app-transcribe"}'
```

## Ecosystem Audit Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `repos` | `[]` (auto-discover) | Specific repo names to audit |
| `include_community` | `"false"` | Include non-Microsoft repos from MODULES.md |
| `create_fix_prs` | `"false"` | Create PRs for fixable issues |
| `dry_run` | `"false"` | Preview mode without creating PRs |
| `max_repos` | `100` | Safety limit on total repos |
| `working_dir` | `"./ai_working/ecosystem-audit"` | Working directory |
| `report_filename` | `"ecosystem-audit-report.md"` | Output report filename |

## Audit Stages

### Stage 1: Discovery and Planning

1. **Setup** -- Create working directories
2. **Discover repos** -- Search GitHub API for amplifier repos, or use manually provided list
3. **Discover community repos** -- (Optional) Extract non-Microsoft repos from MODULES.md
4. **Merge and validate** -- Combine repo lists, check against safety limit
5. **Create audit plan** -- Generate summary for review before proceeding
6. **Approval gate** -- Human reviews the plan before execution

### Stage 2: Per-Repository Audits

Each repository is audited in parallel (max 2 concurrent) using the single-repo audit recipe. Each audit checks:

1. **MODULES.md listing** -- Is the repo listed for discoverability?
2. **Boilerplate files** -- CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, LICENSE match reference
3. **README sections** -- Contributing and Trademarks sections are verbatim from template
4. **GitHub Issues** -- Disabled for non-main repos (recommended)
5. **Repository stats** -- Open PRs, recent commits, last push date

### Stage 3: Aggregation and Reporting

1. **Collect individual reports** -- Gather summaries from each repo audit
2. **Aggregate results** -- Count pass/attention/critical statuses
3. **Generate ecosystem report** -- Comprehensive markdown report with executive summary
4. **Write report** -- Save to working directory

## Single Repository Audit Checks

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| MODULES.md | Repo name appears in table | recommendation |
| CODE_OF_CONDUCT.md | Verbatim match with reference | error |
| SECURITY.md | Verbatim match with reference | error |
| SUPPORT.md | Verbatim match with reference | error |
| LICENSE | Verbatim match with reference | error |
| README Contributing | Section matches template | warning/error |
| README Trademarks | Section matches template | warning/error |
| GitHub Issues | Disabled for non-main repos | recommendation |

## Fix PR Creation

When `create_fix_pr` is enabled:

1. **Deduplication check** -- Looks for existing open PRs on `fix/compliance-boilerplate-update` branch
2. **Prepare fixes** -- Copies correct boilerplate files from reference repo (amplifier-core)
3. **Fix README** -- Updates Contributing and Trademarks sections to match template
4. **Validate fixes** -- Confirms section order and content
5. **Create instructions** -- Generates PR instructions with shell commands

The `dry_run` mode shows what would be fixed without creating any PRs.

## Output

```
ai_working/ecosystem-audit/
  repos/
    {repo-name}/
      audit-report.md
      fixes/           (if create_fix_pr enabled)
  reports/
    ecosystem-audit-report.md
    aggregate-data.json
  audit-started.txt
```

## Requirements

- `gh` CLI installed and authenticated (`gh auth status`)
- Write access to repos if `create_fix_prs` is enabled
- The `repo-audit.yaml` recipe available in the same directory
