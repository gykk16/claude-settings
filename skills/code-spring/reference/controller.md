# Controller Layer

REST controllers handle HTTP requests, validate input, delegate to services, and return responses.

## When to Use

| Scenario | Controller | Service |
|----------|------------|---------|
| HTTP request/response handling | ✅ | ❌ |
| Input validation annotations | ✅ | ❌ |
| Status code selection | ✅ | ❌ |
| Business rules/logic | ❌ | ✅ |
| Multi-step operations | ❌ | ✅ |
| Transaction management | ❌ | ✅ |

## Key Principles

> **Keep controllers thin.** 7-10 lines max. Delegate business logic to services.

| Guideline | Description |
|-----------|-------------|
| **Max 7-10 lines** | Controller methods should be concise |
| **No business logic** | Delegate to service layer |
| **Simple cases OK** | Trivial logic (e.g., simple mapping) can stay |
| **Single responsibility** | One action per endpoint |

## Decision: Controller vs Service Logic

**Keep in Controller:**
- Simple null checks returning 404
- Direct mapping to response
- Trivial transformations (exists check, toDto)

**Move to Service:**
- Multiple conditions or validations
- State changes with business rules
- Operations involving multiple entities

## REST API Design

### HTTP Methods

| Method | Purpose | Idempotent | Response Code |
|--------|---------|------------|---------------|
| `GET` | Read resource(s) | Yes | 200 OK |
| `POST` | Create resource | No | 201 Created |
| `PUT` | Replace resource | Yes | 200 OK |
| `PATCH` | Partial update | Yes | 200 OK |
| `DELETE` | Remove resource | Yes | 204 No Content |

### URL Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| Collection | `/api/v1/users` | List/create resources |
| Item | `/api/v1/users/{id}` | Single resource CRUD |
| Sub-resource | `/api/v1/users/{id}/orders` | Related resources |
| Search | `/api/v1/users/search?name=kim` | Complex queries |

**Avoid:** Verbs in URL (`/createUser`, `/getUserById`)

## Controller Structure

```kotlin
@RestController
@RequestMapping("/api/v1/users")
class UserController(private val userService: UserService) {

    @GetMapping("/{id}")
    fun getUser(@PathVariable id: Long): ResponseEntity<UserDto> =
        userService.findById(id)
            ?.let { ResponseEntity.ok(it) }
            ?: ResponseEntity.notFound().build()

    @PostMapping
    fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserDto> =
        ResponseEntity.status(HttpStatus.CREATED).body(userService.create(request))

    @DeleteMapping("/{id}")
    fun deleteUser(@PathVariable id: Long): ResponseEntity<Void> {
        userService.delete(id)
        return ResponseEntity.noContent().build()
    }
}
```

## Validation

| Annotation | Use Case |
|------------|----------|
| `@NotBlank` | Required string fields |
| `@Email` | Email format validation |
| `@Size(min, max)` | Length constraints |
| `@Min`, `@Max` | Numeric bounds |
| `@Pattern` | Regex validation |

```kotlin
data class CreateUserRequest(
    @field:NotBlank val name: String,
    @field:Email val email: String,
    @field:Size(min = 8) val password: String,
)
```

## Response Status Codes

| Status | Use Case |
|--------|----------|
| `200 OK` | Successful GET, PUT, PATCH |
| `201 Created` | Successful POST |
| `204 No Content` | Successful DELETE |
| `400 Bad Request` | Invalid input |
| `404 Not Found` | Resource not found |
| `409 Conflict` | Resource already exists |

## Exception Handling

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleNotFound(ex: ResourceNotFoundException): ResponseEntity<ErrorResponse> =
        ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(message = ex.message ?: "Resource not found"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors.associate { it.field to it.defaultMessage }
        return ResponseEntity.badRequest().body(ErrorResponse("Validation failed", errors))
    }
}
```

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Business logic in controller | Hard to test, violates SRP | Move to service layer |
| Missing `@Valid` | Validation not triggered | Always use with `@RequestBody` |
| Returning entity directly | Exposes internal structure | Use DTOs |
| Inconsistent error responses | Poor API experience | Use `@RestControllerAdvice` |
| No API versioning | Breaking changes affect clients | Use URL versioning `/api/v1/` |
