# JPA & Hibernate

JPA entity mapping, fetch strategies, and persistence context management.

## Key Principles

> **Keep entities simple.** Extend BaseEntity. Use LAZY fetching. Avoid bidirectional unless necessary.

| Guideline | Description |
|-----------|-------------|
| **Extend BaseEntity** | Inherit audit columns (createdAt, modifiedAt, etc.) |
| **Enum as STRING** | Always `@Enumerated(EnumType.STRING)`, never ORDINAL |
| **LAZY by default** | Use `FetchType.LAZY` for all associations |
| **Avoid bidirectional** | Unidirectional is simpler to manage |

---

## Entity Structure

### Standard Entity Pattern

```kotlin
@Entity
@Table(name = "tb_users")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Getter
class User(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = false, length = 100)
    var name: String,

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    var status: UserStatus = UserStatus.ACTIVE,
) : BaseEntity()
```

### Entity Checklist

| Annotation | Purpose | Required |
|------------|---------|----------|
| `@Entity` | Mark as JPA entity | Yes |
| `@Table(name = "tb_xxx")` | Specify table name | Yes |
| `@NoArgsConstructor(access = PROTECTED)` | JPA requires no-arg constructor | Yes |
| `@Getter` | Lombok getter generation | Yes |
| `extends BaseEntity` | Inherit audit columns | Yes |

### BaseEntity Pattern

```kotlin
@EntityListeners(AuditingEntityListener::class)
@MappedSuperclass
abstract class BaseEntity(
    @CreatedDate
    @Column(updatable = false)
    var createdAt: LocalDateTime? = null,

    @LastModifiedDate
    var modifiedAt: LocalDateTime? = null,

    @CreatedBy
    @Column(length = 30, updatable = false)
    var createdBy: String? = null,

    @LastModifiedBy
    @Column(length = 30)
    var modifiedBy: String? = null,
)
```

---

## Association Mapping

### Decision: Which Relationship Type?

| Relationship | Direction | Use When |
|--------------|-----------|----------|
| `@ManyToOne` | Unidirectional | Most common - child references parent |
| `@OneToMany` | Unidirectional | Parent owns collection, use sparingly |
| `@OneToMany` | Bidirectional | Need navigation from both sides |
| `@OneToOne` | Either | Rare, consider embedding instead |
| `@ManyToMany` | Avoid | Use explicit join entity instead |

### ManyToOne (Recommended Default)

```kotlin
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "user_id", nullable = false)
val user: User
```

### OneToMany (Use Sparingly)

```kotlin
// Unidirectional
@OneToMany(cascade = [CascadeType.ALL], orphanRemoval = true)
@JoinColumn(name = "order_id")
val items: MutableList<OrderItem> = mutableListOf()

// Bidirectional - needs helper methods
@OneToMany(mappedBy = "order", cascade = [CascadeType.ALL], orphanRemoval = true)
val items: MutableList<OrderItem> = mutableListOf()

fun addItem(item: OrderItem) {
    items.add(item)
    item.order = this
}
```

---

## Fetch Strategies

### LAZY vs EAGER

| Type | Behavior | Default For | Recommendation |
|------|----------|-------------|----------------|
| `LAZY` | Load on access | `@OneToMany`, `@ManyToMany` | **Always use** |
| `EAGER` | Load immediately | `@ManyToOne`, `@OneToOne` | Avoid |

> **Always specify LAZY** for `@ManyToOne` and `@OneToOne` - the defaults are EAGER.

### Solving Lazy Loading Issues

| Problem | Solution |
|---------|----------|
| LazyInitializationException | Use JOIN FETCH or EntityGraph |
| N+1 queries | Use JOIN FETCH for batch loading |
| Need data outside transaction | Convert to DTO within transaction |

```kotlin
// JOIN FETCH - prevents N+1
@Query("SELECT o FROM Order o JOIN FETCH o.user WHERE o.id = :id")
fun findByIdWithUser(id: Long): Order?

// EntityGraph - declarative fetch
@EntityGraph(attributePaths = ["user", "items"])
fun findWithDetailsById(id: Long): Order?
```

---

## Locking Strategies

| Type | Use Case | Trade-off |
|------|----------|-----------|
| **Optimistic** (`@Version`) | Low contention, read-heavy | Retries on conflict |
| **Pessimistic** (`@Lock`) | High contention, critical sections | Blocks other transactions |

### Optimistic Locking

```kotlin
@Entity
class Product(
    @Id val id: Long = 0,
    var stock: Int,

    @Version
    var version: Long = 0,  // Auto-incremented on update
)
```

### Pessimistic Locking

```kotlin
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT p FROM Product p WHERE p.id = :id")
fun findByIdForUpdate(id: Long): Product?
```

---

## Entity State

| State | Description | Tracked by JPA |
|-------|-------------|----------------|
| **New/Transient** | Not yet persisted | No |
| **Managed** | In persistence context | Yes (dirty checking) |
| **Detached** | Outside transaction | No |
| **Removed** | Marked for deletion | Yes |

### Dirty Checking

```kotlin
@Transactional
fun updateUserName(userId: Long, newName: String) {
    val user = userRepository.findById(userId)!!
    user.name = newName
    // No save() needed - JPA detects change automatically
}
```

---

## Configuration

### Recommended Settings

```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: none              # Never auto-generate DDL in production
    properties:
      hibernate:
        default_batch_fetch_size: 500
        order_updates: true
        order_inserts: true
        jdbc:
          batch_size: 500
    open-in-view: false           # Disable OSIV (recommended)
```

### OSIV (Open Session In View)

| OSIV | Pros | Cons |
|------|------|------|
| `true` (default) | No LazyInitializationException in view | DB connection held longer, hidden N+1 |
| `false` (recommended) | Clear transaction boundaries | Must handle lazy loading explicitly |

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| N+1 queries | 1 + N queries for lazy associations | Use `JOIN FETCH` or `@EntityGraph` |
| EAGER everywhere | Loads unnecessary data | Always use LAZY, fetch explicitly |
| Bidirectional without sync | Inconsistent state | Use helper methods to sync both sides |
| Modifying detached entities | Changes not saved | Fetch within transaction |
| `@Enumerated(ORDINAL)` | Breaks if enum order changes | Always use `STRING` |
| Missing `@Version` | Lost updates in concurrent scenarios | Add optimistic locking for mutable entities |
| Large batch without flush | OutOfMemoryError | Flush and clear every N items |

---

## Summary

| Topic | Key Point |
|-------|-----------|
| **Entity** | `@Entity`, `@Table`, `@NoArgsConstructor(PROTECTED)`, extend BaseEntity |
| **Enum** | Always `@Enumerated(EnumType.STRING)` |
| **Associations** | Prefer unidirectional, always LAZY |
| **Fetching** | JOIN FETCH or EntityGraph for needed data |
| **N+1** | Detect with logging, fix with fetch joins |
| **Locking** | Optimistic for low contention, pessimistic for high |
| **OSIV** | Disable with `open-in-view: false` |
