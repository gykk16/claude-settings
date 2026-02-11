# Deep Dive Planning Examples

Real-world scenarios demonstrating the team-based parallel planning workflow.

---

## Example 1: Adding JWT Authentication System

### User Request

> "I want to add JWT-based authentication to our Express API. Users should be able to register, login, and access protected routes."

### Workflow Execution

#### Step 1: Initialize

```markdown
**User Request**: Add JWT authentication with register, login, and protected routes
**Scope**: project
**Estimated Complexity**: High
```

#### Step 2: Launch Analyzer Team (3 agents in parallel)

**Launched simultaneously:**

##### Explorer Agent (haiku) Output

```markdown
## Explorer Findings

### Architecture Overview
- Express 4.18.2 with TypeScript
- REST API with 15 existing endpoints
- MongoDB for data persistence
- No authentication currently - all routes are open

### Relevant Code Locations
- `src/server.ts:1-50` - Express app setup, middleware chain
- `src/routes/index.ts:10-30` - Route registration
- `src/models/User.ts` - Exists but minimal (id, email, name only)
- `src/middleware/` - Directory exists, only has `errorHandler.ts`

### Existing Patterns
- Middleware pattern already used for error handling
- Service layer pattern for business logic
- Repository pattern for database access

### Technology Stack
- **Language**: TypeScript 5.0+ (strict mode)
- **Framework**: Express 4.18.2
- **Database**: MongoDB with Mongoose
- **Build**: tsc + nodemon
```

##### Analyst Agent (opus) Output

```markdown
## Analyst Findings

### Internal Dependencies

| Component | Relationship | Impact Level |
|-----------|--------------|--------------|
| `User.ts` model | Need to add password field | High |
| All route handlers | Need to add auth middleware | High |
| `errorHandler.ts` | Need to add auth error cases | Medium |

### External Dependencies

| Package | Version | Purpose | Risk |
|---------|---------|---------|------|
| `jsonwebtoken` | ^9.0.2 | JWT creation/verification | Low - stable |
| `bcrypt` | ^5.1.1 | Password hashing | Low - standard |
| `express-validator` | ^7.0.1 | Input validation | Low - already used |

### Technical Constraints
- **TypeScript**: Strict mode enabled - need proper types for Request extension
- **Performance**: Auth check must be < 10ms
- **Security**: Must follow OWASP guidelines for password storage

### Business Constraints
- **Timeline**: User wants this completed in one session
- **Backwards Compatibility**: No active clients yet, can break existing routes
- **Scope**: No email verification for now (confirmed with user)

### Open Questions
1. Should existing routes require auth immediately? → **Confirmed: Yes**
2. Email verification needed? → **Confirmed: Not now**
```

##### Risk Assessor Agent (sonnet) Output

```markdown
## Risk Assessment Findings

### Risks Identified

#### 🚨 Critical Risks
1. **Breaking All Existing Routes**
   - **Description**: Adding auth middleware could break all existing endpoints
   - **Impact**: API becomes unusable
   - **Probability**: High if not careful
   - **Mitigation**: Phase implementation - add middleware selectively first

#### ⚠️ High Risks
1. **Password Storage Vulnerability**
   - **Description**: If bcrypt not used correctly, passwords could be compromised
   - **Impact**: Security breach
   - **Probability**: Medium
   - **Mitigation**: Use bcrypt.hash with salt rounds >= 10

2. **JWT Secret Management**
   - **Description**: Weak or exposed secret could compromise all tokens
   - **Impact**: Authentication bypass
   - **Probability**: Medium
   - **Mitigation**: Strong secret generation, environment variable only

#### 🔶 Medium Risks
1. **Token Expiry Balance** - Start with 24h, make configurable
2. **No Rate Limiting** - Note for future, not in scope now

### Impact Areas

#### Files to Modify
```
src/
├── models/User.ts (modify - add password field)
├── middleware/
│   ├── auth.middleware.ts (create)
│   └── errorHandler.ts (modify)
├── routes/
│   ├── auth.routes.ts (create)
│   └── index.ts (modify)
├── services/auth.service.ts (create)
├── types/express.d.ts (create)
└── server.ts (modify)
```

#### Test Coverage Impact
- **Unit tests**: 8 new test files needed
- **Integration tests**: 5 scenarios
- **E2E tests**: 2 full flows

### Security Implications
- Password hashing must use bcrypt with salt rounds >= 12
- JWT secret must be cryptographically strong (256-bit)
- Never log passwords or tokens
- Use HTTPS requirement documented
```

#### Step 2b: Synthesize Analysis Report

**Orchestrator combines all 3 outputs:**

```markdown
## 🔍 Analysis Report (Synthesized)

### 1. Current State
Express 4.18.2 + TypeScript API with 15 endpoints, MongoDB, no auth.
Middleware pattern exists (errorHandler). Service/repository patterns in use.

### 2. Dependencies
- **Internal**: User model (high), all routes (high), error handler (medium)
- **External**: jsonwebtoken, bcrypt, express-validator (all low risk)
- **Infrastructure**: JWT_SECRET and TOKEN_EXPIRY env vars needed

### 3. Constraints
- TypeScript strict mode, <10ms auth latency, OWASP compliance
- No active clients (can break routes), no email verification needed

### 4. Risks Identified
- 🚨 Breaking existing routes (mitigate: phased middleware)
- ⚠️ Password storage (mitigate: bcrypt 12 rounds)
- ⚠️ JWT secret management (mitigate: env var, strong generation)

### 5. Impact Areas
- 4 files to modify, 4 files to create
- 8 unit test files, 5 integration scenarios needed

### 6. Recommendations for Planner
- **Preferred**: Middleware-based JWT with Authorization header
- **Avoid**: Session-based (stateful), rolling own crypto
- **Key**: Global middleware with explicit exclusions for auth routes
```

#### Step 3: Launch Planner Agent (opus)

```markdown
## 📋 Implementation Strategy

### 1. Approach
JWT authentication using Express middleware pattern, bcrypt for passwords.
Global auth middleware protecting all routes except /auth/* endpoints.

### 2. Architectural Decisions

**Decision 1: JWT vs Sessions** → JWT (stateless, no Redis needed)
**Decision 2: bcrypt salt rounds** → 12 (OWASP, adaptive)
**Decision 3: Middleware placement** → Global with exclusions (secure by default)

### 3. Implementation Phases

#### Phase 1: Foundation (30-45 min)
- Task 1.1: Update User model (add password field + hash methods)
- Task 1.2: Install dependencies (jsonwebtoken, bcrypt + types)
- Task 1.3: Create TypeScript type extensions (Request.user)
- **Parallel**: Tasks 1.2 and 1.3 can run concurrently

#### Phase 2: Core Logic (45-60 min)
- Task 2.1: Create auth service (generateToken, verifyToken, hash, compare)
- Task 2.2: Create auth middleware (extract, verify, attach user)
- **Sequential**: 2.2 depends on 2.1

#### Phase 3: Endpoints (45-60 min)
- Task 3.1: Create register endpoint
- Task 3.2: Create login endpoint
- Task 3.3: Register auth routes
- **Parallel**: Tasks 3.1 and 3.2 can run concurrently

#### Phase 4: Protection (30-45 min)
- Task 4.1: Apply global auth middleware
- Task 4.2: Update existing route handlers

#### Phase 5: Polish (20-30 min)
- Task 5.1: Add request validation
- Task 5.2: Documentation

### 4. Timeline Estimate
Total: 2.5-4 hours across 5 phases, 12 tasks

### 5. Success Criteria
- Users can register and login
- All routes require valid JWT
- Passwords hashed with bcrypt (>= 12 rounds)
- Test coverage > 80%

### 6. Rollback Strategy
Quick: `git revert HEAD~5..HEAD`
Safe: Remove auth middleware from server.ts, comment out auth routes

### 7. Risk Mitigation Plan
| Risk | Mitigation |
|------|-----------|
| Breaking routes | Phase 4 applies middleware carefully |
| Password leak | bcrypt 12 rounds, never log passwords |
| Weak JWT secret | `openssl rand -base64 32` |
```

#### Step 4: Launch Validator Team (3 agents in parallel)

**Launched simultaneously:**

##### Verifier Agent (sonnet) Output

```markdown
## Verifier Findings

### Cross-Validation
- 🚨 Breaking routes: ✅ Addressed in Phase 4 with selective middleware
- ⚠️ Password storage: ✅ bcrypt 12 rounds in Phase 2
- ⚠️ JWT secret: ✅ Env variable in Phase 1
- 🔶 Token expiry: ✅ Configurable via env
- 🔶 Rate limiting: ✅ Acknowledged as future work

### Spot Checks
- Claim: "express-validator already used" → ✅ Verified in package.json
- Claim: "Middleware pattern exists" → ✅ errorHandler.ts confirmed

### Gaps Found
None - all analysis findings mapped to plan tasks ✓
```

##### Critic Agent (opus) Output

```markdown
## Critic Findings

### Decisions Challenged
- JWT vs Sessions: ✅ Justified - stateless API, no Redis available
- bcrypt rounds 12: ✅ OWASP recommended, good balance
- Global middleware: ✅ Secure by default is correct approach

### Logical Flaws
None identified - phase sequencing is logical ✓

### Hidden Assumptions
- Assumes MongoDB handles concurrent writes for registration (valid for current scale)
- Assumes no need for refresh tokens (user confirmed simple scope)

### Scope Assessment
Plan is right-sized ✅ - no scope creep, matches user request exactly
```

##### Quality Reviewer Agent (sonnet) Output

```markdown
## Quality Review Findings

### Risk Scoring Matrix

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Technical Feasibility | 2 | Well-understood JWT pattern |
| Complexity | 3 | Multiple components, moderate logic |
| Dependencies | 2 | Stable npm packages only |
| Time Estimate | 2 | 2.5-4 hours is reasonable |
| Reversibility | 2 | Easy rollback, minimal data impact |
| **OVERALL** | **2.2** | **Low-Medium Risk** |

### Completeness Checklist
- [x] Testing strategy adequate
- [x] Error handling considered
- [x] Performance implications addressed
- [x] Security considerations included
- [x] Rollback strategy viable
- [x] Success criteria measurable
- [ ] ⚠️ Monitoring not covered (minor - future iteration)

### Issues Found
- 🔶 Minor: Add performance benchmark in Phase 5 to verify <10ms auth latency
- 🔶 Minor: Password complexity rules not specified (suggest: min 8 chars)
```

#### Step 4b: Synthesize Validation Decision

```markdown
## ✅ Validation Report (Synthesized)

### Risk Level: Low-Medium (2.2/5)

### Cross-Validation: All risks addressed ✓ (Verifier)
### Strategic Assessment: No flaws, scope appropriate ✓ (Critic)
### Completeness: 6/7 checklist items pass ✓ (Quality Reviewer)

### Issues Found
- 🚨 Critical: None
- ⚠️ Major: None
- 🔶 Minor: Performance benchmark, password complexity rules

### Decision: ✅ APPROVED

All 3 validators agree. Plan is comprehensive, well-structured, and ready for implementation.
Minor suggestions can be addressed during implementation.
```

#### Step 5: No iteration needed (Approved on first pass)

#### Step 6: Present to User

```markdown
## Deep Dive Plan: JWT Authentication - Ready for Approval

### Overview
- **Risk Level**: Low-Medium
- **Estimated Time**: 2.5-4 hours
- **Phases**: 5 | **Tasks**: 12
- **Agents Used**: 7 (3 Analyzers + 1 Planner + 3 Validators)

### Key Decisions
1. JWT over sessions (stateless, no Redis)
2. bcrypt 12 rounds (OWASP standard)
3. Global middleware with exclusions (secure by default)

### All 3 validators approved unanimously.

Ready to proceed?
```

---

## Example 2: Refactoring Monolithic Service (with Iteration)

### User Request

> "Our OrderService has grown to 2000 lines and is becoming unmaintainable. Help me refactor it."

### Abbreviated Workflow

#### Analyzer Team (Parallel) - Key Findings

**Explorer**: 2000 lines, 45 methods, mixes 5 concerns (validation, business, DB, email, payments)

**Analyst**: Used in 23 places across codebase. Only 40% test coverage. No clear service boundaries.

**Risk Assessor**: 🚨 Breaking existing functionality during refactor. ⚠️ Low test coverage means no safety net.

#### Synthesized Analysis

```markdown
## 🔍 Analysis Report
- OrderService.ts: 2000 lines, 45 methods, 5 mixed concerns
- Used in 23 places, only 40% test coverage
- 🚨 High risk of breaking functionality
- Recommendation: Test-first refactoring with incremental extraction
```

#### Planner Output

```markdown
## 📋 Implementation Strategy

**Approach**: Extract to 5 specialized services incrementally

**Architecture**:
- OrderService (orchestration)
  ├─ ValidationService
  ├─ PaymentService
  ├─ InventoryService
  ├─ NotificationService
  └─ OrderRepository

**Phases**:
1. Add comprehensive tests to existing OrderService (safety net)
2. Extract ValidationService (lowest risk)
3. Extract PaymentService (high value)
4. Extract remaining services
5. Slim down OrderService to orchestrator
```

#### Validator Team (Parallel) - First Round

**Verifier**: All risks mapped ✓

**Critic**: Phase 1 says "add comprehensive tests" but doesn't specify coverage target or scenarios. This is critical for safety net. **MAJOR CONCERN.**

**Quality Reviewer**: Risk score 3.6/5 (High). Testing strategy in Phase 1 is inadequate.

#### Synthesized Decision: 🔄 NEEDS REVISION

```markdown
## Validation Report - Round 1

### Decision: 🔄 NEEDS REVISION

**From Critic**: Phase 1 lacks specific test scenarios - this is the safety net for everything else
**From Quality Reviewer**: Testing strategy inadequate for high-risk refactor

**Required Action**: Re-run Planner with specific test scenarios for Phase 1
- Target: 80% coverage before any refactoring
- Specify: happy path, edge cases, error handling for each major method
```

#### Planner Re-run (with Critic's feedback)

```markdown
## 📋 Revised Phase 1: Comprehensive Test Coverage

**Goal**: Achieve 80% test coverage as safety net

**Tasks**:

##### Task 1.1: Test Order Creation Flow
- Happy path: valid order successfully created
- Edge case: empty cart, invalid items, out of stock
- Error case: payment service down, database failure

##### Task 1.2: Test Order Updates
[... specific scenarios ...]

##### Task 1.3: Test Payment Processing
[... specific scenarios ...]

**Completion Criteria**:
- [ ] Coverage report shows >= 80%
- [ ] All critical paths tested
- [ ] All external service failures mocked and tested
```

#### Validator Team Re-run - Round 2

**Verifier**: Revised Phase 1 now covers all critical paths ✓

**Critic**: Test scenarios are specific and measurable. Safety net is adequate ✓

**Quality Reviewer**: Updated risk score accounts for improved test strategy ✓

#### Synthesized Decision: ✅ APPROVED (Round 2)

```markdown
## Validation Report - Round 2

### Decision: ✅ APPROVED

Phase 1 now has specific test scenarios and measurable 80% coverage target.
This provides the safety net needed for high-risk refactoring.

Note: Only the Planner was re-run. Analyzer Team results were still valid.
```

---

## Example 3: When NOT to Use Deep Dive Planning

### User Request

> "Fix the bug where user names are displaying as 'undefined' on the profile page"

### Correct Response

```markdown
This is a straightforward bug fix - deep dive planning is overkill.

I'll just:
1. Find where user names are displayed (1-2 files)
2. Check if data is being fetched correctly
3. Fix the issue
4. Test the fix

Use deep-dive-plan for:
- Complex features requiring architectural decisions
- Large refactoring efforts
- Multi-component system changes
- Unclear implementation paths
```

---

## Key Lessons

### Team-Based Advantages Demonstrated

1. **Parallel Analysis** (Example 1): 3 agents explored different aspects simultaneously, reducing analysis time by ~50%
2. **Parallel Validation** (Example 1): 3 validators caught different types of issues from different perspectives
3. **Targeted Iteration** (Example 2): Only Planner re-ran (not full Analyzer Team), saving time
4. **Specialized Agents**: Each agent brought domain expertise (Explorer for code mapping, Critic for strategy challenges)

### Success Patterns

1. **Synthesis is key**: Raw parallel outputs must be combined into coherent reports
2. **Iteration is surgical**: Re-run only the agent that failed, not the entire team
3. **Validators complement each other**: Verifier catches gaps, Critic challenges strategy, Quality Reviewer checks feasibility
4. **User clarification early**: Analyst's open questions resolved before planning begins

### When to Skip

- Simple bugs - direct fix is faster
- Well-understood patterns - follow existing implementation
- Prototypes/experiments - planning overhead not justified
