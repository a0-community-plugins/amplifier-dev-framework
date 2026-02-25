# Amplifier Document Generation

Multi-stage recipe for generating documentation from structured outlines, with parallel validation and outline generation from existing documents.

## Document Generation from Outline

### Overview

The document generation recipe takes a structured JSON outline and produces a complete document through iterative generation and validation. It implements breadth-first traversal with parallel validation phases.

### Design Principles

- **Bash for**: File operations, JSON read/write via jq, simple checks
- **Agent for**: Parsing, understanding, reasoning, content generation
- **jq for JSON**: Clean, readable JSON manipulation in bash steps
- **Parallel checks**: Independent validations run concurrently
- **Combined fixes**: Single fix step addresses all issues holistically
- **File-based data**: Complex JSON passed via files, not template variables
- **Agent-writes-file**: Agents write document content directly to files
- **Robust fallbacks**: Three-way logic handles agent failures gracefully

### Validation Groupings

**Group 1 (Sequential -- must be first)**:
- `structural`: Ensures sections exist before content checks

**Group 2 (Parallel -- content validation)**:
- `accuracy`: Claims traceable to sources
- `completeness`: Prompts fully addressed
- `instructions`: Format and template followed

**Group 3 (Parallel -- quality validation)**:
- `depth`: Level-appropriate detail
- `coherence`: Flow, transitions, duplication
- `crossrefs`: Internal references valid
- `consistency`: Terminology and style uniform
- `tone`: Audience and purpose fit

### Version Flow

```
v0 -> [structural] -> v1 -> [content checks parallel] -> v2 ->
     [quality checks parallel] -> v3 -> final
```

### Running Document Generation

```bash
# Basic usage
amplifier run "execute document-generation.yaml with outline_path=./outline.json"

# With existing document (for updates/revisions)
amplifier run "execute document-generation.yaml \
  with outline_path=./outline.json \
  existing_document_path=./current-doc.md"
```

### Existing Document Support

When an existing document is provided:
- Analyzes structure and maps to outline sections
- Extracts per-section content with quality assessment (keep/revise/replace)
- Uses existing content as starting point when available
- Preserves good content, revises outdated content, replaces poor content
- Significantly faster for document updates and revisions

### Provider Preferences and Model Selection

Steps use optimized model selection for cost and performance:

| Task Complexity | Model Tier | Examples |
|----------------|------------|---------|
| Simple parsing | Haiku | parse-outline, extract-sources, check-structural, summary-report |
| Analysis | Sonnet | compute-relationships, assemble-document, fix-structural, content-checks, quality-checks |
| Generation | Opus | generate-section, fix-content, fix-quality |

Fallback chains provide resilience across providers:
- Haiku: anthropic haiku -> openai gpt-4o-mini
- Sonnet: anthropic sonnet -> openai gpt-4o -> azure gpt-4o
- Opus: anthropic opus -> openai gpt-4o -> azure gpt-4o

---

## Outline Generation from Existing Document

### Overview

Generates structured outlines from existing documents through multi-pass analysis. The outline captures document structure, source identification, and regeneration instructions.

### Process

1. **Analyze governance rules** -- Read repository rules and ecosystem structure
2. **Identify source documents** -- Multi-pass analysis to find authoritative sources
3. **Classify document type** -- Determine if "synthesized" (derived from sources) or "original" (authoritative)
4. **Generate prompting strategies** -- Create per-section prompts for regeneration
5. **Create structured outline** -- Output as YAML and JSON files

### Source Identification (4-Pass Analysis)

- **Pass 1**: Identify candidate sources from imports, references, and content overlap
- **Pass 2**: Verify candidates by reading actual files
- **Pass 3**: Detect directionality -- determine who references whom
- **Pass 4**: Final classification with outbound citation check

### Document Classification

The key insight for classification:
- A document with **zero outbound citations** cannot be synthesized -- it defines content authoritatively (ORIGINAL)
- A document with **few outbound citations + high authority** indicators is likely ORIGINAL
- A document with **many outbound citations + confirmed sources** is SYNTHESIZED

### Outline Structure (JSON)

```json
{
  "_meta": {
    "name": "document-outline",
    "document_type": "synthesized|original",
    "document_instruction": "High-level generation instruction",
    "model": "claude-sonnet-4-20250514",
    "source_repo": "repo-name",
    "target_path": "path/to/document.md",
    "allowed_source_repos": ["repo1", "repo2"]
  },
  "document": {
    "title": "# Document Title",
    "output": "path/to/output.md",
    "sections": [
      {
        "heading": "## Section Name",
        "level": 2,
        "prompt": "Instructions for generating this section",
        "sources": [
          {
            "file_path": "path/to/source.md",
            "contribution": "What this source provides",
            "relevance": "high|medium|low"
          }
        ],
        "sections": []
      }
    ]
  }
}
```

### Running Outline Generation

```bash
amplifier recipes execute outline-generation-from-document.yaml \
  --context '{
    "target_repo_url": "https://github.com/myorg/myrepo",
    "target_document_path": "docs/DESIGN.md"
  }'
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `target_repo_url` | (required) | GitHub URL of repo containing target document |
| `target_document_path` | (required) | Path to document within repo |
| `landing_repo_url` | amplifier repo | Landing repo with governance rules |
| `working_dir` | `"./outline_working"` | Working directory |
| `output_dir` | `"./outlines"` | Directory for final outline files |
| `model` | `"claude-sonnet-4-20250514"` | LLM model for regeneration metadata |
| `max_response_tokens` | `8000` | Token limit for regeneration |
| `temperature` | `0.2` | Temperature for regeneration |

## Requirements

- Foundation bundle (provides zen-architect, explorer agents)
- Python 3 installed
- Write access to working directory
- `gh` CLI for outline generation from remote repos
