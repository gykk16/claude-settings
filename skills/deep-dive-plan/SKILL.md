---
name: deep-dive-plan
description: Multi-agent collaborative planning system using parallel Analyzer team, specialized Planner, and parallel Validator team for thorough pre-implementation analysis. Use when complex features need deep analysis before coding.
---

# Deep Dive Planning System

$ARGUMENTS

## Overview

This skill orchestrates specialized agent teams to produce comprehensive implementation plans before writing any code. Each phase uses parallel sub-agents for speed, while phases run sequentially to maintain data dependencies.

**Use this skill when:**
- Complex features requiring architectural decisions
- High-risk changes needing careful analysis
- Multi-component system modifications
- Unclear implementation paths requiring exploration
- Need for documented decision-making process

**Do NOT use for:**
- Simple bug fixes or trivial changes
- Well-understood patterns with clear implementation
- Quick prototypes or experiments

## Three-Phase System

```
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  Phase 1: ANALYZE (parallel)                                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐              │
│  │ 🔍 Explorer  │ │ 📊 Analyst   │ │ 🛡️ Risk Assessor │              │
│  │   (haiku)    │ │   (opus)     │ │    (sonnet)      │              │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘              │
│         └────────────────┼──────────────────┘                        │
│                    Synthesize → Analysis Report                       │
│                          ↓                                            │
│  Phase 2: PLAN (sequential)                                           │
│  ┌──────────────────────────────────┐                                │
│  │ 📋 Planner (opus)                │                                │
│  │ Strategy based on Analysis       │                                │
│  └──────────────┬───────────────────┘                                │
│                 ↓                                                      │
│  Phase 3: VALIDATE (parallel)                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐              │
│  │ ✅ Verifier  │ │ 🧐 Critic    │ │ 📋 Quality Check │              │
│  │   (sonnet)   │ │   (opus)     │ │    (sonnet)      │              │
│  └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘              │
│         └────────────────┼──────────────────┘                        │
│                    Synthesize → Validation Report                     │
│                          ↓                                            │
│              ✅ APPROVED / 🔄 ITERATE / ❌ REJECTED                   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## Agent Type Resolution

This skill uses specialized OMC agents when available, with built-in Claude Code fallbacks.

**Detection**: Try the OMC type first. If the Task tool rejects the `subagent_type`, use the fallback.

| Role | OMC Type (preferred) | Fallback Type | Model |
|------|---------------------|---------------|-------|
| Explorer | `oh-my-claudecode:explore` | `Explore` | haiku |
| Analyst | `oh-my-claudecode:analyst` | `general-purpose` | opus |
| Risk Assessor | `oh-my-claudecode:security-reviewer` | `security-engineer` | sonnet |
| Planner | `oh-my-claudecode:planner` | `general-purpose` | opus |
| Verifier | `oh-my-claudecode:verifier` | `general-purpose` | sonnet |
| Critic | `oh-my-claudecode:critic` | `general-purpose` | opus |
| Quality Reviewer | `oh-my-claudecode:quality-reviewer` | `quality-engineer` | sonnet |

> **Note**: OMC agents carry role-specific system prompts that improve output quality. Fallbacks work correctly but rely entirely on the prompt you provide, so include the full role description in the prompt when using fallbacks.

## Phase 1: Analyzer Team

**Goal**: Deep codebase exploration and current state analysis using 3 parallel agents.

### Team Composition

| Agent | OMC Type | Fallback | Model | Responsibility |
|-------|----------|----------|-------|----------------|
| Explorer | `oh-my-claudecode:explore` | `Explore` | haiku | Codebase structure, file mapping, existing patterns |
| Analyst | `oh-my-claudecode:analyst` | `general-purpose` | opus | Dependencies, constraints, integration points |
| Risk Assessor | `oh-my-claudecode:security-reviewer` | `security-engineer` | sonnet | Risk identification, security concerns, impact areas |

### How It Works

1. **Launch 3 agents in parallel** using Task tool with `run_in_background: true`
2. **Each agent works independently** on their focus area
3. **Synthesize results** into a unified Analysis Report after all complete

### Explorer Agent Prompt

```
You are the Explorer for deep-dive planning. Map the codebase structure for: [USER REQUEST]

**Focus**:
1. Map project structure and architecture patterns
2. Find code locations relevant to the request (file paths + line numbers)
3. Identify existing patterns similar to what's needed
4. Document the technology stack and conventions

**Output**:
## Explorer Findings

### Architecture Overview
[Project structure, design patterns, component relationships]

### Relevant Code Locations
- `path/to/file.ts:45-89` - [What this code does]

### Existing Patterns
[Similar implementations found in codebase]

### Technology Stack
[Languages, frameworks, libraries in use]
```

### Analyst Agent Prompt

```
You are the Analyst for deep-dive planning. Analyze dependencies and constraints for: [USER REQUEST]

**Focus**:
1. Map internal dependencies (modules, components affected)
2. Identify external dependencies (libraries, services, APIs)
3. Discover technical constraints (language, framework, performance)
4. Identify business constraints (timeline, compliance, compatibility)
5. Flag open questions that need user input

**Output**:
## Analyst Findings

### Internal Dependencies
| Component | Relationship | Impact Level |
|-----------|--------------|--------------|

### External Dependencies
| Package | Version | Purpose | Risk |
|---------|---------|---------|------|

### Technical Constraints
[Language/framework limitations, performance requirements]

### Business Constraints
[Timeline, compliance, backwards compatibility needs]

### Open Questions
[Questions that need user input before planning]
```

### Risk Assessor Agent Prompt

```
You are the Risk Assessor for deep-dive planning. Identify risks and impact areas for: [USER REQUEST]

**Focus**:
1. Identify risks at all severity levels (Critical/High/Medium/Low)
2. Map impact areas (files to modify, components affected, blast radius)
3. Assess security implications
4. Evaluate test coverage impact
5. Find technical debt that may complicate the work

**Output**:
## Risk Assessment Findings

### Risks Identified
- 🚨 Critical: [Blockers, breaking changes]
- ⚠️ High: [Major technical debt, complex refactors]
- 🔶 Medium: [Edge cases, testing challenges]
- 🔵 Low: [Minor concerns]

### Impact Areas
- Files to modify/create
- Components affected (direct/indirect)
- Test coverage impact

### Security Implications
[Authentication, authorization, data safety concerns]

### Technical Debt Discovered
[Existing issues that may complicate implementation]
```

### Synthesized Output Format

After all 3 agents complete, synthesize into:

```markdown
## 🔍 Analysis Report

### 1. Current State
[From Explorer: architecture, code locations, patterns]

### 2. Dependencies
[From Analyst: internal, external, infrastructure]

### 3. Constraints
[From Analyst: technical, business]

### 4. Risks Identified
[From Risk Assessor: all severity levels]

### 5. Impact Areas
[From Risk Assessor: files, components, tests]

### 6. Recommendations for Planner
[Synthesized from all three agents' findings]
- Preferred approach
- Approaches to avoid
- Open questions for user
```

## Phase 2: Planner Agent

**Goal**: Strategic implementation planning based on analysis. Single specialized agent.

### Agent Configuration

| Agent | OMC Type | Fallback | Model | Responsibility |
|-------|----------|----------|-------|----------------|
| Planner | `oh-my-claudecode:planner` | `general-purpose` | opus | Full implementation strategy |

### Planner Agent Prompt

```
Use Task tool with subagent_type="oh-my-claudecode:planner" and model="opus":

"You are the Planner for deep-dive planning. Review the Analyzer team's findings and create a comprehensive implementation strategy.

**Analyzer Team's Report**:
[PASTE THE COMPLETE SYNTHESIZED ANALYSIS REPORT]

**Required Tasks**:
1. Review all findings from Analyzer team thoroughly
2. Design implementation approach addressing all identified risks
3. Break down work into logical phases (3-5 phases)
4. Document architectural decisions with rationales
5. Create detailed task breakdown for each phase
6. Identify parallel execution opportunities within phases

**Output Requirements**:
Produce an Implementation Strategy following this structure:

## 📋 Implementation Strategy

### 1. Approach
High-level strategy and why this approach

### 2. Architectural Decisions
For each major decision:
- **Decision**: What was decided
- **Options Considered**: Alternatives with pros/cons
- **Rationale**: Why this choice
- **Trade-offs**: What we're accepting

### 3. Implementation Phases
For each phase (typically 3-5):
- **Phase N: [Name]**
  - Goal: What this achieves
  - Tasks: Specific deliverables with actions
  - Parallel Opportunities: Tasks that can run concurrently
  - Testing: How to verify
  - Completion Criteria: When phase is done

### 4. Timeline Estimate
Realistic time estimates per phase

### 5. Success Criteria
Measurable, testable criteria for completion

### 6. Rollback Strategy
How to undo changes if needed

### 7. Risk Mitigation Plan
Address each high/critical risk from Analysis

Be specific. Include file paths, function names, concrete examples. The Validator team will review your strategy against the Analysis."
```

**Wait for Planner output before proceeding.**

## Phase 3: Validator Team

**Goal**: Critical evaluation and risk assessment using 3 parallel agents.

### Team Composition

| Agent | OMC Type | Fallback | Model | Responsibility |
|-------|----------|----------|-------|----------------|
| Verifier | `oh-my-claudecode:verifier` | `general-purpose` | sonnet | Cross-validate Plan against Analysis |
| Critic | `oh-my-claudecode:critic` | `general-purpose` | opus | Challenge strategy, find flaws, assess alternatives |
| Quality Reviewer | `oh-my-claudecode:quality-reviewer` | `quality-engineer` | sonnet | Feasibility, completeness, measurability |

### How It Works

1. **Launch 3 agents in parallel** using Task tool with `run_in_background: true`
2. **Each agent reviews both Analysis and Plan** from their perspective
3. **Synthesize results** into a unified Validation Report with final decision

### Verifier Agent Prompt

```
You are the Verifier for deep-dive planning. Cross-validate the Plan against the Analysis.

**Analyzer Team's Report**: [PASTE]
**Planner's Strategy**: [PASTE]

**Focus**:
1. Are all risks from Analysis addressed in Plan?
2. Are all dependencies mapped to specific tasks?
3. Are all impact areas covered by phases?
4. Spot-check claims: verify code references with Grep/Read

**Output**:
## Verifier Findings

### Cross-Validation
- Risk [X]: ✅ Addressed in Phase Y / ⚠️ Partially / ❌ Missing
- Dependency [X]: ✅ Mapped to Task Y / ❌ Not mapped

### Spot Checks
- Claim: "[quote]" → ✅ Verified / ❌ Incorrect

### Gaps Found
[Any analysis findings not covered by the plan]
```

### Critic Agent Prompt

```
You are the Critic for deep-dive planning. Challenge the strategy and find flaws.

**Analyzer Team's Report**: [PASTE]
**Planner's Strategy**: [PASTE]

**Focus**:
1. Challenge architectural decisions - are alternatives properly considered?
2. Find logical flaws in the approach
3. Identify hidden assumptions
4. Assess if the strategy is the simplest viable approach (YAGNI)
5. Check for scope creep beyond user's request

**Output**:
## Critic Findings

### Decisions Challenged
- Decision [X]: [Challenge or agreement with reasoning]

### Logical Flaws
[Any contradictions or gaps in reasoning]

### Hidden Assumptions
[Unstated assumptions that could cause problems]

### Scope Assessment
[Is the plan right-sized for the request?]
```

### Quality Reviewer Agent Prompt

```
You are the Quality Reviewer for deep-dive planning. Assess feasibility and completeness.

**Analyzer Team's Report**: [PASTE]
**Planner's Strategy**: [PASTE]

**Focus**:
1. Rate risk dimensions (Technical Feasibility, Complexity, Dependencies, Time, Reversibility)
2. Check success criteria are measurable
3. Verify rollback strategy is viable
4. Assess testing strategy adequacy
5. Check error handling and monitoring coverage

**Output**:
## Quality Review Findings

### Risk Scoring Matrix
| Dimension | Score (1-5) | Reasoning |
|-----------|-------------|-----------|
| Technical Feasibility | | |
| Complexity | | |
| Dependencies | | |
| Time Estimate | | |
| Reversibility | | |
| **OVERALL** | **[avg]** | **[Low/Medium/High/Critical]** |

### Completeness Checklist
- [ ] Testing strategy adequate
- [ ] Error handling considered
- [ ] Performance implications addressed
- [ ] Security considerations included
- [ ] Rollback strategy viable
- [ ] Success criteria measurable

### Issues Found
- 🚨 Critical: [Must fix]
- ⚠️ Major: [Should fix]
- 🔶 Minor: [Nice to have]
```

### Synthesized Validation Decision

After all 3 validator agents complete, synthesize into a final decision:

```markdown
## ✅ Validation Report

### 1. Risk Assessment
[From Quality Reviewer: risk scoring matrix]

### 2. Cross-Validation Results
[From Verifier: risk/dependency/impact coverage]

### 3. Strategic Assessment
[From Critic: decision challenges, flaws, assumptions]

### 4. Completeness Assessment
[From Quality Reviewer: checklist results]

### 5. Issues Found
[Consolidated from all three agents]
- 🚨 Critical Issues (Must Fix)
- ⚠️ Major Concerns (Should Fix)
- 🔶 Minor Suggestions (Nice to Have)

### 6. Decision
**Status**: [✅ APPROVED | 🔄 NEEDS REVISION | ❌ REJECTED]

**Decision Logic**:
- If ANY critical issues → ❌ REJECTED or 🔄 NEEDS REVISION
- If major concerns only → 🔄 NEEDS REVISION
- If minor suggestions only → ✅ APPROVED

**Reasoning**: [Why this decision]
**Required Actions**: [If not approved, what must change]
```

## Workflow

**CRITICAL: Execution Rules**

1. **ALWAYS use Task tool** - Never execute agent logic directly
2. **Parallel within phases** - Launch sub-agents in parallel within each phase
3. **Sequential between phases** - Analyzer Team → Planner → Validator Team
4. **Store all outputs** - Save each agent's output for reference in subsequent phases
5. **Synthesize before handoff** - Combine parallel agent outputs before passing to next phase
6. **Iterate based on Validator** - Only re-run failed agents, not all

### Step 1: Initialize

Start by understanding the user's request and determining scope.

```markdown
**User Request**: [Summarize what user wants]
**Scope**: [file | module | project | system]
**Estimated Complexity**: [Low | Medium | High | Critical]
```

### Step 2: Launch Analyzer Team (Parallel)

**IMPORTANT**: Launch all 3 agents in parallel using Task tool. Do NOT perform analysis yourself.

```
Launch in parallel (use run_in_background: true for each):
Use OMC types if available, otherwise use fallback types (see Agent Type Resolution).

1. Task(subagent_type="oh-my-claudecode:explore",  # fallback: "Explore"
        model="haiku",
        prompt="[Explorer prompt with USER REQUEST]")

2. Task(subagent_type="oh-my-claudecode:analyst",  # fallback: "general-purpose"
        model="opus",
        prompt="[Analyst prompt with USER REQUEST]")

3. Task(subagent_type="oh-my-claudecode:security-reviewer",  # fallback: "security-engineer"
        model="sonnet",
        prompt="[Risk Assessor prompt with USER REQUEST]")
```

**Wait for ALL 3 agents to complete, then synthesize into unified Analysis Report.**

If any agent's findings raise questions for the user, use **AskUserQuestion** before proceeding.

### Step 3: Launch Planner Agent (Sequential)

**IMPORTANT**: Only run after Analyzer Team completes and synthesis is done.

```
Task(subagent_type="oh-my-claudecode:planner",  # fallback: "general-purpose"
     model="opus",
     prompt="[Planner prompt with SYNTHESIZED ANALYSIS REPORT]")
```

**Wait for Planner output before proceeding.**

### Step 4: Launch Validator Team (Parallel)

**IMPORTANT**: Only run after Planner completes. All 3 validators need both Analysis and Plan.

```
Launch in parallel (use run_in_background: true for each):
Use OMC types if available, otherwise use fallback types (see Agent Type Resolution).

1. Task(subagent_type="oh-my-claudecode:verifier",  # fallback: "general-purpose"
        model="sonnet",
        prompt="[Verifier prompt with ANALYSIS + PLAN]")

2. Task(subagent_type="oh-my-claudecode:critic",  # fallback: "general-purpose"
        model="opus",
        prompt="[Critic prompt with ANALYSIS + PLAN]")

3. Task(subagent_type="oh-my-claudecode:quality-reviewer",  # fallback: "quality-engineer"
        model="sonnet",
        prompt="[Quality Reviewer prompt with ANALYSIS + PLAN]")
```

**Wait for ALL 3 agents to complete, then synthesize into Validation Report with decision.**

### Step 5: Iteration (If Needed)

**Analyze Validator Team's Decision**:

If **✅ APPROVED**: Proceed to Step 6 (Finalization)

If **🔄 NEEDS REVISION** or **❌ REJECTED**:

1. **Read consolidated feedback** from all 3 validators
2. **Identify which phase needs re-run**:
   - Missing analysis / wrong assumptions → Re-run specific **Analyzer agent(s)** (not full team)
   - Flawed strategy / poor decisions → Re-run **Planner** with feedback
   - Need user clarification → Use **AskUserQuestion** tool

3. **Re-run only what's needed**:
   - Include Validator team's specific feedback in the agent prompt
   - Reference original outputs: "Previous analysis showed X, but Validator identified gap Y"
   - If only one Analyzer sub-area failed, re-run only that agent (not all 3)

4. **Re-run Validator Team** after changes:
   - Always validate again after any changes
   - Pass updated outputs to all 3 validators

**Iteration Limit**: Maximum 3 iterations. If still not approved after 3 rounds, ask user for guidance.

### Step 6: Finalization

Once Validator Team returns **✅ APPROVED**:

1. **Consolidate all reports** into single comprehensive document
2. **Save to claudedocs/**: `claudedocs/deep-dive-plan-[feature-name].md`
3. **Create executive summary**: 2-3 sentences covering What, Why, How, Risk Level
4. **Present to user**: Show summary with key decisions and recommendations
5. **Get user approval**: Use AskUserQuestion to confirm before any implementation begins

## Output Structure

Save the final approved plan to `claudedocs/deep-dive-plan-[feature-name].md`:

```markdown
# Deep Dive Plan: [Feature Name]

**Created**: [Date]
**Status**: Validated and Approved
**Overall Risk**: [Low/Medium/High/Critical]
**Agents Used**: Explorer(haiku) + Analyst(opus) + Risk Assessor(sonnet) | Planner(opus) | Verifier(sonnet) + Critic(opus) + Quality Reviewer(sonnet)

---

## Executive Summary
[2-3 sentences: What, Why, How]

---

## Analysis Report
[Synthesized from Explorer + Analyst + Risk Assessor]

---

## Implementation Strategy
[Full Planner output]

---

## Validation Report
[Synthesized from Verifier + Critic + Quality Reviewer]

---

## Next Steps

Ready to implement? Use this plan with:
- `/software-engineer` for implementation
- `/commit` for incremental commits following phases
- `/review` for code review after each phase

**Recommendation**: Implement one phase at a time, validate, then proceed.
```

## Best Practices

1. **Always use Task tool for agents**: Never perform agent work yourself - delegate to Task agents
2. **Parallel within, sequential between**: Sub-agents run in parallel; phases run sequentially
3. **Use `run_in_background: true`**: Launch parallel agents as background tasks for true concurrency
4. **Synthesize before handoff**: Combine parallel outputs into coherent report before next phase
5. **Right-size agent models**: haiku for exploration, opus for deep reasoning, sonnet for verification
6. **Pass complete context**: Each phase needs full synthesized output from previous phase
7. **Let agents work independently**: Don't inject opinions between agent phases
8. **Trust the process**: If Validator Team rejects, iterate - don't skip validation
9. **Re-run surgically**: On iteration, only re-run the specific agent(s) that need changes
10. **User approval required**: Always confirm final plan before implementation

## Anti-Patterns to Avoid

- **Doing agent work yourself**: Never perform analysis/planning/validation directly - always delegate
- **Running phases in parallel**: Planner needs Analysis; Validators need both - phases must be sequential
- **Using general-purpose for everything**: Use specialized agent types for better results
- **Skipping synthesis**: Don't pass raw parallel outputs directly - synthesize first
- **Skipping Validator Team**: Never implement without validation approval
- **Running full team on iteration**: If only one sub-area failed, re-run only that agent
- **Rushing to code**: This skill is about planning, not implementation
- **Analysis paralysis**: If Validator Team approves, move forward - don't over-iterate

## Integration with Other Skills

- **After deep-dive-plan**: Use `/software-engineer` for implementation
- **During implementation**: Use `/review` after each phase
- **For commits**: Use `/commit` with phase-based messages
- **For PRs**: Use `/create-pr` referencing the plan document

---

**Remember**: The goal is a validated, comprehensive plan that makes implementation straightforward and low-risk. Parallel agents speed up each phase without sacrificing thoroughness.
