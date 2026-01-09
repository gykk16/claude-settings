# JPA & Hibernate

JPA (Java Persistence API) entity mapping, fetch strategies, and persistence context management.

## Entity Principles

> **Keep entities simple.** Extend BaseEntity. Use standard annotations. Avoid bidirectional unless necessary.

| Guideline | Description |
|-----------|-------------|
| **Extend BaseEntity** | Always extend BaseEntity for audit columns |
| **Standard annotations** | `@Entity`, `@Table`, `@NoArgsConstructor`, `@Getter` |
| **Enum as STRING** | Always use `@Enumerated(EnumType.STRING)` |
| **Lazy by default** | Use `FetchType.LAZY` for associations |
| **Avoid bidirectional** | Unidirectional is simpler to manage |

---

## Base Entity Pattern

### BaseTimeEntity

```kotlin
@EntityListeners(AuditingEntityListener::class)
@MappedSuperclass
abstract class BaseTimeEntity(
    @CreatedDate
    @Column(updatable = false)
    var createdAt: LocalDateTime? = null,

    @LastModifiedDate
    var modifiedAt: LocalDateTime? = null,
)
```

### BaseEntity

```kotlin
@EntityListeners(AuditingEntityListener::class)
@MappedSuperclass
abstract class BaseEntity(
    @CreatedBy
    @Column(length = 30, updatable = false)
    var createdBy: String? = null,

    @LastModifiedBy
    @Column(length = 30)
    var modifiedBy: String? = null,
) : BaseTimeEntity()
```

### Enable JPA Auditing

```kotlin
@Configuration
@EnableJpaAuditing
class JpaConfig {

    @Bean
    fun auditorProvider(): AuditorAware<String> = AuditorAware {
        Optional.ofNullable(SecurityContextHolder.getContext().authentication?.name)
    }
}
```

---

## JPA Configuration

### Recommended Settings

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: none              # Never auto-generate DDL in production
    properties:
      hibernate:
        format_sql: false         # true only for debugging
        default_batch_fetch_size: 500
        order_updates: true       # Group updates for batch efficiency
        order_inserts: true       # Group inserts for batch efficiency
        jdbc:
          batch_size: 500         # Batch insert/update size
    open-in-view: false           # Disable OSIV (recommended)
```

### Configuration Options

| Property | Value | Description |
|----------|-------|-------------|
| `ddl-auto` | `none` | Never auto-generate DDL in production |
| `format_sql` | `false` | Set `true` only for debugging |
| `default_batch_fetch_size` | `500` | Fetch size for lazy collections (prevents N+1) |
| `order_updates` | `true` | Group updates by entity type for batch efficiency |
| `order_inserts` | `true` | Group inserts by entity type for batch efficiency |
| `batch_size` | `500` | JDBC batch size for bulk operations |
| `open-in-view` | `false` | Disable OSIV - explicit transaction boundaries |

### Development vs Production

```yaml
# Development - enable SQL logging
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true

# Production - disable SQL logging
spring:
  jpa:
    show-sql: false
    properties:
      hibernate:
        format_sql: false
```

### OSIV (Open Session In View)

> **Always disable OSIV in production** with `open-in-view: false`

| OSIV | Pros | Cons |
|------|------|------|
| `true` (default) | No LazyInitializationException in view | DB connection held longer, hidden N+1 |
| `false` (recommended) | Clear transaction boundaries, better performance | Must handle lazy loading explicitly |

---

## Entity Definition

### Standard Entity Structure

> **Always include:** `@Entity`, `@Table`, `@NoArgsConstructor(access = PROTECTED)`, `@Getter`, extend `BaseEntity`

```kotlin
@Entity
@Table(name = "tb_users")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
class User(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    val id: Long = 0,

    @Column(nullable = false, length = 100)
    var name: String,

    @Column(nullable = false, unique = true)
    var email: String,

    @Enumerated(EnumType.STRING)  // Always STRING, never ORDINAL
    @Column(length = 20)
    var status: UserStatus = UserStatus.ACTIVE,
) : BaseEntity()

enum class UserStatus {
    ACTIVE, INACTIVE, SUSPENDED
}
```

### Entity Annotation Checklist

| Annotation | Purpose | Required |
|------------|---------|----------|
| `@Entity` | Mark as JPA entity | Yes |
| `@Table(name = "tb_xxx")` | Specify table name | Yes |
| `@NoArgsConstructor(access = PROTECTED)` | JPA requires no-arg constructor | Yes |
| `@Getter` | Lombok getter generation | Yes |
| `extends BaseEntity` | Inherit audit columns | Yes |

### Enum Mapping

> **Always use `@Enumerated(EnumType.STRING)`** - never use ORDINAL.

```kotlin
// Good: STRING - safe for refactoring
@Enumerated(EnumType.STRING)
@Column(length = 20)
var status: UserStatus = UserStatus.ACTIVE

// Bad: ORDINAL - breaks if enum order changes
@Enumerated(EnumType.ORDINAL)  // DON'T USE
var status: UserStatus = UserStatus.ACTIVE
```

Why STRING over ORDINAL:
- **ORDINAL** stores index (0, 1, 2) - breaks if enum order changes
- **STRING** stores name ("ACTIVE") - safe for reordering, readable in DB

### ID Generation Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `IDENTITY` | DB auto-increment | MySQL, PostgreSQL |
| `SEQUENCE` | DB sequence | PostgreSQL, Oracle |
| `TABLE` | Separate table | Portable but slow |
| `AUTO` | Provider chooses | Avoid (unpredictable) |

```kotlin
// IDENTITY - most common
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
val id: Long = 0

// SEQUENCE - better for batch inserts
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "user_seq")
@SequenceGenerator(name = "user_seq", sequenceName = "user_sequence", allocationSize = 50)
val id: Long = 0
```

### Column Mapping

```kotlin
@Entity
class Product(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(name = "product_name", nullable = false, length = 200)
    var name: String,

    @Column(precision = 10, scale = 2)
    var price: BigDecimal,

    @Column(columnDefinition = "TEXT")
    var description: String? = null,

    @Lob
    var largeContent: ByteArray? = null,

    @Transient  // Not persisted
    var calculatedField: String? = null,
)
```

---

## Association Mapping

### ManyToOne (Recommended Default)

```kotlin
@Entity
class Order(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    val user: User,

    var totalAmount: BigDecimal,
)
```

### OneToMany (Use Sparingly)

```kotlin
@Entity
class Order(
    @Id val id: Long = 0,

    // Unidirectional - Order owns the relationship
    @OneToMany(cascade = [CascadeType.ALL], orphanRemoval = true)
    @JoinColumn(name = "order_id")
    val items: MutableList<OrderItem> = mutableListOf(),
)

// Bidirectional - when navigating from both sides is needed
@Entity
class Order(
    @Id val id: Long = 0,

    @OneToMany(mappedBy = "order", cascade = [CascadeType.ALL], orphanRemoval = true)
    val items: MutableList<OrderItem> = mutableListOf(),
) {
    fun addItem(item: OrderItem) {
        items.add(item)
        item.order = this
    }

    fun removeItem(item: OrderItem) {
        items.remove(item)
        item.order = null
    }
}

@Entity
class OrderItem(
    @Id val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    var order: Order? = null,

    var productName: String,
    var quantity: Int,
)
```

### ManyToMany (Avoid When Possible)

```kotlin
// Prefer explicit join entity for better control
@Entity
class Student(
    @Id val id: Long = 0,
    var name: String,

    @OneToMany(mappedBy = "student")
    val enrollments: List<Enrollment> = emptyList(),
)

@Entity
class Course(
    @Id val id: Long = 0,
    var title: String,

    @OneToMany(mappedBy = "course")
    val enrollments: List<Enrollment> = emptyList(),
)

@Entity
class Enrollment(
    @Id val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id")
    val student: Student,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "course_id")
    val course: Course,

    val enrolledAt: LocalDateTime = LocalDateTime.now(),
    var grade: String? = null,
)
```

### OneToOne

```kotlin
@Entity
class User(
    @Id val id: Long = 0,
    var name: String,

    @OneToOne(mappedBy = "user", cascade = [CascadeType.ALL], fetch = FetchType.LAZY)
    var profile: UserProfile? = null,
)

@Entity
class UserProfile(
    @Id val id: Long = 0,

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    @MapsId  // Share primary key with User
    val user: User,

    var bio: String? = null,
    var avatarUrl: String? = null,
)
```

---

## Fetch Strategies

### FetchType.LAZY vs EAGER

| Type | Behavior | Default For |
|------|----------|-------------|
| `LAZY` | Load on access | `@OneToMany`, `@ManyToMany` |
| `EAGER` | Load immediately | `@ManyToOne`, `@OneToOne` |

> **Best Practice:** Always use `LAZY` and fetch explicitly when needed.

```kotlin
// Always specify LAZY for ManyToOne/OneToOne
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "user_id")
val user: User
```

### JOIN FETCH

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {

    // Single association
    @Query("SELECT o FROM Order o JOIN FETCH o.user WHERE o.id = :id")
    fun findByIdWithUser(id: Long): Order?

    // Multiple associations
    @Query("""
        SELECT DISTINCT o FROM Order o
        JOIN FETCH o.user
        JOIN FETCH o.items
        WHERE o.id = :id
    """)
    fun findByIdWithUserAndItems(id: Long): Order?

    // Collection with pagination (use two queries)
    @Query("SELECT o FROM Order o JOIN FETCH o.user WHERE o.status = :status")
    fun findByStatusWithUser(status: OrderStatus, pageable: Pageable): Page<Order>
}
```

### EntityGraph

Declarative fetch strategy without JPQL:

```kotlin
@Entity
@NamedEntityGraph(
    name = "Order.withUserAndItems",
    attributeNodes = [
        NamedAttributeNode("user"),
        NamedAttributeNode("items"),
    ],
)
class Order(
    @Id val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY)
    val user: User,

    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    val items: List<OrderItem> = emptyList(),
)

interface OrderRepository : JpaRepository<Order, Long> {

    // Use named entity graph
    @EntityGraph("Order.withUserAndItems")
    fun findWithGraphById(id: Long): Order?

    // Ad-hoc entity graph
    @EntityGraph(attributePaths = ["user", "items"])
    fun findWithUserAndItemsById(id: Long): Order?

    // With query
    @EntityGraph(attributePaths = ["user"])
    @Query("SELECT o FROM Order o WHERE o.status = :status")
    fun findByStatusWithUser(status: OrderStatus): List<Order>
}
```

### Nested EntityGraph

```kotlin
@NamedEntityGraph(
    name = "Order.full",
    attributeNodes = [
        NamedAttributeNode("user"),
        NamedAttributeNode(value = "items", subgraph = "items-subgraph"),
    ],
    subgraphs = [
        NamedSubgraph(
            name = "items-subgraph",
            attributeNodes = [NamedAttributeNode("product")],
        ),
    ],
)
class Order(...)
```

---

## Lazy Loading & N+1 Problem

### LazyInitializationException

Accessing lazy associations outside transaction:

```kotlin
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

```kotlin
// Option 1: JOIN FETCH in repository (Recommended)
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
fun findByIdWithItems(id: Long): Order?

// Option 2: EntityGraph
@EntityGraph(attributePaths = ["items"])
fun findWithItemsById(id: Long): Order?

// Option 3: Initialize in service (DTO conversion)
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
// Bad: 1 query for orders + N queries for users
@Transactional(readOnly = true)
fun getAllOrders(): List<OrderDto> {
    val orders = orderRepository.findAll()  // 1 query
    return orders.map { order ->
        OrderDto(
            id = order.id,
            userName = order.user.name,  // N queries!
        )
    }
}

// Good: Single query with JOIN FETCH
@Query("SELECT o FROM Order o JOIN FETCH o.user")
fun findAllWithUser(): List<Order>
```

### OSIV (Open Session In View)

Spring Boot enables OSIV by default:

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

---

## Optimistic Locking

Detects concurrent modifications at commit time using `@Version`:

```kotlin
@Entity
class Product(
    @Id val id: Long = 0,
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
        // Throws OptimisticLockingFailureException if version mismatch
    }
}
```

**Handle conflicts with retry:**

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

---

## Pessimistic Locking

Acquires database lock immediately:

```kotlin
interface ProductRepository : JpaRepository<Product, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    fun findByIdForUpdate(id: Long): Product?

    @Lock(LockModeType.PESSIMISTIC_READ)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    fun findByIdWithSharedLock(id: Long): Product?

    // With timeout
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(QueryHint(name = "javax.persistence.lock.timeout", value = "3000"))
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    fun findByIdForUpdateWithTimeout(id: Long): Product?
}

@Transactional
fun decrementStock(productId: Long, quantity: Int) {
    val product = productRepository.findByIdForUpdate(productId)
        ?: throw ProductNotFoundException(productId)

    if (product.stock < quantity) {
        throw InsufficientStockException(productId)
    }
    product.stock -= quantity
}
```

| Type | Use Case | Trade-off |
|------|----------|-----------|
| **Optimistic** | Low contention, read-heavy | Retries on conflict |
| **Pessimistic** | High contention, critical sections | Blocks other transactions |

---

## Entity State Management

### Entity States

| State | Description | Managed by EntityManager |
|-------|-------------|--------------------------|
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

    // Managed: changes auto-tracked (dirty checking)
    user.name = "Jane"  // Will be saved at flush

    // Managed -> Detached (at transaction end or explicit)
    entityManager.detach(user)

    // Detached -> Managed
    val merged = entityManager.merge(user)  // Returns managed copy

    // Managed -> Removed
    entityManager.remove(merged)
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

> **Tip:** Avoid unnecessary `save()` calls on managed entities.

### Detached Entity Pitfalls

```kotlin
// Bad: Modifying detached entity outside transaction
fun updateOutsideTransaction(user: User) {
    user.name = "Updated"  // user is detached, change is lost!
}

// Good: Fetch and modify within transaction
@Transactional
fun updateUser(userId: Long, newName: String) {
    val user = userRepository.findById(userId)
        ?: throw UserNotFoundException(userId)
    user.name = newName  // Managed entity, auto-tracked
}
```

---

## Specification (Dynamic Queries)

For type-safe, composable queries:

```kotlin
interface UserRepository : JpaRepository<User, Long>, JpaSpecificationExecutor<User>

object UserSpecifications {

    fun hasName(name: String): Specification<User> =
        Specification { root, _, cb ->
            cb.like(cb.lower(root.get("name")), "%${name.lowercase()}%")
        }

    fun hasStatus(status: UserStatus): Specification<User> =
        Specification { root, _, cb ->
            cb.equal(root.get<UserStatus>("status"), status)
        }

    fun createdAfter(date: LocalDateTime): Specification<User> =
        Specification { root, _, cb ->
            cb.greaterThan(root.get("createdAt"), date)
        }

    fun hasEmail(email: String): Specification<User> =
        Specification { root, _, cb ->
            cb.equal(root.get<String>("email"), email)
        }
}

// Usage
@Service
class UserService(private val userRepository: UserRepository) {

    fun search(
        name: String?,
        status: UserStatus?,
        since: LocalDateTime?,
        pageable: Pageable,
    ): Page<User> {
        var spec = Specification.where<User>(null)

        name?.let { spec = spec.and(UserSpecifications.hasName(it)) }
        status?.let { spec = spec.and(UserSpecifications.hasStatus(it)) }
        since?.let { spec = spec.and(UserSpecifications.createdAfter(it)) }

        return userRepository.findAll(spec, pageable)
    }
}
```

### Complex Specifications

```kotlin
object OrderSpecifications {

    fun hasUserStatus(status: UserStatus): Specification<Order> =
        Specification { root, _, cb ->
            val userJoin = root.join<Order, User>("user")
            cb.equal(userJoin.get<UserStatus>("status"), status)
        }

    fun totalAmountBetween(min: BigDecimal, max: BigDecimal): Specification<Order> =
        Specification { root, _, cb ->
            cb.between(root.get("totalAmount"), min, max)
        }

    fun createdInDateRange(start: LocalDateTime, end: LocalDateTime): Specification<Order> =
        Specification { root, _, cb ->
            cb.between(root.get("createdAt"), start, end)
        }
}

// Combine with OR
fun hasHighValueOrPremiumUser(): Specification<Order> =
    OrderSpecifications.totalAmountBetween(BigDecimal(1000), BigDecimal.valueOf(Long.MAX_VALUE))
        .or(OrderSpecifications.hasUserStatus(UserStatus.PREMIUM))
```

---

## Batch Operations

### Batch Insert

```kotlin
@Service
class ProductBatchService(
    private val entityManager: EntityManager,
) {
    @Transactional
    fun batchInsert(products: List<Product>) {
        products.forEachIndexed { index, product ->
            entityManager.persist(product)

            // Flush and clear every 50 items
            if (index > 0 && index % 50 == 0) {
                entityManager.flush()
                entityManager.clear()
            }
        }
    }
}
```

**Configuration:**

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

    @Modifying(clearAutomatically = true)
    @Query("UPDATE Product p SET p.price = p.price * :multiplier WHERE p.category = :category")
    fun updatePriceByCategory(category: String, multiplier: BigDecimal): Int

    @Modifying
    @Query("DELETE FROM Product p WHERE p.stock = 0")
    fun deleteOutOfStock(): Int
}
```

> **Warning:** Bulk operations bypass entity lifecycle - `@Version` not updated, caches not invalidated.

---

## Soft Delete

```kotlin
@Entity
@Where(clause = "deleted_at IS NULL")  // Auto-filter deleted records
@SQLDelete(sql = "UPDATE users SET deleted_at = NOW() WHERE id = ?")
class User(
    @Id val id: Long = 0,
    var name: String,
    var deletedAt: LocalDateTime? = null,
)

interface UserRepository : JpaRepository<User, Long> {

    // Automatically excludes soft-deleted due to @Where

    // Include soft-deleted explicitly
    @Query("SELECT u FROM User u WHERE u.id = :id")
    @Where(clause = "")  // Override default filter
    fun findByIdIncludingDeleted(id: Long): User?
}
```

---

## Common Pitfalls

### 1. N+1 Queries

```kotlin
// Bad
orders.forEach { it.user.name }  // N queries

// Good
@Query("SELECT o FROM Order o JOIN FETCH o.user")
fun findAllWithUser(): List<Order>
```

### 2. Eager Loading Everything

```kotlin
// Bad
@ManyToOne  // Default EAGER
val user: User

// Good
@ManyToOne(fetch = FetchType.LAZY)
val user: User
```

### 3. Bidirectional Without Sync

```kotlin
// Bad: Inconsistent state
order.items.add(item)
// item.order is still null!

// Good: Helper methods
fun addItem(item: OrderItem) {
    items.add(item)
    item.order = this
}
```

### 4. Modifying Detached Entities

```kotlin
// Bad: Changes lost
fun updateName(user: User, name: String) {
    user.name = name  // Detached - no effect
}

// Good: Fetch within transaction
@Transactional
fun updateName(userId: Long, name: String) {
    val user = userRepository.findById(userId)!!
    user.name = name  // Managed - tracked
}
```

---

## Summary

| Topic | Key Point |
|-------|-----------|
| **Entity Structure** | `@Entity`, `@Table`, `@NoArgsConstructor(PROTECTED)`, `@Getter` |
| **Base Entity** | Always extend `BaseEntity` for audit columns |
| **Enum** | Always `@Enumerated(EnumType.STRING)`, never ORDINAL |
| **Associations** | Prefer unidirectional, always LAZY |
| **Fetching** | JOIN FETCH or EntityGraph for needed data |
| **N+1** | Detect with logging, fix with fetch joins |
| **Locking** | Optimistic for low contention, pessimistic for high |
| **State** | Understand managed vs detached |
| **Batch** | Flush/clear periodically, enable batch config |
