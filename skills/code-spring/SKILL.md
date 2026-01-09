---
name: code-spring
description: Guides Spring Boot development following Spring official conventions. Enforces best practices for layered architecture, dependency injection, REST API design, and exception handling. Use when writing or reviewing Spring Boot code.
---

# Spring Boot Coding

$ARGUMENTS

For advanced usage, see [reference/reference.md](reference/reference.md)

## Core Principles

> **Core Philosophy**: Follow Spring conventions. Use constructor injection. Keep layers clean.

1. **Constructor Injection** - Immutable dependencies, testable code
2. **Layered Architecture** - Controller → Service → Repository
3. **Single Responsibility** - One reason to change per class
4. **Convention over Configuration** - Use sensible defaults
5. **Fail Fast** - Validate early, fail with clear messages

| Do | Don't |
|----|-------|
| Use constructor injection | Use field injection |
| Keep controllers thin | Put business logic in controllers |
| Use `@ConfigurationProperties` | Scatter `@Value` everywhere |
| Handle exceptions globally | Catch exceptions in every method |
| Return proper HTTP status codes | Return 200 for everything |

> **Remember**: Spring Boot is opinionated for a reason. Follow conventions.

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

### REST Controller

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
        userService.createUser(request)
            .let { ResponseEntity.status(HttpStatus.CREATED).body(UserResponse.from(it)) }
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

### Catching Generic Exceptions

```kotlin
// Bad: swallows all errors
fun processPayment(payment: Payment): Result {
    return try {
        paymentGateway.process(payment)
    } catch (e: Exception) {
        Result.failure("Payment failed")
    }
}

// Good: handle specific exceptions
fun processPayment(payment: Payment): Result {
    return try {
        paymentGateway.process(payment)
    } catch (e: InsufficientFundsException) {
        Result.failure("Insufficient funds")
    } catch (e: PaymentGatewayException) {
        logger.error("Gateway error", e)
        throw PaymentProcessingException("Payment processing failed", e)
    }
}
```
