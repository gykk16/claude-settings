# Software Engineering Reference

Detailed principles and guidelines for senior software engineering.

---

## Engineering Principles

### 1. YAGNI (You Aren't Gonna Need It)

Don't build features until they're actually needed.

```
✗ Don't create abstractions for single implementations
✗ Don't add configurability "just in case"
✗ Don't build for hypothetical future requirements

✓ Build what's needed now
✓ Refactor when patterns emerge
✓ Add flexibility when there's a real need
```

**Example:**
```kotlin
// Bad: Over-engineered for hypothetical needs
interface NotificationStrategy { ... }
class EmailNotificationStrategy : NotificationStrategy { ... }
class NotificationStrategyFactory { ... }

// Good: Simple solution for current need
class EmailNotificationService {
    fun send(to: String, message: String) { ... }
}
```

### 2. DRY (Don't Repeat Yourself) - Pragmatically

Duplicate code 2-3 times before abstracting.

```
✗ Don't abstract after first duplication
✗ Don't create wrong abstractions prematurely
✗ Don't force unrelated code into shared abstractions

✓ Duplicate 2-3 times first
✓ Extract when patterns are clear
✓ Accept that wrong abstraction is worse than duplication
```

**The Rule of Three:**
1. First time: Just write it
2. Second time: Note the duplication
3. Third time: Consider abstracting

### 3. KISS (Keep It Simple, Stupid)

Prefer simple solutions over clever ones.

```
✗ Don't use complex patterns when simple code works
✗ Don't optimize prematurely
✗ Don't add layers without clear benefit

✓ Optimize for readability first
✓ Add complexity only when necessary
✓ Prefer explicit over implicit
```

**Simplicity Checklist:**
- Can a junior developer understand this?
- Is there a simpler way to achieve the same result?
- Am I solving a real problem or a hypothetical one?

### 4. Single Responsibility Principle

Each class/function should do one thing well.

```
✗ Don't mix multiple concerns in one class
✗ Don't create "god" objects that do everything
✗ Don't name classes vaguely (Manager, Handler, Processor)

✓ One reason to change per class
✓ Clear, specific naming
✓ Split when responsibilities diverge
```

**Naming Test:**
If you can't name it clearly and specifically, it probably does too much.

---

## Code Quality Checklist

### Before Writing Code

- [ ] Understand the requirements clearly
- [ ] Read existing related code
- [ ] Identify potential impact areas
- [ ] Plan the approach

### While Writing Code

- [ ] Follow language/framework conventions
- [ ] Write self-documenting code
- [ ] Keep functions/methods small (< 20 lines ideal)
- [ ] Use meaningful names
- [ ] Handle errors appropriately

### Before Committing

- [ ] **Readable** - Code is self-explanatory
- [ ] **Tested** - Critical paths have tests
- [ ] **Secure** - No obvious vulnerabilities
- [ ] **Performant** - No obvious bottlenecks
- [ ] **Documented** - Complex logic explained (why, not what)
- [ ] **Consistent** - Follows project conventions

### Code Review Readiness

- [ ] Self-reviewed the code
- [ ] Ran all tests locally
- [ ] Checked for debugging code/comments
- [ ] Verified no sensitive data exposed

---

## When to Seek Help

As a senior engineer, know when to:

| Situation | Action |
|-----------|--------|
| Unclear requirements | Ask questions before coding |
| Unfamiliar domain | Research or consult domain experts |
| Multiple valid approaches | Propose alternatives with trade-offs |
| Technical debt concerns | Push back with data |
| Unrealistic timelines | Escalate with estimates |
| Architectural concerns | Raise in design discussions |
| Blockers | Escalate early, not late |

### Asking Good Questions

1. **Be specific** - "How should X handle Y?" not "How does this work?"
2. **Show your work** - "I tried A and B, but..."
3. **Provide context** - Why you need to know
4. **Suggest options** - "Should we do A or B?"

---

## Communication Style

### Technical Communication

| Do | Don't |
|----|-------|
| Be direct and concise | Be vague or verbose |
| Explain trade-offs | Only present one option |
| Provide context | Assume others know the background |
| Use concrete examples | Speak in abstractions only |
| Admit uncertainty | Pretend to know everything |

### Code Review Comments

**Good comments:**
- "Consider using X for better performance because..."
- "This might fail when Y happens. How about..."
- "Nice approach! One suggestion: ..."

**Bad comments:**
- "This is wrong" (no explanation)
- "Why?" (too vague)
- "I would do it differently" (no alternative given)

### Mentoring Through Code

1. **Show, don't just tell** - Provide code examples
2. **Explain the why** - Not just the what
3. **Be constructive** - Focus on improvement, not criticism
4. **Acknowledge good work** - Positive feedback matters

---

## Anti-Patterns to Avoid

### Over-Engineering

```
Symptoms:
- Abstractions with single implementations
- Configurable everything
- "Future-proof" architecture for unknown futures

Cure:
- Build for today's needs
- Refactor when patterns emerge
- Delete unused code
```

### Premature Optimization

```
Symptoms:
- Optimizing before measuring
- Complex caching without load testing
- Micro-optimizations in non-critical paths

Cure:
- Measure first, optimize second
- Focus on algorithmic complexity
- Profile before optimizing
```

### Copy-Paste Programming

```
Symptoms:
- Duplicated code blocks
- Similar bugs in multiple places
- Inconsistent implementations

Cure:
- Extract common patterns (after 2-3 duplications)
- Create shared utilities
- Use templates/generics appropriately
```

### God Objects

```
Symptoms:
- Classes with many responsibilities
- Vague names (Manager, Handler, Utils)
- Files with thousands of lines

Cure:
- Single responsibility per class
- Specific, descriptive names
- Split by domain/concern
```

---

## Summary

| Principle | Key Point |
|-----------|-----------|
| YAGNI | Build what's needed now |
| DRY | Duplicate 2-3 times before abstracting |
| KISS | Simple > Clever |
| SRP | One reason to change |
| Communication | Direct, concrete, constructive |
| Quality | Readable, tested, secure, consistent |
