---
name: code-java
description: Guides Java development following modern Java best practices. Enforces clean code, SOLID principles, effective type safety, and idiomatic patterns. Use when writing or reviewing Java code.
---

# Java Coding

$ARGUMENTS

For advanced usage, see [reference.md](reference/reference.md)

## Core Principles

> **Core Philosophy**: Simple is best. Write code that humans can understand. Don't over-engineer.

1. **Type Safety** - Leverage Java's type system, use Optional, avoid null returns
2. **Immutability** - Prefer final, immutable collections, defensive copies
3. **Java Idioms** - Records, sealed classes, streams, functional interfaces
4. **Clean Code** - Self-documenting, small focused methods

| Do | Don't |
|----|-------|
| Write readable code | Write clever code |
| Use Java idioms | Fight the language |
| Keep it simple | Over-engineer |
| Abstract when needed | Abstract preemptively |
| Name things clearly | Use abbreviations |

> **Remember**: Code is read more often than written. Optimize for readability.

## Quick Reference

### Naming Conventions

| Type | Style | Example |
|------|-------|---------|
| Packages | lowercase | `com.example.project` |
| Classes, Interfaces | UpperCamelCase | `UserRepository` |
| Methods, Variables | lowerCamelCase | `processOrder`, `userName` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Type parameters | Single capital letter | `T`, `E`, `K`, `V` |

### Acronyms

```java
// Two letters: both uppercase
class IOStream { }

// Longer: capitalize first letter only
class XmlParser { }
class HttpClient { }
```

## Key Patterns

### Optional Instead of Null

```java
// Return Optional for potentially absent values
public Optional<User> findUser(Long id) {
    return userRepository.findById(id);
}

// Use Optional methods
user.ifPresent(this::processUser);
String name = user.map(User::getName).orElse("Unknown");
User found = findUser(id).orElseThrow(() -> new UserNotFoundException(id));
```

### Records (Java 16+)

```java
public record User(
    Long id,
    String name,
    String email
) {
    // Compact constructor for validation
    public User {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be blank");
        }
    }

    // Additional methods
    public boolean hasEmail() {
        return email != null && !email.isBlank();
    }
}
```

### Sealed Classes (Java 17+)

```java
public sealed interface Result<T> permits Success, Error, Loading {
}

public record Success<T>(T data) implements Result<T> { }
public record Error(String message) implements Result<Nothing> { }
public record Loading() implements Result<Nothing> { }

public void handle(Result<User> result) {
    switch (result) {
        case Success<User> s -> showUser(s.data());
        case Error e -> showError(e.message());
        case Loading l -> showLoading();
    }
}
```

### Streams and Functional Style

```java
// Filter and map
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .toList();

// Reduce
int totalAge = users.stream()
    .mapToInt(User::getAge)
    .sum();

// Group by
Map<String, List<User>> byRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole));
```

### Immutability

```java
// Use final for parameters and locals
public void processUser(final User user) {
    final String name = user.getName();
}

// Immutable collections
List<String> names = List.of("Alice", "Bob", "Charlie");
Set<Integer> numbers = Set.of(1, 2, 3);
Map<String, Integer> scores = Map.of("Alice", 100, "Bob", 95);

// Defensive copies
public class Users {
    private final List<User> users;

    public Users(List<User> users) {
        this.users = List.copyOf(users);  // Defensive copy
    }

    public List<User> getUsers() {
        return users;  // Already immutable
    }
}
```

## Class Layout Order

```java
public class UserService {
    // 1. Constants
    private static final int CACHE_SIZE = 100;

    // 2. Static variables
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    // 3. Instance variables
    private final UserRepository userRepository;
    private final Map<Long, User> cache;

    // 4. Constructors
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
        this.cache = new HashMap<>();
    }

    // 5. Public methods
    public Optional<User> findUser(Long id) { }

    // 6. Package-private methods
    void clearCache() { }

    // 7. Protected methods
    protected void validateUser(User user) { }

    // 8. Private methods
    private void updateCache(User user) { }

    // 9. Static nested classes
    private static class CacheEntry {
        private final User user;
        private final Instant timestamp;
    }
}
```

## Anti-Patterns to Avoid

### Over-Engineering

```java
// Bad: unnecessary abstraction
interface StringProcessor { String process(String s); }
class UpperCaseProcessor implements StringProcessor { ... }
class ProcessorFactory { StringProcessor create() { ... } }

// Good: simple and direct
String toUpperCase(String s) {
    return s.toUpperCase();
}
```

### Deep Nesting

```java
// Bad: nested conditionals
public void processUser(User user) {
    if (user != null) {
        if (user.isActive()) {
            if (user.hasPermission("admin")) {
                // logic here
            }
        }
    }
}

// Good: early returns
public void processUser(User user) {
    if (user == null) return;
    if (!user.isActive()) return;
    if (!user.hasPermission("admin")) return;
    // logic here
}
```

### Null Checking

```java
// Bad: returning null
public User findUser(Long id) {
    return userRepository.findById(id);  // Can be null
}

// Good: Optional
public Optional<User> findUser(Long id) {
    return userRepository.findById(id);
}

// Or: throw exception for required values
public User getUserOrThrow(Long id) {
    return findUser(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}
```

## Error Handling

```java
// Use Optional for expected absence
public Optional<User> findUser(Long id) {
    return userRepository.findById(id);
}

// Use exceptions for exceptional conditions
public User createUser(String name, String email) {
    if (name == null || name.isBlank()) {
        throw new IllegalArgumentException("Name cannot be blank");
    }
    return userRepository.save(new User(name, email));
}

// Custom exceptions
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("User not found: " + id);
    }
}

// Try-with-resources for auto-closeable
try (var reader = new BufferedReader(new FileReader(path))) {
    return reader.lines().toList();
} catch (IOException e) {
    throw new UncheckedIOException("Failed to read file", e);
}
```

## Modern Java Features

### Pattern Matching (Java 21+)

```java
// Pattern matching for instanceof
if (obj instanceof String s) {
    return s.toUpperCase();
}

// Pattern matching for switch
return switch (obj) {
    case String s -> s.toUpperCase();
    case Integer i -> i.toString();
    case null -> "null";
    default -> obj.toString();
};

// Record patterns
record Point(int x, int y) { }

if (obj instanceof Point(int x, int y)) {
    System.out.println("x: " + x + ", y: " + y);
}
```

### Text Blocks (Java 15+)

```java
String json = """
    {
        "name": "John",
        "email": "john@example.com"
    }
    """;

String sql = """
    SELECT id, name, email
    FROM users
    WHERE active = true
    ORDER BY name
    """;
```

## Best Practices Summary

1. **Use `final` liberally** - Parameters, local variables, fields when possible
2. **Prefer immutability** - Use immutable collections, records, defensive copies
3. **Return Optional** - Instead of null for potentially absent values
4. **Use streams wisely** - For transformations, not as a replacement for loops
5. **Keep methods small** - Single responsibility, 10-20 lines ideal
6. **Avoid premature optimization** - Write clear code first, optimize when needed
7. **Leverage modern features** - Records, sealed classes, pattern matching, text blocks
8. **Write self-documenting code** - Clear names over comments
9. **Fail fast** - Validate input early, throw exceptions for invalid state
10. **Use standard library** - Don't reinvent Collections, Streams, Optional
