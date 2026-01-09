# Transaction Management

## Transaction Principles

> **Keep transactions small and fast.** Avoid external calls. Watch for self-invocation.

| Guideline | Description |
|-----------|-------------|
| **Keep it small** | Only include necessary DB operations |
| **No external I/O** | Avoid HTTP calls, file I/O, messaging inside transactions |
| **No self-invocation** | Same-class method calls bypass proxy |
| **Fail fast** | Validate before starting transaction |

## @Transactional Basics

Place `@Transactional` on service methods to declare transaction boundaries.

```kotlin
@Service
class UserService(private val userRepository: UserRepository) {

    @Transactional
    fun createUser(name: String): User {
        return userRepository.save(User(name = name))
    }
}
```

**Key defaults:**
- Propagation: `REQUIRED` (joins existing or creates new)
- Isolation: Database default (usually `READ_COMMITTED`)
- Rollback: Unchecked exceptions only
- Timeout: None

## Propagation Levels

**REQUIRED**: Default. Uses existing transaction or creates new.

```kotlin
@Transactional
fun save(entity: Entity) { }  // Standard case
```

**REQUIRES_NEW**: Always creates new transaction, suspends current.

```kotlin
@Transactional(propagation = Propagation.REQUIRES_NEW)
fun auditLog(message: String) {
    // Commits independently, even if parent rolls back
    logRepository.save(AuditLog(message))
}
```

**NESTED**: Creates savepoint within existing transaction.

```kotlin
@Transactional(propagation = Propagation.NESTED)
fun optionalStep() { }  // Can rollback to savepoint without losing parent
```

## Isolation Levels

**READ_COMMITTED**: Prevents dirty reads. Good default.

```kotlin
@Transactional(isolation = Isolation.READ_COMMITTED)
fun getUser(id: Long): User? = userRepository.findById(id)
```

**REPEATABLE_READ**: Prevents non-repeatable reads. Use for consistency-critical operations.

```kotlin
@Transactional(isolation = Isolation.REPEATABLE_READ)
fun transferFunds(fromId: Long, toId: Long, amount: BigDecimal) {
    val from = accountRepository.findById(fromId)
    val to = accountRepository.findById(toId)
    // Repeated reads return same values
}
```

## Read-Only Transactions

Mark queries as read-only to optimize performance.

```kotlin
@Transactional(readOnly = true)
fun getUsersByRole(role: String): List<User> =
    userRepository.findByRole(role)
```

**Benefits:**
- JDBC driver optimizations
- Database hint for query planning
- Prevention of accidental writes

## Keep Transactions Small

Long transactions hold database locks, reduce throughput, and increase deadlock risk.

```kotlin
// Bad: Transaction holds lock during slow operations
@Transactional
fun processOrder(orderId: Long) {
    val order = orderRepository.findById(orderId)
    val invoice = pdfService.generateInvoice(order)      // Slow PDF generation
    emailService.sendInvoice(order.email, invoice)       // External HTTP call
    order.status = OrderStatus.COMPLETED
    orderRepository.save(order)
}

// Good: Minimize transaction scope
fun processOrder(orderId: Long) {
    // 1. Update DB in short transaction
    val order = completeOrder(orderId)

    // 2. External calls outside transaction
    val invoice = pdfService.generateInvoice(order)
    emailService.sendInvoice(order.email, invoice)
}

@Transactional
fun completeOrder(orderId: Long): Order {
    val order = orderRepository.findById(orderId)
        ?: throw OrderNotFoundException(orderId)
    order.status = OrderStatus.COMPLETED
    return orderRepository.save(order)
}
```

## Avoid External I/O in Transactions

External calls (HTTP, file I/O, messaging) inside transactions cause:
- **Connection pool exhaustion** - DB connections held during slow external calls
- **Inconsistent state** - External call succeeds but transaction rolls back
- **Increased latency** - Lock held longer than necessary

```kotlin
// Bad: External call inside transaction
@Transactional
fun createUser(request: CreateUserRequest): User {
    val user = userRepository.save(User.from(request))
    paymentService.createCustomer(user.email)  // HTTP call to external API
    emailService.sendWelcome(user.email)       // SMTP call
    return user
}

// Good: External calls after transaction commits
fun createUser(request: CreateUserRequest): User {
    val user = saveUser(request)

    // External calls after commit - if these fail, user is still created
    paymentService.createCustomer(user.email)
    emailService.sendWelcome(user.email)
    return user
}

@Transactional
fun saveUser(request: CreateUserRequest): User =
    userRepository.save(User.from(request))
```

### Using @TransactionalEventListener

For operations that must run after commit:

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val eventPublisher: ApplicationEventPublisher,
) {
    @Transactional
    fun createUser(request: CreateUserRequest): User {
        val user = userRepository.save(User.from(request))
        eventPublisher.publishEvent(UserCreatedEvent(user))
        return user
    }
}

@Component
class UserEventHandler(
    private val emailService: EmailService,
) {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    fun handleUserCreated(event: UserCreatedEvent) {
        emailService.sendWelcome(event.user.email)  // Runs after commit
    }
}
```

## Rollback Rules

By default, only **unchecked exceptions** (RuntimeException, Error) trigger rollback.

```kotlin
@Transactional
fun processPayment(id: Long) {
    // Unchecked: rolls back
    if (!isValid) throw IllegalArgumentException()

    // Checked: doesn't rollback by default
    // throw IOException()
}
```

**Custom rollback rules:**

```kotlin
@Transactional(rollbackFor = [IOException::class, CustomException::class])
fun processFile(file: File) {
    // Now IOException triggers rollback
}

@Transactional(noRollbackFor = [ValidationException::class])
fun validate() {
    // ValidationException doesn't rollback
}
```

## Common Pitfalls

### 1. Self-invocation (Same-class method calls)

Calling `@Transactional` methods from the same class bypasses the proxy:

```kotlin
@Service
class UserService(private val userRepository: UserRepository) {

    @Transactional
    fun createUser(name: String): User {
        return userRepository.save(User(name = name))
    }

    fun register(name: String): User {
        // No transaction! Direct method call bypasses Spring proxy
        return createUser(name)
    }
}
```

**Solutions:**

**Option 1:** Make the calling method transactional (Recommended)

```kotlin
@Transactional
fun register(name: String): User {
    return createUser(name)  // Now wrapped in outer transaction
}
```

**Option 2:** Inject self to call through proxy

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
) {
    @Autowired
    private lateinit var self: UserService  // Inject self

    @Transactional
    fun createUser(name: String): User =
        userRepository.save(User(name = name))

    fun register(name: String): User {
        return self.createUser(name)  // Calls through proxy - transaction works
    }
}
```

**Option 3:** Extract to separate service

```kotlin
@Service
class UserCreationService(private val userRepository: UserRepository) {
    @Transactional
    fun createUser(name: String): User =
        userRepository.save(User(name = name))
}

@Service
class UserRegistrationService(private val userCreationService: UserCreationService) {
    fun register(name: String): User {
        return userCreationService.createUser(name)  // Different class - proxy works
    }
}
```

### 2. Non-public methods

Only `public` methods are proxied:

```kotlin
@Transactional
private fun internalSave() { }  // Ignored

@Transactional
fun publicSave() { }  // Works
```

### 3. Checked exceptions

Don't rollback by default:

```kotlin
@Transactional  // throws IOException - won't rollback!
fun loadData() { }

@Transactional(rollbackFor = [IOException::class])  // Correct
fun loadData() { }
```

## Lazy Loading & N+1 Problem

### LazyInitializationException

Accessing lazy-loaded associations outside transaction throws exception:

```kotlin
@Entity
class Order(
    @Id val id: Long,
    @OneToMany(fetch = FetchType.LAZY)
    val items: List<OrderItem> = emptyList(),
)

@Service
class OrderService(private val orderRepository: OrderRepository) {

    @Transactional(readOnly = true)
    fun getOrder(id: Long): Order? = orderRepository.findById(id)
}

// Controller - outside transaction
@GetMapping("/{id}")
fun getOrder(@PathVariable id: Long): OrderDto {
    val order = orderService.getOrder(id)
    order.items.size  // LazyInitializationException!
}
```

**Solutions:**

**Option 1:** Fetch eagerly in query (Recommended)

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {
    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
    fun findByIdWithItems(id: Long): Order?
}
```

**Option 2:** Use @EntityGraph

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {
    @EntityGraph(attributePaths = ["items"])
    fun findWithItemsById(id: Long): Order?
}
```

**Option 3:** Initialize in service (DTO conversion)

```kotlin
@Transactional(readOnly = true)
fun getOrderDto(id: Long): OrderDto? {
    val order = orderRepository.findById(id) ?: return null
    return OrderDto(
        id = order.id,
        items = order.items.map { it.toDto() },  // Access within transaction
    )
}
```

### N+1 Problem

```kotlin
// Bad: 1 query for orders + N queries for items
@Transactional(readOnly = true)
fun getAllOrders(): List<OrderDto> {
    val orders = orderRepository.findAll()  // 1 query
    return orders.map { order ->
        OrderDto(
            id = order.id,
            items = order.items.map { it.toDto() },  // N queries
        )
    }
}

// Good: Single query with JOIN FETCH
@Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.items")
fun findAllWithItems(): List<Order>
```

### OSIV (Open Session In View)

Spring Boot enables OSIV by default - keeps session open in view layer.

```yaml
# application.yml - Disable OSIV (recommended for production)
spring:
  jpa:
    open-in-view: false
```

| OSIV | Pros | Cons |
|------|------|------|
| Enabled | No LazyInitializationException in view | DB connection held longer, hidden N+1 |
| Disabled | Clear transaction boundaries | Must handle lazy loading explicitly |

## Optimistic vs Pessimistic Locking

### Optimistic Locking (@Version)

Detects concurrent modifications at commit time:

```kotlin
@Entity
class Product(
    @Id val id: Long,
    var name: String,
    var stock: Int,
    @Version
    var version: Long = 0,  // Auto-incremented on update
)

@Service
class ProductService(private val productRepository: ProductRepository) {

    @Transactional
    fun updateStock(id: Long, delta: Int) {
        val product = productRepository.findById(id)
            ?: throw ProductNotFoundException(id)
        product.stock += delta
        productRepository.save(product)
        // Throws OptimisticLockingFailureException if version mismatch
    }
}
```

**Handle conflicts:**

```kotlin
@Transactional
fun updateStockWithRetry(id: Long, delta: Int, maxRetries: Int = 3) {
    repeat(maxRetries) { attempt ->
        try {
            updateStock(id, delta)
            return
        } catch (e: OptimisticLockingFailureException) {
            if (attempt == maxRetries - 1) throw e
            // Retry with fresh data
        }
    }
}
```

### Pessimistic Locking (@Lock)

Acquires database lock immediately:

```kotlin
interface ProductRepository : JpaRepository<Product, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    fun findByIdForUpdate(id: Long): Product?

    @Lock(LockModeType.PESSIMISTIC_READ)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    fun findByIdWithSharedLock(id: Long): Product?
}

@Transactional
fun decrementStock(productId: Long, quantity: Int) {
    val product = productRepository.findByIdForUpdate(productId)  // Locks row
        ?: throw ProductNotFoundException(productId)

    if (product.stock < quantity) {
        throw InsufficientStockException(productId)
    }
    product.stock -= quantity
    productRepository.save(product)
}
```

| Type | Use Case | Trade-off |
|------|----------|-----------|
| **Optimistic** | Low contention, read-heavy | Retries on conflict |
| **Pessimistic** | High contention, critical sections | Blocks other transactions |

## Batch Operations

### Batch Insert

```kotlin
@Service
class ProductBatchService(
    private val productRepository: ProductRepository,
    private val entityManager: EntityManager,
) {
    @Transactional
    fun batchInsert(products: List<Product>) {
        products.forEachIndexed { index, product ->
            entityManager.persist(product)

            // Flush and clear every 50 items to avoid memory issues
            if (index > 0 && index % 50 == 0) {
                entityManager.flush()
                entityManager.clear()
            }
        }
    }
}
```

**Enable batch insert in configuration:**

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
```

### Bulk Update/Delete

```kotlin
interface ProductRepository : JpaRepository<Product, Long> {

    @Modifying
    @Query("UPDATE Product p SET p.price = p.price * :multiplier WHERE p.category = :category")
    fun updatePriceByCategory(category: String, multiplier: BigDecimal): Int

    @Modifying
    @Query("DELETE FROM Product p WHERE p.stock = 0")
    fun deleteOutOfStock(): Int
}

@Transactional
fun applyDiscount(category: String, discountPercent: Int): Int {
    val multiplier = BigDecimal.ONE - BigDecimal(discountPercent).divide(BigDecimal(100))
    return productRepository.updatePriceByCategory(category, multiplier)
}
```

> **Note:** Bulk operations bypass entity lifecycle - `@Version` not updated, caches not invalidated.

## Transaction Timeout

Prevent long-running transactions from holding resources:

```kotlin
@Transactional(timeout = 5)  // 5 seconds
fun processLargeData(data: List<Item>) {
    data.forEach { item ->
        // Throws TransactionTimedOutException if exceeds 5 seconds
        itemRepository.save(process(item))
    }
}
```

**Global default:**

```yaml
spring:
  transaction:
    default-timeout: 30  # 30 seconds
```

**Use cases:**
- Batch jobs with known time limits
- Preventing runaway queries
- SLA enforcement

## Deadlock Prevention

### Consistent Lock Ordering

```kotlin
// Bad: Different lock order can cause deadlock
// Thread 1: locks A, then B
// Thread 2: locks B, then A

@Transactional
fun transfer(fromId: Long, toId: Long, amount: BigDecimal) {
    val from = accountRepository.findByIdForUpdate(fromId)
    val to = accountRepository.findByIdForUpdate(toId)  // Deadlock risk!
    // ...
}

// Good: Always lock in consistent order (e.g., by ID)
@Transactional
fun transfer(fromId: Long, toId: Long, amount: BigDecimal) {
    val (firstId, secondId) = if (fromId < toId) fromId to toId else toId to fromId

    val first = accountRepository.findByIdForUpdate(firstId)
    val second = accountRepository.findByIdForUpdate(secondId)

    val from = if (fromId < toId) first else second
    val to = if (fromId < toId) second else first
    // ...
}
```

### Lock Timeout

```kotlin
interface AccountRepository : JpaRepository<Account, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(QueryHint(name = "javax.persistence.lock.timeout", value = "3000"))  // 3 seconds
    @Query("SELECT a FROM Account a WHERE a.id = :id")
    fun findByIdForUpdateWithTimeout(id: Long): Account?
}
```

### Deadlock Detection & Retry

```kotlin
@Service
class TransferService(private val accountRepository: AccountRepository) {

    @Retryable(
        value = [DeadlockLoserDataAccessException::class],
        maxAttempts = 3,
        backoff = Backoff(delay = 100, multiplier = 2.0),
    )
    @Transactional
    fun transfer(fromId: Long, toId: Long, amount: BigDecimal) {
        // ... transfer logic
    }
}
```

## Entity State Management

### Entity States

| State | Description | Managed by EntityManager |
|-------|-------------|-------------------------|
| **New/Transient** | Not yet persisted | No |
| **Managed** | Associated with persistence context | Yes |
| **Detached** | Was managed, now outside transaction | No |
| **Removed** | Marked for deletion | Yes |

### State Transitions

```kotlin
@Transactional
fun entityLifecycle() {
    // New -> Managed
    val user = User(name = "John")
    entityManager.persist(user)  // Now managed

    // Managed: changes auto-tracked
    user.name = "Jane"  // Will be saved at flush

    // Managed -> Detached (at transaction end or explicit)
    entityManager.detach(user)

    // Detached -> Managed
    val merged = entityManager.merge(user)  // Returns managed copy

    // Managed -> Removed
    entityManager.remove(merged)
}
```

### Detached Entity Pitfalls

```kotlin
// Bad: Modifying detached entity has no effect
fun updateOutsideTransaction(user: User) {
    user.name = "Updated"  // user is detached, change is lost
    userRepository.save(user)  // This works because save() does merge
}

// Good: Explicit merge or use repository
@Transactional
fun updateUser(userId: Long, newName: String) {
    val user = userRepository.findById(userId)
        ?: throw UserNotFoundException(userId)
    user.name = newName  // Managed entity, auto-tracked
    // No explicit save needed - dirty checking handles it
}
```

### Dirty Checking

```kotlin
@Transactional
fun updateUserName(userId: Long, newName: String) {
    val user = userRepository.findById(userId)
        ?: throw UserNotFoundException(userId)

    user.name = newName
    // No save() call needed!
    // Hibernate detects change and generates UPDATE at flush
}
```

> **Tip:** Avoid unnecessary `save()` calls on managed entities - dirty checking handles updates automatically.

## Testing Transactions

**@DataJpaTest** includes `@Transactional` by default (auto-rollback after each test):

```kotlin
@DataJpaTest
class UserRepositoryTest(
    @Autowired private val userRepository: UserRepository,
) {
    @Test
    fun `should save user`() {
        val user = userRepository.save(User(name = "John"))
        assertNotNull(user.id)
        // Automatically rolled back after test
    }
}
```

**Disable auto-rollback when needed:**

```kotlin
@DataJpaTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class UserRepositoryIntegrationTest
```
