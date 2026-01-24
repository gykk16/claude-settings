# Service Layer

Services orchestrate business logic, coordinate repositories and external services, and manage transactions.

## When to Use

| Scenario | Service | Controller |
|----------|---------|------------|
| Business logic/rules | ✅ | ❌ |
| Transaction boundaries | ✅ | ❌ |
| Multi-repository operations | ✅ | ❌ |
| External service calls | ✅ | ❌ |
| HTTP request/response | ❌ | ✅ |
| Input validation annotations | ❌ | ✅ |

## Key Principles

> **Keep services focused.** Single responsibility. Thin controllers, rich services.

| Guideline | Description |
|-----------|-------------|
| **Single responsibility** | One service per domain concept |
| **Business logic here** | Validation, rules, calculations |
| **Coordinate, don't duplicate** | Orchestrate other services |
| **Transaction per operation** | One @Transactional per use case |

## Service Types

| Type | Characteristics | Dependencies |
|------|-----------------|--------------|
| **Domain Service** | Pure business logic, no Spring annotations | None (POJO) |
| **Application Service** | Orchestration, transactions, external calls | Repositories, other services |

```kotlin
// Domain Service - Pure business logic
class PricingDomainService {
    fun calculateDiscount(amount: BigDecimal, tier: String): BigDecimal =
        when (tier) {
            "PREMIUM" -> amount * BigDecimal("0.90")
            "STANDARD" -> amount * BigDecimal("0.95")
            else -> amount
        }
}

// Application Service - Orchestration
@Service
class OrderApplicationService(
    private val orderRepository: OrderRepository,
    private val pricingService: PricingDomainService,
    private val paymentGateway: PaymentGateway,
) {
    @Transactional
    fun processOrder(orderId: Long): OrderDto {
        val order = orderRepository.findById(orderId)
            ?: throw OrderNotFoundException(orderId)
        val discountedPrice = pricingService.calculateDiscount(order.amount, order.customerTier)
        paymentGateway.charge(discountedPrice)
        return orderRepository.save(order).toDto()
    }
}
```

## Error Handling

Use domain exceptions for business rule violations:

```kotlin
open class BusinessException(message: String) : RuntimeException(message)
class OrderNotFoundException(id: Long) : BusinessException("Order not found: $id")
class InsufficientInventoryException(sku: String) : BusinessException("Insufficient stock: $sku")

@Service
class OrderService(private val orderRepository: OrderRepository) {

    fun getOrder(id: Long): OrderDto =
        orderRepository.findById(id)?.toDto()
            ?: throw OrderNotFoundException(id)

    fun cancelOrder(id: Long) {
        val order = orderRepository.findById(id) ?: throw OrderNotFoundException(id)
        require(!order.isShipped) { "Cannot cancel shipped orders" }
        orderRepository.save(order.copy(status = OrderStatus.CANCELLED))
    }
}
```

## Service Composition

Chain services without circular dependencies:

```kotlin
@Service
class CheckoutService(
    private val cartService: CartService,
    private val paymentService: PaymentService,
    private val orderService: OrderService,
) {
    @Transactional
    fun checkout(cartId: Long): OrderDto {
        val cart = cartService.getCart(cartId)
        val payment = paymentService.processPayment(cart.total)
        return orderService.createOrder(cart, payment).toDto()
    }
}
```

## Logging Guidelines

| Level | Use Case |
|-------|----------|
| `INFO` | Normal operations (user created, order placed) |
| `WARN` | Recoverable issues (duplicate email, validation failure) |
| `ERROR` | Failures requiring attention (payment failed, DB error) |

```kotlin
@Service
class UserService(private val userRepository: UserRepository) {
    private val logger = LoggerFactory.getLogger(javaClass)

    fun createUser(request: CreateUserRequest): UserDto {
        logger.info("Creating user: {}", request.email)
        return try {
            userRepository.save(User.from(request)).also {
                logger.info("User created: {}", it.id)
            }.toDto()
        } catch (e: DataIntegrityViolationException) {
            logger.warn("Duplicate email: {}", request.email)
            throw DuplicateEmailException(request.email)
        }
    }
}
```

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Circular dependencies | Application startup failure | Extract shared logic, use events |
| Business logic in controller | Hard to test, violates SRP | Move all business logic to service |
| Transaction too large | Lock contention, connection exhaustion | Keep transactions small and focused |
| External calls in transaction | Connection held during I/O | Move external calls outside transaction |
| Missing null checks | NullPointerException | Use Kotlin nullable types, throw domain exceptions |

## Testing

```kotlin
@ExtendWith(MockitoExtension::class)
class OrderServiceTest {

    @Mock lateinit var orderRepository: OrderRepository
    @InjectMocks lateinit var orderService: OrderService

    @Test
    fun `should throw when order not found`() {
        whenever(orderRepository.findById(any())).thenReturn(null)

        assertThrows<OrderNotFoundException> {
            orderService.getOrder(999L)
        }
    }
}
```
