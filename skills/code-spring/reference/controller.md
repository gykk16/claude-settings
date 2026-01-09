# Controller Layer

REST controllers handle HTTP requests, validate input, delegate to services, and return responses.

## Controller Principles

> **Keep controllers thin.** Methods should be 7-10 lines max. Delegate business logic to services.

| Guideline | Description |
|-----------|-------------|
| **Max 7-10 lines** | Controller methods should be concise |
| **No business logic** | Delegate to service layer |
| **Simple cases OK** | Trivial logic (e.g., simple mapping) can stay in controller |
| **Single responsibility** | One action per endpoint |

### When Business Logic in Controller is Acceptable

```kotlin
// OK: Trivial transformation, no business rules
@GetMapping("/{id}/exists")
fun checkExists(@PathVariable id: Long): ResponseEntity<Boolean> =
    ResponseEntity.ok(userService.existsById(id))

// OK: Simple conditional response
@GetMapping("/{id}")
fun getUser(@PathVariable id: Long): ResponseEntity<UserDto> =
    userService.findById(id)
        ?.let { ResponseEntity.ok(it) }
        ?: ResponseEntity.notFound().build()
```

### When to Move Logic to Service

```kotlin
// Bad: Business logic in controller
@PostMapping("/{id}/activate")
fun activateUser(@PathVariable id: Long): ResponseEntity<UserDto> {
    val user = userService.findById(id) ?: return ResponseEntity.notFound().build()
    if (user.status == Status.SUSPENDED) {
        throw BusinessException("Suspended users cannot be activated")
    }
    if (user.emailVerified == false) {
        throw BusinessException("Email must be verified first")
    }
    val activated = user.copy(status = Status.ACTIVE, activatedAt = Instant.now())
    return ResponseEntity.ok(userService.save(activated).toDto())
}

// Good: Delegate to service
@PostMapping("/{id}/activate")
fun activateUser(@PathVariable id: Long): ResponseEntity<UserDto> =
    ResponseEntity.ok(userService.activate(id))
```

## REST API Design Principles

Follow RESTful conventions for predictable, intuitive APIs.

### Resource Naming

| Pattern | Example | Description |
|---------|---------|-------------|
| Collection | `/users` | Plural nouns for collections |
| Item | `/users/{id}` | Singular resource by ID |
| Sub-resource | `/users/{id}/orders` | Nested resources |
| Action (avoid) | `/users/{id}/activate` | Use sparingly, prefer state change via PUT |

### HTTP Methods

| Method | Purpose | Idempotent | Request Body |
|--------|---------|------------|--------------|
| `GET` | Read resource(s) | Yes | No |
| `POST` | Create resource | No | Yes |
| `PUT` | Replace resource | Yes | Yes |
| `PATCH` | Partial update | Yes | Yes |
| `DELETE` | Remove resource | Yes | No |

### URL Design

```kotlin
// Good: Resource-oriented
GET    /api/v1/users           // List users
GET    /api/v1/users/{id}      // Get user
POST   /api/v1/users           // Create user
PUT    /api/v1/users/{id}      // Replace user
PATCH  /api/v1/users/{id}      // Update user
DELETE /api/v1/users/{id}      // Delete user

// Good: Sub-resources
GET    /api/v1/users/{id}/orders        // User's orders
POST   /api/v1/users/{id}/orders        // Create order for user

// Avoid: Verbs in URL
POST   /api/v1/users/createUser         // Bad
POST   /api/v1/getUserById              // Bad
GET    /api/v1/users/search?name=kim    // OK for complex queries
```

### Query Parameters

```kotlin
// Filtering
GET /api/v1/users?status=active&role=admin

// Pagination
GET /api/v1/users?page=0&size=20

// Sorting
GET /api/v1/users?sort=createdAt,desc

// Combined
GET /api/v1/users?status=active&page=0&size=20&sort=name,asc
```

## REST Controller Structure

```kotlin
@RestController
@RequestMapping("/api/v1/users")
class UserController(
    private val userService: UserService,
) {
    // endpoints here
}
```

**Key annotations:**
- `@RestController`: Combines @Controller + @ResponseBody
- `@RequestMapping`: Base path for all endpoints
- Constructor injection for dependencies

## Request Mapping

```kotlin
@GetMapping
fun getAllUsers(): ResponseEntity<List<UserDto>> =
    ResponseEntity.ok(userService.findAll())

@GetMapping("/{id}")
fun getUserById(@PathVariable id: Long): ResponseEntity<UserDto> =
    userService.findById(id)
        ?.let { ResponseEntity.ok(it) }
        ?: ResponseEntity.notFound().build()

@PostMapping
fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserDto> =
    ResponseEntity.status(HttpStatus.CREATED).body(userService.create(request))

@PutMapping("/{id}")
fun updateUser(
    @PathVariable id: Long,
    @Valid @RequestBody request: UpdateUserRequest,
): ResponseEntity<UserDto> =
    ResponseEntity.ok(userService.update(id, request))

@DeleteMapping("/{id}")
fun deleteUser(@PathVariable id: Long): ResponseEntity<Void> {
    userService.delete(id)
    return ResponseEntity.noContent().build()
}
```

## Path Variables & Query Parameters

```kotlin
@GetMapping("/search")
fun searchUsers(
    @RequestParam name: String,
    @RequestParam(required = false, defaultValue = "0") page: Int,
    @RequestParam(required = false, defaultValue = "20") size: Int,
): ResponseEntity<Page<UserDto>> =
    ResponseEntity.ok(userService.search(name, page, size))

@GetMapping("/{userId}/posts/{postId}")
fun getUserPost(
    @PathVariable userId: Long,
    @PathVariable postId: Long,
): ResponseEntity<PostDto> =
    ResponseEntity.ok(userService.getPost(userId, postId))
```

## Request Body & Validation

```kotlin
data class CreateUserRequest(
    @field:NotBlank(message = "Name is required")
    val name: String,

    @field:Email(message = "Invalid email format")
    val email: String,

    @field:Size(min = 8, message = "Password must be at least 8 characters")
    val password: String,

    @field:Min(value = 18, message = "Age must be at least 18")
    val age: Int,
)

@PostMapping
fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserDto> =
    ResponseEntity.status(HttpStatus.CREATED).body(userService.create(request))
```

## Response Handling

**HTTP Status Codes:**

| Status | Use Case |
|--------|----------|
| `200 OK` | Successful GET, PUT, PATCH |
| `201 Created` | Successful POST |
| `204 No Content` | Successful DELETE |
| `400 Bad Request` | Invalid input |
| `401 Unauthorized` | Authentication required |
| `403 Forbidden` | Authorization failed |
| `404 Not Found` | Resource not found |
| `409 Conflict` | Resource already exists |

## DTO Pattern

```kotlin
// Request DTO
data class CreateUserRequest(
    val name: String,
    val email: String,
)

// Response DTO
data class UserDto(
    val id: Long,
    val name: String,
    val email: String,
    val createdAt: LocalDateTime,
)

// Mapping extension
fun User.toDto() = UserDto(
    id = id,
    name = name,
    email = email,
    createdAt = createdAt,
)
```

## Exception Handling

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleNotFound(ex: ResourceNotFoundException): ResponseEntity<ErrorResponse> =
        ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(message = ex.message ?: "Resource not found"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidationError(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors
            .associate { it.field to it.defaultMessage }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
            .body(ErrorResponse(message = "Validation failed", details = errors))
    }
}

data class ErrorResponse(
    val message: String,
    val details: Map<String, Any?>? = null,
    val timestamp: LocalDateTime = LocalDateTime.now(),
)
```

## API Versioning

**URL-based versioning** (recommended):

```kotlin
@RestController
@RequestMapping("/api/v1/users")
class UserControllerV1(private val userService: UserService)

@RestController
@RequestMapping("/api/v2/users")
class UserControllerV2(private val userService: UserService)
```

**Best practice:** Use URL versioning for clarity and caching.
