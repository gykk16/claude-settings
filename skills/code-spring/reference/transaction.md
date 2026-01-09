# Transaction Management

For JPA-specific topics (Lazy Loading, N+1, Locking, Entity State), see [jpa.md](jpa.md).

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
