# Java Style & Best Practices Reference

A comprehensive guide for writing clean, readable, and maintainable Java code.

> **Core Philosophy**: Simple is best. Write code that humans can understand. Don't over-engineer.

---

## Quick Navigation

### Core Topics

📖 **[Core Topics](core-topics.md)** - Comprehensive guide covering all essential Java best practices:
- Naming Conventions (packages, classes, methods, variables, constants)
- Code Organization (class layout, grouping members, records, sealed classes)
- Formatting (indentation, braces, method signatures, line wrapping)
- Clean Code (self-documenting code, small methods, avoiding nesting)
- Modern Features (records, sealed classes, pattern matching, text blocks, streams)
- Immutability (immutable collections, using final, immutable objects)
- Error Handling (Optional, exceptions, try-with-resources, custom exceptions)
- Testing (test names, AAA pattern, builders, parameterized tests)
- Anti-Patterns (common mistakes and how to avoid them)

### Java Version Guides

| Version | Status | Key Features | Link |
|---------|--------|--------------|------|
| **Java 8** | Extended support ended | Lambdas, Streams, Optional, Date/Time API | [java-8.md](java-8.md) |
| **Java 11** | LTS (until 2026) | var in lambdas, String methods, HTTP Client, Collection.toArray | [java-11.md](java-11.md) |
| **Java 17** | LTS (until 2029) | Sealed classes, Records, Pattern matching, Text blocks | [java-17.md](java-17.md) |
| **Java 21** | LTS (until 2031) | Pattern matching for switch, Virtual threads, Sequenced collections | [java-21.md](java-21.md) |
| **Java 25** | LTS (until 2033) | Module imports, Instance main, Scoped values, Structured concurrency | [java-25.md](java-25.md) |

---

## Getting Started

### For New Projects
1. **Use Java 21 or 25** (Latest LTS versions with modern features)
2. Read **[Core Topics](core-topics.md)** for best practices
3. Review version-specific guide ([java-21.md](java-21.md) or [java-25.md](java-25.md))
4. Follow Modern Features and Clean Code sections

### For Existing Projects
1. Check your Java version
2. Review version-specific guide for migration tips
3. Start with Anti-Patterns section in **[Core Topics](core-topics.md)** to identify issues
4. Gradually adopt modern features

### For Code Reviews
1. Check **Naming Conventions** - Consistency
2. Verify **Code Organization** - Structure
3. Assess **Clean Code** - Readability
4. Validate **Testing** - Quality

   All guidelines available in **[Core Topics](core-topics.md)**

---

## Quick Reference

### Essential Rules

| Rule | Example |
|------|---------|
| Use `Optional` for absence | `Optional<User> findUser(Long id)` |
| Prefer immutability | `private final List<User> users` |
| Use records for DTOs | `record UserDto(Long id, String name)` |
| Early returns over nesting | `if (invalid) return;` |
| Self-documenting names | `calculateTotalWithTax()` not `calc()` |

### Modern Java Checklist

- [ ] Use records for simple data carriers
- [ ] Use sealed classes for closed type hierarchies
- [ ] Pattern matching for instanceof/switch
- [ ] Text blocks for multiline strings
- [ ] Optional instead of null returns
- [ ] Streams for collection operations
- [ ] var for obvious types
- [ ] Immutable collections (List.of, Set.of, Map.of)

---

## Choosing the Right Java Version

### Java 8 (Legacy)
- ✅ Lambdas, Streams, Optional
- ✅ Date/Time API
- ❌ No records, sealed classes, pattern matching
- ⚠️ Extended support ended - migrate to Java 11+

### Java 11 (Stable LTS)
- ✅ All Java 8 features
- ✅ var, String enhancements, HTTP Client
- ✅ Supported until 2026
- ❌ No records, sealed classes
- 👍 Good for conservative migration

### Java 17 (Modern LTS)
- ✅ All Java 11 features
- ✅ Records, sealed classes, pattern matching
- ✅ Text blocks, switch expressions
- ✅ Supported until 2029
- 👍 Stable and mature

### Java 21 (Latest Stable LTS)
- ✅ All Java 17 features
- ✅ Pattern matching for switch (finalized)
- ✅ Virtual threads, sequenced collections
- ✅ Supported until 2031
- 👍 **Recommended for most new projects**

### Java 25 (Newest LTS)
- ✅ All Java 21 features
- ✅ Module imports, instance main methods
- ✅ Scoped values, structured concurrency
- ✅ Compact object headers (memory optimization)
- ✅ Supported until 2033
- 👍 Best for cutting-edge projects
- ⚠️ Some features still in preview (primitive patterns)

---

## Language Feature Summary

| Feature | Java 8 | Java 11 | Java 17 | Java 21 | Java 25 |
|---------|--------|---------|---------|---------|---------|
| Lambdas & Streams | ✅ | ✅ | ✅ | ✅ | ✅ |
| Optional | ✅ | ✅ | ✅ | ✅ | ✅ |
| var | ❌ | ✅ | ✅ | ✅ | ✅ |
| Records | ❌ | ❌ | ✅ | ✅ | ✅ |
| Sealed Classes | ❌ | ❌ | ✅ | ✅ | ✅ |
| Pattern Matching (instanceof) | ❌ | ❌ | ✅ | ✅ | ✅ |
| Pattern Matching (switch) | ❌ | ❌ | ❌ | ✅ | ✅ |
| Text Blocks | ❌ | ❌ | ✅ | ✅ | ✅ |
| Switch Expressions | ❌ | ❌ | ✅ | ✅ | ✅ |
| Virtual Threads | ❌ | ❌ | ❌ | ✅ | ✅ |
| Sequenced Collections | ❌ | ❌ | ❌ | ✅ | ✅ |
| Module Imports | ❌ | ❌ | ❌ | ❌ | ✅ |
| Instance Main Methods | ❌ | ❌ | ❌ | ❌ | ✅ |
| Scoped Values | ❌ | ❌ | ❌ | ❌ | ✅ |
| Structured Concurrency | ❌ | ❌ | ❌ | ❌ | ✅ |
| Primitive Patterns | ❌ | ❌ | ❌ | ❌ | 🔄 (Preview) |

---

## Migration Paths

### Java 8 → Java 11
1. Replace deprecated APIs (Integer constructor → valueOf)
2. Use new String methods (isBlank, lines, strip)
3. Adopt HTTP Client for new code
4. Use var for obvious types
5. See [java-11.md](java-11.md) for details

### Java 11 → Java 17
1. Convert data classes to records
2. Use sealed classes for closed hierarchies
3. Adopt pattern matching for instanceof
4. Use text blocks for multiline strings
5. See [java-17.md](java-17.md) for details

### Java 17 → Java 21
1. Use pattern matching for switch
2. Adopt virtual threads for I/O operations
3. Use sequenced collections API
4. Explore record patterns
5. See [java-21.md](java-21.md) for details

### Java 21 → Java 25
1. Replace ThreadLocal with Scoped Values
2. Use Structured Concurrency for parallel tasks
3. Adopt instance main methods for scripts
4. Use flexible constructor bodies for validation
5. Benefit from compact object headers (automatic)
6. See [java-25.md](java-25.md) for details

---

## Resources

### Official Documentation
- [Java Language Specification](https://docs.oracle.com/javase/specs/)
- [Java API Documentation](https://docs.oracle.com/en/java/javase/)
- [Effective Java (Book)](https://www.oreilly.com/library/view/effective-java/9780134686097/)

### Style Guides
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Oracle Java Code Conventions](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)

### Tools
- [Checkstyle](https://checkstyle.org/) - Code style checker
- [PMD](https://pmd.github.io/) - Source code analyzer
- [SpotBugs](https://spotbugs.github.io/) - Bug detector
- [SonarQube](https://www.sonarqube.org/) - Code quality platform

---

## Summary

### Do's ✅
- Write readable, self-documenting code
- Use modern Java features appropriately
- Keep classes and methods focused (SRP)
- Prefer immutability
- Use Optional for absence
- Write comprehensive tests

### Don'ts ❌
- Over-engineer simple solutions
- Return null (use Optional)
- Create god classes
- Use magic numbers
- Ignore compiler warnings
- Skip proper error handling

> **Remember**: Code is read more often than written. Optimize for readability and maintainability.
