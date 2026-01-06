# TypeScript Style Guide Reference

Strictly follows [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html).

---

## Source Organization

### File Structure Order

```typescript
// 1. @fileoverview JSDoc (if applicable)

// 2. Imports
import {Injectable} from '@angular/core';
import type {User} from './types';

// 3. Implementation
export class UserService { }
```

### Imports

**Use named exports exclusively. Do NOT use default exports.**

```typescript
// GOOD
export {UserService};
export class UserService { }

// BAD - never use default exports
export default UserService;
```

**Use `import type` for type-only imports:**

```typescript
// GOOD
import type {User, Order} from './types';
import {UserService} from './services';

// BAD
import {User, Order} from './types';  // When only used as types
```

**Import styles:**

```typescript
// Use namespace imports for large APIs
import * as fs from 'fs';

// Use destructured imports for frequently used items
import {map, filter} from 'lodash';

// Use relative imports within projects
import {User} from './models';  // Not absolute paths
```

---

## Naming Conventions

### Casing Rules

| Type | Style | Example |
|------|-------|---------|
| Classes, Interfaces, Types, Enums, Decorators, Type Parameters | `UpperCamelCase` | `UserService`, `HttpClient` |
| Variables, Parameters, Functions, Methods, Properties | `lowerCamelCase` | `userName`, `calculateTotal()` |
| Global constants, Enum values | `CONSTANT_CASE` | `MAX_COUNT`, `Status.ACTIVE` |

### Identifiers

```typescript
// Use descriptive names - avoid abbreviations
// GOOD
function calculateTotalPrice() { }
const userRepository = new UserRepository();

// BAD
function calcTotPr() { }
const usrRepo = new UserRepository();
```

### Acronyms - Treat as Words

```typescript
// GOOD
function loadHttpUrl() { }
class XmlParser { }
const htmlContent = '';

// BAD
function loadHTTPURL() { }
class XMLParser { }
const HTMLContent = '';
```

### Avoid

```typescript
// DO NOT use underscores or prefixes
let _privateVar;        // BAD
let opt_value;          // BAD
interface IUserService  // BAD - no 'I' prefix

// GOOD
private privateVar;
let value;
interface UserService
```

---

## Formatting

### Indentation and Encoding

- Use **spaces**, not tabs
- UTF-8 encoding

### Braces

**ALWAYS use braces for control structures, even for single statements:**

```typescript
// GOOD
if (isValid) {
  return result;
}

// BAD
if (isValid) return result;
```

### Horizontal Whitespace

```typescript
// Spaces around binary operators
const sum = a + b;

// NO space around range operator
for (let i = 0; i < 10; i++) { }

// Space after keywords
if (condition) { }
for (const item of items) { }
while (running) { }

// NO space before opening parenthesis in declarations
function process() { }
class User { }
```

### Strings

**Use single quotes for ordinary strings:**

```typescript
// GOOD
const name = 'John';

// BAD
const name = "John";
```

**Use template literals for:**
- String interpolation
- Multi-line strings

```typescript
const greeting = `Hello, ${name}!`;
const query = `
  SELECT *
  FROM users
  WHERE active = true
`;
```

### Semicolons

**ALWAYS use explicit semicolons. Do NOT rely on ASI.**

```typescript
const value = 42;
function process() { }
```

### Trailing Commas

**Use trailing commas for multi-line:**

```typescript
const user = {
  name: 'John',
  email: 'john@example.com',
  age: 30,
};

const items = [
  'apple',
  'banana',
  'orange',
];
```

---

## Type System

### Type Inference

**Rely on inference for trivially inferred types:**

```typescript
// GOOD - let TypeScript infer
const name = 'John';
const count = 42;
const items = ['a', 'b', 'c'];

// GOOD - annotate when not obvious
function processUser(user: User): ProcessedUser { }
const config: AppConfig = loadConfig();
```

### Use `unknown` Instead of `any`

**Never use `any`. Use `unknown` for truly opaque values.**

```typescript
// BAD
function parse(input: any): any { }

// GOOD
function parse(input: unknown): Result {
  if (typeof input === 'string') {
    return parseString(input);
  }
  throw new Error('Invalid input');
}
```

### Interfaces vs Type Aliases

**Prefer interfaces for object definitions:**

```typescript
// GOOD - use interface for object shapes
interface User {
  id: string;
  name: string;
  email: string;
}

// Use type aliases for unions, intersections, primitives
type UserId = string;
type Status = 'active' | 'inactive' | 'pending';
type UserWithOrders = User & {orders: Order[]};
```

### Array Types

```typescript
// Use T[] for simple types
const names: string[] = [];
const users: User[] = [];

// Use Array<T> for complex types
const handlers: Array<(event: Event) => void> = [];
```

### Nullability

**Use optional fields, NOT `|undefined`:**

```typescript
// GOOD
interface User {
  name: string;
  nickname?: string;
}

// BAD
interface User {
  nickname: string | undefined;
}
```

**Handle null/undefined near their source:**

```typescript
function processUser(user: User | null) {
  if (!user) {
    return null;
  }
  return transform(user);
}
```

### Readonly

**Mark non-reassigned properties as `readonly`:**

```typescript
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

class UserService {
  private readonly repository: UserRepository;
}
```

### Do NOT Use `{}`

```typescript
// BAD
let value: {};

// GOOD - use specific types
let value: unknown;
let value: Record<string, unknown>;
let value: object;
```

---

## Functions

### Function Declarations vs Arrow Functions

```typescript
// Use function declarations for named functions
function processOrder(order: Order): ProcessedOrder { }

// Use arrow functions for callbacks
const activeUsers = users.filter(user => user.isActive);

// Use arrow functions in nested contexts
class UserService {
  private handleClick = () => {
    this.process();
  };
}
```

### Parameters

**Use default parameter initializers:**

```typescript
function createUser(name: string, role: Role = Role.USER): User { }
```

**Use rest parameters instead of `arguments`:**

```typescript
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### Return Types

```typescript
// Annotate complex return types
function parseConfig(input: string): AppConfig { }

// Let inference work for simple returns
const double = (n: number) => n * 2;
```

---

## Classes

### Structure Order

```typescript
class UserService {
  // 1. Static properties
  private static readonly instance: UserService;

  // 2. Instance properties
  private readonly repository: UserRepository;
  private cache: Map<string, User>;

  // 3. Constructor
  constructor(repository: UserRepository) {
    this.repository = repository;
    this.cache = new Map();
  }

  // 4. Public methods
  async findUser(id: string): Promise<User | null> { }

  // 5. Private methods
  private validateId(id: string): void { }
}
```

### Parameter Properties

**Use parameter properties to reduce boilerplate:**

```typescript
// GOOD
class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly emailService: EmailService,
  ) { }
}

// Verbose alternative - avoid
class UserService {
  private readonly repository: UserRepository;
  private readonly emailService: EmailService;

  constructor(repository: UserRepository, emailService: EmailService) {
    this.repository = repository;
    this.emailService = emailService;
  }
}
```

### Visibility

**Use TypeScript's `private`, NOT `#private` fields:**

```typescript
// GOOD
class Service {
  private secret: string;
}

// BAD - do not use #private
class Service {
  #secret: string;
}
```

**Do NOT access properties via `obj['property']` to bypass visibility.**

### Static Members

**Do NOT use classes as namespaces for static members:**

```typescript
// BAD - container class
class Utils {
  static formatDate() { }
  static parseDate() { }
}

// GOOD - export functions directly
export function formatDate() { }
export function parseDate() { }
```

---

## Control Structures

### Equality

**ALWAYS use `===` and `!==`.**

**Exception: Use `== null` to check both null and undefined:**

```typescript
// GOOD
if (value === 'active') { }
if (count !== 0) { }

// GOOD - exception for null check
if (value == null) {
  return defaultValue;
}

// BAD
if (value == 'active') { }
```

### Loops

**Prefer `for...of` for iterations:**

```typescript
// GOOD
for (const item of items) { }

// Use for...in only for dict-style objects with hasOwnProperty
for (const key in obj) {
  if (Object.prototype.hasOwnProperty.call(obj, key)) { }
}
```

### Switch Statements

**All switch statements MUST have a default case:**

```typescript
switch (status) {
  case 'active':
    return process();
  case 'inactive':
    return skip();
  default:
    throw new Error(`Unknown status: ${status}`);
}
```

---

## Error Handling

### Throw Only Error Instances

**Never throw primitives or arbitrary objects:**

```typescript
// BAD
throw 'Something went wrong';
throw 404;
throw {message: 'error'};

// GOOD
throw new Error('Something went wrong');
throw new NotFoundError(`User ${id} not found`);
```

### Custom Errors

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}
```

### Catch Blocks

```typescript
// Assume caught values are Error types
try {
  await process();
} catch (e) {
  if (e instanceof SpecificError) {
    handle(e);
  }
  throw e;
}

// Non-empty catch blocks MUST have explanation
try {
  await process();
} catch {
  // Expected to fail during initialization, will retry
}
```

---

## Disallowed Patterns

### NEVER Use

| Pattern | Replacement |
|---------|-------------|
| `var` | `const` / `let` |
| `any` | `unknown` or specific types |
| Default exports | Named exports |
| `#private` fields | TypeScript `private` |
| `new String()` / `new Boolean()` / `new Number()` | Primitive types |
| `Array()` constructor | `[]` literal |
| `Object()` constructor | `{}` literal |
| `const enum` | `enum` |
| `eval()` | Never |
| `Function(string)` constructor | Never |
| `with` statement | Never |

### Type Assertions

**Use `as Type` syntax, NOT angle brackets:**

```typescript
// GOOD
const user = value as User;

// BAD
const user = <User>value;
```

**Prefer runtime checks over assertions:**

```typescript
// GOOD
if (value instanceof User) {
  return value.name;
}

// Use assertions only when necessary, with explanation
const user = value as User;  // Safe: validated by schema above
```

---

## Testing

### Descriptive Names

```typescript
describe('UserService', () => {
  describe('findUser', () => {
    it('should return null when user does not exist', () => { });
    it('should throw error when id is invalid', () => { });
  });
});
```

### Arrange-Act-Assert

```typescript
it('should calculate correct total with discount', () => {
  // Arrange
  const order: Order = {
    items: [{price: 100, quantity: 2}],
    discountPercent: 10,
  };

  // Act
  const total = calculator.calculateTotal(order);

  // Assert
  expect(total).toBe(180);
});
```

---

## Summary

| MUST | MUST NOT |
|------|----------|
| Use `const`/`let` | Use `var` |
| Use `unknown` | Use `any` |
| Use named exports | Use default exports |
| Use `===`/`!==` | Use `==`/`!=` (except null check) |
| Use braces for control structures | Omit braces |
| Use single quotes | Use double quotes |
| Use explicit semicolons | Rely on ASI |
| Use TypeScript `private` | Use `#private` |
| Throw `Error` instances | Throw primitives |
| Use `as Type` assertions | Use `<Type>` assertions |
