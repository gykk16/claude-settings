# Service Layer

Services are Spring-managed beans responsible for orchestrating business logic, coordinating between repositories and external services, and managing transactions.

## Service Structure

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val emailService: EmailService,
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    fun createUser(request: CreateUserRequest): UserDto {
        // Business logic here
    }
}
```

## Business Logic Organization

Keep services focused with single responsibility:

```kotlin
@Service
class OrderService(
    private val orderRepository: OrderRepository,
    private val inventoryService: InventoryService,
) {
    fun placeOrder(request: PlaceOrderRequest): OrderDto {
        validateOrder(request)
        val order = createOrder(request)
        inventoryService.reserveItems(order.items)
        return orderRepository.save(order).toDto()
    }

    private fun validateOrder(request: PlaceOrderRequest) {
        require(request.items.isNotEmpty()) { "Order must contain items" }
        require(request.items.all { it.quantity > 0 }) { "Quantity must be positive" }
    }

    private fun createOrder(request: PlaceOrderRequest): Order {
        return Order(
            customerId = request.customerId,
            items = request.items,
            totalPrice = calculateTotal(request),
        )
    }

    private fun calculateTotal(request: PlaceOrderRequest): BigDecimal {
        return request.items.sumOf { it.price * it.quantity.toBigDecimal() }
    }
}
```

## Domain vs Application Services

**Domain Service** - Pure business logic, no framework dependencies:

```kotlin
class PricingDomainService {
    fun calculateDiscount(amount: BigDecimal, customerTier: String): BigDecimal {
        return when (customerTier) {
            "PREMIUM" -> amount * BigDecimal("0.90")
            "STANDARD" -> amount * BigDecimal("0.95")
            else -> amount
        }
    }
}
```

**Application Service** - Orchestrates repositories, transactions, external services:

```kotlin
@Service
class OrderApplicationService(
    private val orderRepository: OrderRepository,
    private val pricingDomainService: PricingDomainService,
    private val paymentGateway: PaymentGateway,
) {
    @Transactional
    fun processOrder(request: OrderRequest): OrderDto {
        val order = orderRepository.findById(request.orderId)
            ?: throw OrderNotFoundException(request.orderId)
        val discountedPrice = pricingDomainService.calculateDiscount(order.amount, order.customerTier)
        paymentGateway.charge(discountedPrice)
        return orderRepository.save(order).toDto()
    }
}
```

## Error Handling in Services

Use domain exceptions for business failures:

```kotlin
open class BusinessException(message: String) : RuntimeException(message)
class OrderNotFoundException(id: Long) : BusinessException("Order not found: $id")
class InsufficientInventoryException(sku: String) : BusinessException("Insufficient stock for $sku")

@Service
class OrderService(private val orderRepository: OrderRepository) {

    fun getOrder(orderId: Long): OrderDto =
        orderRepository.findById(orderId)?.toDto()
            ?: throw OrderNotFoundException(orderId)

    fun cancelOrder(orderId: Long) {
        val order = orderRepository.findById(orderId)
            ?: throw OrderNotFoundException(orderId)
        require(!order.isShipped) { "Cannot cancel shipped orders" }
        orderRepository.save(order.copy(status = OrderStatus.CANCELLED))
    }
}
```

## Service Composition

Chain services cleanly without circular dependencies:

```kotlin
@Service
class CheckoutService(
    private val cartService: CartService,
    private val paymentService: PaymentService,
    private val orderService: OrderService,
    private val notificationService: NotificationService,
) {
    @Transactional
    fun checkout(cartId: Long): OrderDto {
        val cart = cartService.getCart(cartId)
        val payment = paymentService.processPayment(cart.total)
        val order = orderService.createOrder(cart, payment)
        notificationService.sendConfirmation(order.customerId)
        return order.toDto()
    }
}
```

## Logging Best Practices

```kotlin
@Service
class UserService(private val userRepository: UserRepository) {

    private val logger = LoggerFactory.getLogger(javaClass)

    fun createUser(request: CreateUserRequest): UserDto {
        logger.info("Creating user with email: {}", request.email)

        return try {
            val user = userRepository.save(User.from(request))
            logger.info("User created successfully: {}", user.id)
            user.toDto()
        } catch (e: DataIntegrityViolationException) {
            logger.warn("Failed to create user - duplicate email: {}", request.email)
            throw DuplicateEmailException(request.email)
        }
    }
}
```

**Log levels:**
- `INFO`: Normal operations
- `WARN`: Recoverable issues
- `ERROR`: Failures requiring attention

## Testing Services

Mock dependencies and focus on business logic:

```kotlin
@ExtendWith(MockitoExtension::class)
class OrderServiceTest {

    @Mock
    private lateinit var orderRepository: OrderRepository

    @Mock
    private lateinit var inventoryService: InventoryService

    @InjectMocks
    private lateinit var orderService: OrderService

    @Test
    fun `should place order successfully`() {
        val request = PlaceOrderRequest(
            customerId = 1,
            items = listOf(OrderItem(sku = "SKU1", quantity = 2)),
        )
        val savedOrder = Order(id = 1, customerId = 1, items = request.items)

        whenever(inventoryService.reserveItems(any())).thenReturn(true)
        whenever(orderRepository.save(any())).thenReturn(savedOrder)

        val result = orderService.placeOrder(request)

        assertEquals(1, result.id)
        verify(inventoryService).reserveItems(request.items)
        verify(orderRepository).save(any())
    }

    @Test
    fun `should throw exception when order is empty`() {
        val request = PlaceOrderRequest(customerId = 1, items = emptyList())

        assertThrows<IllegalArgumentException> {
            orderService.placeOrder(request)
        }
    }
}
```
