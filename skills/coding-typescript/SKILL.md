---
name: coding-typescript
description: Guides TypeScript development following Google TypeScript Style Guide. Enforces best practices for types, naming, formatting, and error handling. Use when writing or reviewing TypeScript code.
---

# TypeScript Coding

$ARGUMENTS

For advanced usage, see [reference.md](reference.md)

## Core Principles

1. **Type Safety** - Use `unknown` over `any`, leverage type inference
2. **Named Exports** - Never use default exports
3. **Explicit Style** - Always use braces, semicolons, single quotes
4. **Clean Code** - Descriptive names, no abbreviations

| Do | Don't |
|----|-------|
| Write readable code | Write clever code |
| Use TypeScript idioms | Fight the language |
| Keep it simple | Over-engineer |
| Abstract when needed | Abstract preemptively |
| Name things clearly | Use abbreviations |

> **Remember**: Code is read more often than written. Optimize for readability.

## Quick Reference

### MUST Use

| Pattern | Example |
|---------|---------|
| `const`/`let` | `const name = 'John';` |
| `unknown` | `function parse(input: unknown)` |
| Named exports | `export {UserService};` |
| `===`/`!==` | `if (value === 'active')` |
| Braces always | `if (x) { return y; }` |
| Single quotes | `const s = 'text';` |
| Semicolons | `const x = 1;` |
| `as Type` | `value as User` |

### MUST NOT Use

| Avoid | Use Instead |
|-------|-------------|
| `var` | `const`/`let` |
| `any` | `unknown` or specific type |
| Default exports | Named exports |
| `==`/`!=` | `===`/`!==` (except `== null`) |
| `#private` | TypeScript `private` |
| `<Type>` assertion | `as Type` |
| Throw primitives | `throw new Error()` |

## Key Rules

### Naming

```typescript
// Classes, Interfaces, Types: UpperCamelCase
class UserService { }
interface HttpClient { }

// Variables, Functions: lowerCamelCase
const userName = 'John';
function calculateTotal() { }

// Constants, Enum values: CONSTANT_CASE
const MAX_COUNT = 100;
enum Status { ACTIVE, INACTIVE }

// Acronyms as words
loadHttpUrl()  // NOT loadHTTPURL
class XmlParser { }  // NOT XMLParser
```

### Types

```typescript
// Use interface for objects
interface User {
  id: string;
  name: string;
  email?: string;  // Optional, not `| undefined`
}

// Use type for unions/intersections
type Status = 'active' | 'inactive';
type UserWithOrders = User & { orders: Order[] };

// Use unknown, not any
function parse(input: unknown): Result { }

// Mark readonly when not reassigned
interface Config {
  readonly apiUrl: string;
}
```

### Functions & Classes

```typescript
// Parameter properties
class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly cache: CacheService,
  ) { }
}

// Default parameters
function createUser(name: string, role = Role.USER) { }

// Arrow functions for callbacks
const active = users.filter(u => u.isActive);
```

### Error Handling

```typescript
// Always throw Error instances
throw new Error('Something failed');
throw new NotFoundError(`User ${id} not found`);

// Custom errors
class AppError extends Error {
  constructor(message: string, public readonly code: string) {
    super(message);
    this.name = 'AppError';
  }
}
```

