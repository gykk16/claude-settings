# Deep Dive Planning Reference

Detailed templates, checklists, and guidelines for each agent team in the planning system.

---

## Phase 1: Analyzer Team Reference

### Explorer Agent (haiku)

#### Exploration Framework

**Goal**: Map codebase structure and identify relevant patterns

**Steps:**
1. Use Glob to map project directory structure
2. Identify main components and their relationships
3. Find existing patterns similar to what's needed
4. Document architectural style (MVC, layered, microservices, etc.)

**Questions to answer:**
- What's the overall project structure?
- What design patterns are currently used?
- How do components communicate?
- What's the data flow?

**Tools to use:**
- Glob for file discovery
- Grep for pattern searching
- Read for understanding implementations

#### Explorer Output Template

```markdown
## Explorer Findings

**Explored by**: Explorer Agent (haiku)
**Date**: [Timestamp]

---

### Architecture Overview
[Describe current architecture, key components, design patterns]

### Relevant Code Locations
- `path/to/file.ts:45-89` - [What this code does]
- `path/to/another.ts:12-34` - [What this code does]

### Existing Patterns
[Similar implementations found in codebase with file references]

### Technology Stack
- **Language**: [Language and version]
- **Framework**: [Framework and version]
- **Libraries**: [Key libraries]
- **Build Tools**: [Build system]

### Project Structure
```
src/
├── [directory structure]
```

---

**Exploration Complete** ✓
```

---

### Analyst Agent (opus)

#### Analysis Framework

**Goal**: Map all dependencies, constraints, and integration points

**Internal Dependencies:**
- Modules/packages this change will use
- Components that will be affected by this change
- Shared utilities or services involved

**External Dependencies:**
- Third-party libraries required
- APIs or services to integrate
- Database schema changes needed
- Infrastructure requirements

**Constraint Discovery:**

**Technical Constraints:**
- Language/framework version limitations
- Performance requirements (latency, throughput)
- Memory/resource constraints
- Compatibility requirements (browsers, OS)

**Business Constraints:**
- Security/compliance requirements (GDPR, SOC2)
- Scalability targets
- Backwards compatibility needs
- Timeline pressures

**Tools to use:**
- Read for examining package files and configurations
- Grep for import/dependency analysis
- Bash for `npm list`, `gradle dependencies`, etc.

#### Analyst Output Template

```markdown
## Analyst Findings

**Analyzed by**: Analyst Agent (opus)
**Date**: [Timestamp]

---

### Internal Dependencies

| Component | Relationship | Impact Level |
|-----------|--------------|--------------|
| `module.name` | [How it's related] | [Low/Medium/High] |

### External Dependencies

| Package | Version | Purpose | Risk |
|---------|---------|---------|------|
| `package-name` | ^X.Y.Z | [Why needed] | [Low/Medium/High] |

### Infrastructure Requirements
- [ ] Database migration needed
- [ ] New environment variables
- [ ] External service access
- [ ] Additional hosting resources

### Technical Constraints
- **Language**: [Version requirements and why]
- **Performance**: [Latency/throughput requirements]
- **Compatibility**: [Platform requirements]
- **Security**: [Compliance requirements]

### Business Constraints
- **Timeline**: [If mentioned by user]
- **Resources**: [Team size, availability]
- **Compliance**: [GDPR, HIPAA, etc.]

### Open Questions
1. **[Question]** - [Why it matters for planning]
2. **[Question]** - [Why it matters for planning]

---

**Analysis Complete** ✓
```

---

### Risk Assessor Agent (sonnet)

#### Risk Assessment Framework

**Goal**: Identify risks, security concerns, and impact areas

Use this risk classification:

**🚨 Critical Risks** (Blockers):
- Breaking changes to public APIs
- Data loss potential
- Security vulnerabilities
- Production outages

**⚠️ High Risks** (Major concerns):
- Performance degradation
- Complex migration paths
- High technical debt areas
- Missing critical knowledge

**🔶 Medium Risks** (Manageable):
- Edge cases to handle
- Testing challenges
- Documentation needs
- Minor breaking changes

**🔵 Low Risks** (Minor concerns):
- Code style inconsistencies
- Nice-to-have features
- Optional improvements

**Impact Assessment:**
- List all files that will be modified
- List all components that depend on modified code
- Identify integration points with other systems
- Estimate test coverage impact

**Tools to use:**
- Grep for finding usages and references
- Read for understanding code dependencies
- Bash for `git log` and history analysis

#### Risk Assessor Output Template

```markdown
## Risk Assessment Findings

**Assessed by**: Risk Assessor Agent (sonnet)
**Date**: [Timestamp]

---

### Risks Identified

#### 🚨 Critical Risks
1. **[Risk Name]**
   - **Description**: [What could go wrong]
   - **Impact**: [Consequences]
   - **Probability**: [Low/Medium/High]
   - **Mitigation**: [How to prevent/minimize]

#### ⚠️ High Risks
[Same format]

#### 🔶 Medium Risks
[Same format]

#### 🔵 Low Risks
[Same format]

### Impact Areas

#### Files to Modify
```
src/
├── directory/
│   ├── file.ts (modify)
│   └── file2.ts (create)
```

#### Components Affected
- **Direct**: [Components that will change]
- **Indirect**: [Components that depend on changes]
- **Downstream**: [Services/apps that consume this]

#### Test Coverage Impact
- **Unit tests**: X tests will break, Y new tests needed
- **Integration tests**: Z scenarios to cover
- **E2E tests**: W flows to validate

### Security Implications
- [Authentication concerns]
- [Authorization concerns]
- [Data safety concerns]

### Technical Debt Discovered
1. **[Issue Area]**
   - **Current State**: [What's problematic]
   - **Impact on Plan**: [How it affects this work]
   - **Recommendation**: [Fix now vs later]

---

**Risk Assessment Complete** ✓
```

---

### Synthesis Guide

After all 3 Analyzer Team agents complete, the orchestrator synthesizes their outputs:

1. **Merge without duplication**: Combine findings, remove overlaps
2. **Cross-reference**: Link Explorer's code locations with Risk Assessor's impact areas
3. **Prioritize**: Use Analyst's constraints to weight Risk Assessor's findings
4. **Surface questions**: Collect all open questions from Analyst before proceeding
5. **Create recommendations**: Based on all three perspectives, suggest approach for Planner

---

## Phase 2: Planner Agent Reference

### Planning Framework

#### 1. Strategy Development

**Read and internalize** the synthesized Analysis Report first.

**Ask yourself:**
- What's the simplest approach that addresses all requirements?
- What are the key architectural decisions needed?
- What can be done incrementally vs all-at-once?
- What's the critical path?
- Which tasks within phases can run in parallel?

**Principles:**
- **YAGNI**: Don't plan for hypothetical future requirements
- **Incremental**: Break into smallest valuable increments
- **Reversible**: Prefer approaches that can be undone
- **Testable**: Each phase should be verifiable
- **Parallelizable**: Identify concurrent execution opportunities

#### 2. Architectural Decision Making

For each significant decision, document using ADR format:

```markdown
### Decision: [Short title]

**Context**: [What situation requires this decision]

**Options Considered**:
1. **Option A**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Complexity: [1-5]

2. **Option B**: [Description]
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Complexity: [1-5]

**Decision**: [Chosen option]

**Rationale**: [Why this option over others]

**Trade-offs Accepted**:
- [What we're giving up]
- [What we're gaining]
```

#### 3. Phase Breakdown

Organize work into logical phases:

**Phase Types:**

1. **Foundation Phase**
   - Set up infrastructure, add dependencies, create base structures
   - **Goal**: Enable core implementation

2. **Core Implementation Phase**
   - Implement main functionality, add business logic
   - **Goal**: Working feature (may be feature-flagged)

3. **Integration Phase**
   - Connect to existing systems, wire up components
   - **Goal**: End-to-end functionality

4. **Polish Phase**
   - Error handling, performance, logging, documentation
   - **Goal**: Production-ready

**Phase Template:**
```markdown
#### Phase N: [Phase Name]

**Goal**: [What this phase achieves - must be testable]

**Prerequisites**:
- [ ] [What must be done before starting]

**Tasks**:

##### Task N.1: [Task Name]
**Deliverable**: [Concrete output]

**Actions**:
1. [Specific step with file path]
2. [Specific step with file path]

**Parallel Opportunities**: [Tasks that can run concurrently]

**Testing**:
- [ ] Unit test: [Specific test case]
- [ ] Integration test: [Specific scenario]

**Dependencies**:
- Requires: [What this task needs]
- Blocks: [What depends on this task]

**Estimated Complexity**: [Low/Medium/High]

**Phase Completion Criteria**:
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Code reviewed

**Phase Validation**:
- Run: `[Command to verify phase]`
- Expected: [What success looks like]
```

#### 4. Success Criteria Definition

Make criteria **SMART** (Specific, Measurable, Achievable, Relevant, Time-bound):

```markdown
### Success Criteria

#### Functional Requirements
- [ ] Feature X works as specified
- [ ] User can complete flow Y without errors

#### Non-Functional Requirements
- [ ] Response time < 200ms for typical requests
- [ ] Test coverage > 80% for new code

#### Quality Gates
- [ ] All existing tests still pass
- [ ] Linter with zero errors
- [ ] No security vulnerabilities in scan
```

#### 5. Rollback Strategy

```markdown
### Rollback Strategy

#### Quick Rollback (< 5 minutes)
**Steps**:
1. Revert commit: `git revert [commit-hash]`
2. Deploy previous version
3. Verify health check

**Data Impact**: [None | Requires DB rollback]

#### Safe Rollback (< 30 minutes)
**Steps**:
1. Feature flag disable
2. Database migration rollback
3. Clean up resources
4. Monitoring

**Points of No Return**:
- After: [Specific task/phase]
- Reason: [Why rollback is hard]
- Mitigation: [How to minimize risk]
```

---

## Phase 3: Validator Team Reference

### Verifier Agent (sonnet)

#### Cross-Validation Checklist

Systematically check each mapping:

**Analysis → Strategy Mapping:**
- [ ] Every critical risk has a mitigation task
- [ ] Every dependency has a corresponding task
- [ ] Every impact area is covered by a phase
- [ ] Every constraint is respected in the approach

**Spot-Check Protocol:**
1. Pick 3-5 specific claims from Analysis or Plan
2. Use Grep/Read to verify against actual codebase
3. Report verification results with evidence

---

### Critic Agent (opus)

#### Critical Evaluation Mindset

**Principles**:
- **Assume nothing**: Challenge stated assumptions
- **Question everything**: Why this approach over alternatives?
- **Think adversarially**: What could go wrong?
- **Check scope**: Is the plan right-sized?

**Challenge Areas:**
1. **Architectural decisions**: Were alternatives truly considered?
2. **Complexity**: Is this the simplest viable approach?
3. **Assumptions**: What's being taken for granted?
4. **Scope**: Does the plan exceed what was asked?
5. **Sequence**: Is the phase ordering optimal?

---

### Quality Reviewer Agent (sonnet)

#### Risk Scoring Methodology

Rate each dimension on a 1-5 scale:

**Technical Feasibility** (Can we build this?)
- 1 = Trivial, well-understood
- 3 = Moderate complexity, some research needed
- 5 = Extremely complex, requires breakthroughs

**Complexity** (How hard is this?)
- 1 = Single file, simple logic
- 3 = Multiple components, moderate logic
- 5 = Architectural changes, very complex logic

**Dependencies** (What do we rely on?)
- 1 = Self-contained
- 3 = Multiple internal dependencies
- 5 = Many external dependencies, version conflicts

**Time Estimate** (How long will this take?)
- 1 = < 2 hours, well-estimated
- 3 = 1-2 days, moderate uncertainty
- 5 = > 5 days, high uncertainty

**Reversibility** (Can we undo this?)
- 1 = Fully reversible, simple rollback
- 3 = Reversible but requires coordination
- 5 = Irreversible or extremely costly

**Overall Risk Calculation**:
- Average 1-2 = Low Risk
- Average 2-3 = Medium Risk
- Average 3-4 = High Risk
- Average 4-5 = Critical Risk

#### Completeness Checklist

- [ ] Testing strategy adequate
- [ ] Error handling considered
- [ ] Performance implications addressed
- [ ] Security considerations included
- [ ] Documentation plan clear
- [ ] Monitoring/observability covered
- [ ] Rollback strategy viable
- [ ] Success criteria measurable

---

### Validation Decision Guide

After synthesizing all 3 validator outputs:

**✅ APPROVED**
- Zero critical issues
- Zero major concerns (or minor-only)
- All 3 validators have no blocking feedback
- Risk level is acceptable

**🔄 NEEDS REVISION**
- Major concerns present but plan is salvageable
- Specific feedback provided for targeted improvement
- Identify exactly which agent(s) need to re-run

**❌ REJECTED**
- Critical issues found
- Fundamental flaws in approach
- Must go back to analysis or planning

---

## Common Patterns & Tips

### When to Iterate

**Iterate if:**
- Any validator finds critical or major issues
- Assumptions in analysis were wrong
- User provides new information

**Don't iterate if:**
- Only minor suggestions remain
- All 3 validators agree on approval
- Validator Team has approved

### Handling Ambiguity

If user request is unclear:
1. **Analyst agent**: Flag ambiguities in "Open Questions"
2. **Orchestrator**: Use AskUserQuestion tool immediately (before planning)
3. **Don't guess**: Better to clarify than to plan wrong thing

### Managing Scope Creep

- **Explorer**: Focus only on what's relevant to user request
- **Planner**: Use YAGNI - don't plan for hypothetical features
- **Critic**: Call out scope creep explicitly

### Token Efficiency

If running low on tokens:
- Use symbol communication from token efficiency mode
- Reference previous sections by ID instead of repeating
- Focus on critical information only
- Skip minor suggestions in validation

### Quality Signals

**Good planning shows:**
- Specific file paths and line numbers
- Concrete examples
- Measured success criteria
- Realistic risk assessment
- Clear decision rationale

**Poor planning shows:**
- Vague descriptions
- Unverified assumptions
- Missing error handling
- Unrealistic estimates
- No rollback plan

---

## Agent Handoff Protocols

### Analyzer Team → Planner Handoff (Synthesis)

```markdown
## Synthesized Analysis Report

**Analysis Summary**: [2-3 sentences combining all 3 agents' key findings]

**Key Findings from Each Agent**:
- **Explorer**: [Top 3 findings]
- **Analyst**: [Top 3 findings]
- **Risk Assessor**: [Top 3 findings]

**Planning Guidance**:
- **Recommended Approach**: [Based on all findings]
- **Avoid**: [Known pitfalls from risk assessment]
- **Constraints**: [Hard limits from analyst]

**Open Questions for User**: [If any, from analyst]
```

### Planner → Validator Team Handoff

```markdown
## Strategy Handoff to Validators

**Strategy Summary**: [2-3 sentences]

**Validation Priorities**:
- **Verifier**: Check risk/dependency coverage against Analysis
- **Critic**: Challenge decisions [1], [2], [3] specifically
- **Quality Reviewer**: Focus on feasibility of Phase [X] (highest risk)
```

### Validator Team → Iteration Handoff (Synthesis)

```markdown
## Consolidated Validation Feedback

**Decision**: [NEEDS REVISION / REJECTED]

**From Verifier**: [Key gaps found]
**From Critic**: [Key challenges raised]
**From Quality Reviewer**: [Key feasibility concerns]

**Required Actions**:
1. [Action] - Re-run: [specific agent]
2. [Action] - Re-run: [specific agent]

**Keep from Previous**:
[Parts that don't need to change]
```

---

## Troubleshooting

### "Explorer can't find relevant code"
**Solution**: Use more specific search terms or explore broader areas first

### "Planner creates too many phases"
**Solution**: Combine related work - aim for 3-5 phases maximum

### "Validator Team keeps rejecting"
**Solution**: Check if critic is being too strict - some risk is acceptable. After 2 iterations, pause and ask user.

### "Parallel agents produce conflicting findings"
**Solution**: This is expected. The synthesis step should resolve conflicts by cross-referencing. If conflict is fundamental, flag it for user input.

### "Iteration loop not converging"
**Solution**: Re-run only the specific failing agent, not the full team. After 3 iterations, ask user for guidance.

---

This reference should be consulted by each agent during their phase to ensure comprehensive, consistent, high-quality planning.
