---
name: coding-kotlin
description: Guides Kotlin development following Kotlin Coding Conventions. Enforces best practices for null safety, idioms, clean code, and pragmatic OOP. Use when writing or reviewing Kotlin code.
---

# Kotlin Coding

$ARGUMENTS

For advanced usage, see [reference.md](reference.md)

## Core Principles

> **Core Philosophy**: Simple is best. Write code that humans can understand. Don't over-engineer.

1. **Null Safety** - Leverage Kotlin's type system, use `?.` and `?:`
2. **Immutability** - Prefer `val` over `var`, immutable collections
3. **Kotlin Idioms** - Data classes, sealed classes, extension functions
4. **Clean Code** - Self-documenting, small focused functions

| Do | Don't |
|----|-------|
| Write readable code | Write clever code |
| Use Kotlin idioms | Fight the language |
| Keep it simple | Over-engineer |
| Abstract when needed | Abstract preemptively |
| Name things clearly | Use abbreviations |

> **Remember**: Code is read more often than written. Optimize for readability.

## Quick Reference

### Naming Conventions

| Type | Style | Example |
|------|-------|---------|
| Packages | lowercase | `org.example.project` |
| Classes, Interfaces | UpperCamelCase | `UserRepository` |
| Functions, Variables | lowerCamelCase | `processOrder`, `userName` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Backing properties | underscore prefix | `_items` |

### Acronyms

```kotlin
// Two letters: both uppercase
class IOStream

// Longer: capitalize first letter only
class XmlParser
class HttpClient
```

## Key Patterns

### Null Safety

```kotlin
val length = name?.length ?: 0
user?.let { saveToDatabase(it) }
requireNotNull(user) { "User cannot be null" }
```

### Data Classes

```kotlin
data class User(
    val id: Long,
    val name: String,
    val email: String,
)

val updated = user.copy(name = "New Name")
```

### Sealed Classes

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}

fun handle(result: Result<User>) = when (result) {
    is Result.Success -> showUser(result.data)
    is Result.Error -> showError(result.message)
    is Result.Loading -> showLoading()
}
```

### Scope Functions

```kotlin
// let: null checks
val result = nullableValue?.let { transform(it) }

// apply: object configuration
val user = User().apply {
    name = "John"
    email = "john@example.com"
}

// also: side effects
return user.also { logger.info("Created: ${it.id}") }
```

### Extension Functions

```kotlin
fun String.toSlug() = lowercase().replace(" ", "-")

fun User.isEligibleForDiscount() =
    accountAge > Duration.ofDays(365) && totalPurchases > 1000
```

## Class Layout Order

```kotlin
class UserService(
    private val userRepository: UserRepository,  // 1. Constructor properties
) {
    // 2. Properties & initializer blocks
    private val cache = mutableMapOf<Long, User>()

    // 3. Secondary constructors
    constructor() : this(DefaultUserRepository())

    // 4. Public methods
    fun findUser(id: Long): User? { }

    // 5. Internal/Protected methods
    internal fun clearCache() { }

    // 6. Private methods
    private fun validateUser(user: User) { }

    // 7. Companion object
    companion object {
        private const val CACHE_SIZE = 100
    }

    // 8. Nested/Inner classes
    data class CacheEntry(val user: User, val timestamp: Long)
}
```

## Anti-Patterns to Avoid

### Over-Engineering

```kotlin
// Bad
interface StringProcessor { fun process(s: String): String }
class UpperCaseProcessor : StringProcessor { ... }
class ProcessorFactory { fun create(): StringProcessor = ... }

// Good
fun toUpperCase(s: String) = s.uppercase()
```

### Deep Nesting

```kotlin
// Bad
fun processUser(user: User?) {
    if (user != null) {
        if (user.isActive) {
            if (user.hasPermission("admin")) {
                // logic here
            }
        }
    }
}

// Good: early returns
fun processUser(user: User?) {
    if (user == null) return
    if (!user.isActive) return
    if (!user.hasPermission("admin")) return
    // logic here
}
```

## Error Handling

```kotlin
// Nullable for expected absence
fun findUser(id: Long): User? = userRepository.findById(id)

// Exceptions for unexpected errors
fun findUserOrThrow(id: Long): User =
    userRepository.findById(id) ?: throw UserNotFoundException(id)

// Result pattern for expected failures
sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Failure(val error: AppError) : Result<Nothing>()
}
```
