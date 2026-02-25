# Amplifier Reference

Amplifier is a modular AI agent framework built on the Linux kernel philosophy: a tiny, stable kernel that provides mechanisms only, with all policies and features living at the edges as replaceable modules.

**Core Principle**: "The center stays still so the edges can move fast."

## The Ecosystem

### Entry Point (amplifier)
The main repository providing user-facing documentation, getting started guides, ecosystem overview, and repository governance rules.

### Kernel (amplifier-core)
The ultra-thin kernel (~2,600 lines) providing:
- Session lifecycle management
- Module loading and unloading
- Event system and hooks
- Coordinator infrastructure
- Stable contracts and protocols

The kernel provides MECHANISMS, never POLICIES.

### Foundation Library (amplifier-foundation)
The primary library for building applications:
- Bundle primitives (composition, validation)
- Reference bundles and behaviors
- Best-practice examples
- Shared utilities

### Modules
Swappable capabilities that plug into the kernel. Exactly 5 types:

| Type | Purpose | Examples |
|------|---------|----------|
| **Provider** | LLM backends | anthropic, openai, azure, ollama |
| **Tool** | Agent capabilities (LLM-decided) | filesystem, bash, web, search, task |
| **Orchestrator** | The main engine driving sessions | loop-basic, loop-streaming, loop-events |
| **Context** | Memory management | context-simple, context-persistent |
| **Hook** | Lifecycle observers (code-decided) | logging, redaction, approval |

**Orchestrator: The Main Engine** -- The orchestrator controls the entire execution loop (LLM -> tool calls -> response). Swapping orchestrators can radically change agent behavior. It is THE control surface, not just "strategy."

**Tool vs Hook** -- Tools are LLM-decided (model chooses to call them). Hooks are code-decided (fire on lifecycle events). Both can use models internally, but the triggering mechanism differs.

### Bundles
Composable configuration packages combining providers, tools, orchestrators, behaviors (reusable capability sets), agents (specialized personas), and context files.

### Agents (Built on Bundles)
Agents ARE bundles. They use the same file format (markdown + YAML frontmatter) and are loaded via `load_bundle()`. The only difference is frontmatter convention:
- Bundles use `bundle:` with `name` and `version`
- Agents use `meta:` with `name` and `description`

When the `task` tool spawns an agent:
1. Looks up agent config from `coordinator.config["agents"]`
2. Calls the `session.spawn` capability (app-layer, not kernel)
3. Creates a new `AmplifierSession` with merged config and `parent_id` linking
4. Child session runs its own orchestrator loop and returns result

This is a foundation-layer pattern. The kernel provides session forking; "agents" are built on top.

### Recipes
Multi-step AI agent orchestration for repeatable workflows:
- Declarative YAML workflow definitions
- Context accumulation across agent handoffs
- Approval gates for human-in-loop checkpoints
- Resumability after interruption

## The Philosophy

### Mechanism, Not Policy
The kernel provides capabilities; modules decide behavior.

**Litmus test**: "Could two teams want different behavior?" If yes, it is policy. It belongs in a module, not the kernel.

### Bricks and Studs (LEGO Model)
- Each module is a self-contained "brick"
- Interfaces are "studs" where bricks connect
- Regenerate any brick independently
- Stable interfaces enable composition

### Ruthless Simplicity
- As simple as possible, but no simpler
- Every abstraction must justify its existence
- Start minimal, grow as needed
- Do not build for hypothetical futures

### Event-First Observability
- If it is important, emit an event
- Single JSONL log as source of truth
- Hooks observe without blocking
- Tracing IDs enable correlation

## Using Recipes

### How to Run Recipes

**In a session (recommended):** Just ask naturally:
```
"run repo-activity-analysis for this repo"
"analyze ecosystem activity since yesterday"
```

**From CLI:** Use `amplifier tool invoke recipes`:
```bash
amplifier tool invoke recipes operation=execute recipe_path=<recipe> context='{"key": "value"}'
```

There is no `amplifier recipes` CLI command. Recipes are invoked via the `recipes` tool.

### Available Generic Recipes

| Recipe | Description | Default |
|--------|-------------|---------|
| `repo-activity-analysis.yaml` | Single repo analysis | Current directory, since yesterday |
| `multi-repo-activity-report.yaml` | Multi-repo synthesis | Requires repo list |

### Amplifier-Specific Recipes

| Recipe | Description |
|--------|-------------|
| `ecosystem-activity-report.yaml` | Analyze activity across all Amplifier ecosystem repos |
| `amplifier-ecosystem-audit.yaml` | Audit all repos for compliance with standards |
| `repo-audit.yaml` | Audit a single repo for compliance |
| `document-generation.yaml` | Generate documentation from structured outlines |
| `outline-generation-from-doc.yaml` | Generate outlines from existing documents |

### Context Variables for Repo Analysis

| Variable | Default | Description |
|----------|---------|-------------|
| `repo_url` | (detect from CWD) | GitHub repo URL to analyze |
| `date_range` | "since yesterday" | Natural language date range |
| `working_dir` | "./ai_working" | Working directory for output |
| `include_deep_dive` | true | Deep analysis for unclear changes |

### Tips

1. **Date ranges**: Use natural language -- "since yesterday", "last 7 days", "last week", "since 2024-12-01"
2. **gh CLI**: Ensure `gh` is installed and authenticated (`gh auth status`)
3. **Rate limits**: For many repos, the recipes include retry logic and rate limiting
4. **Approval gates**: Multi-repo recipes have approval gates -- review the plan before committing to long analysis

## Getting Started Paths

### For Users
1. Start with user onboarding documentation (quick start and commands)
2. Choose a bundle from foundation
3. Run `amplifier run` with your chosen configuration

### For App Developers
1. Study foundation examples for working patterns
2. Read the bundle guide for bundle composition
3. Build your app using bundle primitives

### For Module Developers
1. Understand kernel contracts via core docs
2. Follow module protocols
3. Test modules in isolation before integration

### For Contributors
1. Read repository rules for governance
2. Understand the dependency hierarchy
3. Contribute to the appropriate repository

## Expert Agents

| Topic | Agent | Expertise |
|-------|-------|-----------|
| Ecosystem, modules, governance | amplifier-expert | MODULES.md, REPOSITORY_RULES.md, USER_ONBOARDING.md |
| Bundle authoring, patterns | foundation-expert | BUNDLE_GUIDE.md, examples, PATTERNS.md |
| Kernel internals, protocols | core-expert | Kernel contracts, HOOKS_API.md, specs |
| Recipe authoring, validation | recipe-author | RECIPE_SCHEMA.md, example recipes |
