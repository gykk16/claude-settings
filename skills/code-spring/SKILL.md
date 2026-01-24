---
name: code-spring
description: Guides Spring Boot development following Spring official conventions. Enforces best practices for layered architecture, dependency injection, REST API design, and exception handling. Use when writing or reviewing Spring Boot code.
---

# Spring Boot Coding

$ARGUMENTS

Spring Boot 개발 시 Spring 공식 컨벤션을 따르도록 안내합니다.

## References

For detailed information, see:
- [reference/reference.md](reference/reference.md)

## Instructions

1. **Spring 컨벤션 준수** - Spring Boot의 기본 규칙을 따른다
2. **생성자 주입 사용** - 필드 주입 대신 생성자 주입으로 의존성 관리
3. **계층 분리 유지** - Controller → Service → Repository 구조 준수
4. **전역 예외 처리** - `@RestControllerAdvice`로 일관된 에러 응답
5. **적절한 HTTP 상태 코드** - 200 OK, 201 Created, 204 No Content 등 구분

## Examples

**Input:**
```
UserService 클래스 작성해줘
```

**Output:**
```kotlin
@Service
@Transactional(readOnly = true)
class UserService(
    private val userRepository: UserRepository,
) {
    fun findById(id: Long): User? =
        userRepository.findById(id).orElse(null)

    @Transactional
    fun create(request: CreateUserRequest): User =
        userRepository.save(request.toEntity())
}
```

**Input:**
```
REST API 엔드포인트 만들어줘
```

**Output:**
```kotlin
@RestController
@RequestMapping("/api/v1/users")
class UserController(
    private val userService: UserService,
) {
    @GetMapping("/{id}")
    fun getUser(@PathVariable id: Long): ResponseEntity<UserResponse> =
        userService.findById(id)
            ?.let { ResponseEntity.ok(UserResponse.from(it)) }
            ?: ResponseEntity.notFound().build()

    @PostMapping
    fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserResponse> =
        ResponseEntity.status(HttpStatus.CREATED)
            .body(UserResponse.from(userService.create(request)))
}
```

## Core Principles

> **Core Philosophy**: Follow Spring conventions. Use constructor injection. Keep layers clean.

| Do | Don't |
|----|-------|
| Use constructor injection | Use field injection |
| Keep controllers thin | Put business logic in controllers |
| Use `@ConfigurationProperties` | Scatter `@Value` everywhere |
| Handle exceptions globally | Catch exceptions in every method |
| Return proper HTTP status codes | Return 200 for everything |

## Quick Reference

### Naming Conventions

| Type | Style | Example |
|------|-------|---------|
| Packages | lowercase, feature-based | `com.example.user` |
| Controllers | `*Controller` | `UserController` |
| Services | `*Service` | `UserService` |
| Repositories | `*Repository` | `UserRepository` |
| Configuration | `*Config` / `*Properties` | `SecurityConfig`, `AppProperties` |

### Spring Stereotypes

| Annotation | Purpose | Layer |
|------------|---------|-------|
| `@RestController` | REST API endpoints | Presentation |
| `@Service` | Business logic | Business |
| `@Repository` | Data access | Persistence |
| `@Component` | Generic bean | Any |
| `@Configuration` | Bean definitions | Infrastructure |

## Key Patterns

### Constructor Injection

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val emailService: EmailService,
) {
    fun createUser(request: CreateUserRequest): User {
        val user = userRepository.save(request.toEntity())
        emailService.sendWelcome(user.email)
        return user
    }
}
```

### Exception Handling

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException::class)
    fun handleNotFound(ex: EntityNotFoundException): ResponseEntity<ErrorResponse> =
        ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(ex.message ?: "Resource not found"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> =
        ResponseEntity.badRequest()
            .body(ErrorResponse(ex.bindingResult.fieldErrors.map { it.defaultMessage }.joinToString()))
}

data class ErrorResponse(val message: String)
```

### Configuration Properties

```kotlin
@ConfigurationProperties(prefix = "app")
data class AppProperties(
    val name: String,
    val maxRetries: Int = 3,
    val api: ApiProperties = ApiProperties(),
) {
    data class ApiProperties(
        val baseUrl: String = "https://api.example.com",
        val timeout: Duration = Duration.ofSeconds(30),
    )
}

@Configuration
@EnableConfigurationProperties(AppProperties::class)
class AppConfig
```

## Class Layout Order

```kotlin
@Service
class OrderService(
    private val orderRepository: OrderRepository,  // 1. Dependencies
) {
    // 2. Properties
    private val logger = LoggerFactory.getLogger(javaClass)

    // 3. Public methods (API)
    fun createOrder(request: CreateOrderRequest): Order { }

    fun findOrder(id: Long): Order? { }

    // 4. Internal methods
    internal fun validateOrder(order: Order) { }

    // 5. Private methods
    private fun calculateTotal(items: List<OrderItem>): BigDecimal { }

    // 6. Companion object
    companion object {
        private const val MAX_ITEMS = 100
    }
}
```

## Anti-Patterns to Avoid

### Field Injection

```kotlin
// Bad: hidden dependencies, hard to test
@Service
class UserService {
    @Autowired
    private lateinit var userRepository: UserRepository
}

// Good: explicit, immutable, testable
@Service
class UserService(
    private val userRepository: UserRepository,
)
```

### Fat Controller

```kotlin
// Bad: business logic in controller
@RestController
class OrderController(private val orderRepository: OrderRepository) {
    @PostMapping
    fun createOrder(@RequestBody request: CreateOrderRequest): Order {
        val order = Order(items = request.items)
        order.total = request.items.sumOf { it.price * it.quantity }
        if (order.total > 1000) order.discount = order.total * 0.1
        return orderRepository.save(order)
    }
}

// Good: delegate to service
@RestController
class OrderController(private val orderService: OrderService) {
    @PostMapping
    fun createOrder(@RequestBody request: CreateOrderRequest): Order =
        orderService.createOrder(request)
}
```
