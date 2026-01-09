# Repository Layer

Repository layer handles data access using Spring Data JPA.

For JPA entity mapping, fetch strategies, and locking, see [jpa.md](jpa.md).

## Repository Principles

> **Keep queries simple.** Use query methods for simple cases, JPQL for complex ones.

| Guideline | Description |
|-----------|-------------|
| **Interface-based** | Extend JpaRepository, no implementation needed |
| **Query methods first** | Use method naming conventions for simple queries |
| **JPQL for complex** | Use @Query for joins, aggregations, projections |
| **Native SQL last resort** | Only when JPQL can't express the query |

## Basic Repository

```kotlin
interface UserRepository : JpaRepository<User, Long> {
    // Inherited: save, findById, findAll, delete, count, existsById, etc.
}

// For entity definition, see jpa.md
```

## Query Methods

Spring Data JPA generates queries from method names.

### Basic Patterns

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    // findBy + Property
    fun findByEmail(email: String): User?
    fun findByName(name: String): List<User>

    // Multiple conditions
    fun findByNameAndStatus(name: String, status: UserStatus): List<User>
    fun findByNameOrEmail(name: String, email: String): List<User>

    // Comparison
    fun findByAgeGreaterThan(age: Int): List<User>
    fun findByAgeLessThanEqual(age: Int): List<User>
    fun findByAgeBetween(start: Int, end: Int): List<User>

    // Null checks
    fun findByDeletedAtIsNull(): List<User>
    fun findByDeletedAtIsNotNull(): List<User>

    // String matching
    fun findByNameContaining(keyword: String): List<User>
    fun findByNameStartingWith(prefix: String): List<User>
    fun findByNameEndingWith(suffix: String): List<User>
    fun findByNameIgnoreCase(name: String): User?

    // Collection
    fun findByStatusIn(statuses: Collection<UserStatus>): List<User>
    fun findByStatusNotIn(statuses: Collection<UserStatus>): List<User>

    // Boolean
    fun findByActiveTrue(): List<User>
    fun findByActiveFalse(): List<User>
}
```

### Sorting & Limiting

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    // OrderBy
    fun findByStatusOrderByCreatedAtDesc(status: UserStatus): List<User>
    fun findByStatusOrderByNameAscCreatedAtDesc(status: UserStatus): List<User>

    // First, Top
    fun findFirstByOrderByCreatedAtDesc(): User?
    fun findTop10ByStatusOrderByCreatedAtDesc(status: UserStatus): List<User>

    // With Sort parameter
    fun findByStatus(status: UserStatus, sort: Sort): List<User>
}

// Usage
val users = userRepository.findByStatus(
    UserStatus.ACTIVE,
    Sort.by(Sort.Direction.DESC, "createdAt"),
)
```

### Existence & Count

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    fun existsByEmail(email: String): Boolean
    fun countByStatus(status: UserStatus): Long
}
```

## Pagination

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    fun findByStatus(status: UserStatus, pageable: Pageable): Page<User>

    // Slice - doesn't count total (better performance)
    fun findSliceByStatus(status: UserStatus, pageable: Pageable): Slice<User>
}

// Usage
@Service
class UserService(private val userRepository: UserRepository) {

    fun getActiveUsers(page: Int, size: Int): Page<User> {
        val pageable = PageRequest.of(page, size, Sort.by("createdAt").descending())
        return userRepository.findByStatus(UserStatus.ACTIVE, pageable)
    }
}

// Controller
@GetMapping
fun getUsers(
    @RequestParam(defaultValue = "0") page: Int,
    @RequestParam(defaultValue = "20") size: Int,
): ResponseEntity<Page<UserDto>> {
    val users = userService.getActiveUsers(page, size)
    return ResponseEntity.ok(users.map { it.toDto() })
}
```

### Page vs Slice

| Type | Total Count | Use Case |
|------|-------------|----------|
| `Page<T>` | Yes (extra query) | When total count needed (pagination UI) |
| `Slice<T>` | No | Infinite scroll, "Load more" |
| `List<T>` | No | Simple list without pagination info |

## JPQL Queries

Use `@Query` for complex queries that can't be expressed with method names.

### Basic JPQL

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    @Query("SELECT u FROM User u WHERE u.email = :email")
    fun findByEmailQuery(@Param("email") email: String): User?

    @Query("SELECT u FROM User u WHERE u.status = :status AND u.createdAt > :since")
    fun findRecentActiveUsers(
        @Param("status") status: UserStatus,
        @Param("since") since: LocalDateTime,
    ): List<User>

    // LIKE with parameter
    @Query("SELECT u FROM User u WHERE u.name LIKE %:keyword%")
    fun searchByName(@Param("keyword") keyword: String): List<User>

    // IN clause
    @Query("SELECT u FROM User u WHERE u.id IN :ids")
    fun findByIds(@Param("ids") ids: Collection<Long>): List<User>
}
```

### JOIN Queries

```kotlin
@Entity
class Order(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    val user: User,

    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    val items: List<OrderItem> = emptyList(),
)

interface OrderRepository : JpaRepository<Order, Long> {

    // JOIN - returns only orders
    @Query("SELECT o FROM Order o JOIN o.user u WHERE u.status = :status")
    fun findByUserStatus(@Param("status") status: UserStatus): List<Order>

    // JOIN FETCH - eagerly loads association (prevents N+1)
    @Query("SELECT o FROM Order o JOIN FETCH o.user WHERE o.id = :id")
    fun findByIdWithUser(@Param("id") id: Long): Order?

    // Multiple JOIN FETCH
    @Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.user JOIN FETCH o.items WHERE o.id = :id")
    fun findByIdWithUserAndItems(@Param("id") id: Long): Order?

    // LEFT JOIN - includes orders without items
    @Query("SELECT o FROM Order o LEFT JOIN o.items i WHERE o.user.id = :userId")
    fun findByUserIdWithItems(@Param("userId") userId: Long): List<Order>
}
```

### Aggregation

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {

    @Query("SELECT COUNT(o) FROM Order o WHERE o.user.id = :userId")
    fun countByUserId(@Param("userId") userId: Long): Long

    @Query("SELECT SUM(o.totalAmount) FROM Order o WHERE o.user.id = :userId")
    fun sumTotalAmountByUserId(@Param("userId") userId: Long): BigDecimal?

    @Query("SELECT AVG(o.totalAmount) FROM Order o WHERE o.status = :status")
    fun avgTotalAmountByStatus(@Param("status") status: OrderStatus): Double?

    @Query("SELECT MAX(o.createdAt) FROM Order o WHERE o.user.id = :userId")
    fun findLastOrderDate(@Param("userId") userId: Long): LocalDateTime?
}
```

### GROUP BY

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {

    // Group by with projection
    @Query("""
        SELECT o.status as status, COUNT(o) as count, SUM(o.totalAmount) as total
        FROM Order o
        GROUP BY o.status
    """)
    fun getOrderStatsByStatus(): List<OrderStatusStats>

    // Group by date
    @Query("""
        SELECT FUNCTION('DATE', o.createdAt) as date, COUNT(o) as count
        FROM Order o
        WHERE o.createdAt >= :since
        GROUP BY FUNCTION('DATE', o.createdAt)
        ORDER BY date DESC
    """)
    fun getDailyOrderCounts(@Param("since") since: LocalDateTime): List<DailyCount>
}

// Projection interface
interface OrderStatusStats {
    fun getStatus(): OrderStatus
    fun getCount(): Long
    fun getTotal(): BigDecimal
}

interface DailyCount {
    fun getDate(): LocalDate
    fun getCount(): Long
}
```

### Subqueries

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    // Users with orders
    @Query("""
        SELECT u FROM User u
        WHERE EXISTS (SELECT 1 FROM Order o WHERE o.user = u)
    """)
    fun findUsersWithOrders(): List<User>

    // Users with order count > N
    @Query("""
        SELECT u FROM User u
        WHERE (SELECT COUNT(o) FROM Order o WHERE o.user = u) > :minOrders
    """)
    fun findUsersWithMinOrders(@Param("minOrders") minOrders: Long): List<User>

    // Users with max order amount
    @Query("""
        SELECT u FROM User u
        WHERE u.id IN (
            SELECT o.user.id FROM Order o
            WHERE o.totalAmount = (SELECT MAX(o2.totalAmount) FROM Order o2)
        )
    """)
    fun findUsersWithMaxOrderAmount(): List<User>
}
```

## Projections

Return only needed fields instead of full entities.

### Interface Projection

```kotlin
// Projection interface
interface UserSummary {
    fun getId(): Long
    fun getName(): String
    fun getEmail(): String
}

interface UserRepository : JpaRepository<User, Long> {

    fun findByStatus(status: UserStatus): List<UserSummary>

    @Query("SELECT u.id as id, u.name as name, u.email as email FROM User u WHERE u.status = :status")
    fun findSummaryByStatus(@Param("status") status: UserStatus): List<UserSummary>
}
```

### DTO Projection

```kotlin
data class UserDto(
    val id: Long,
    val name: String,
    val email: String,
)

interface UserRepository : JpaRepository<User, Long> {

    @Query("""
        SELECT new com.example.dto.UserDto(u.id, u.name, u.email)
        FROM User u
        WHERE u.status = :status
    """)
    fun findDtoByStatus(@Param("status") status: UserStatus): List<UserDto>
}
```

### Tuple Projection

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {

    @Query("""
        SELECT u.name, COUNT(o), SUM(o.totalAmount)
        FROM Order o JOIN o.user u
        GROUP BY u.id, u.name
    """)
    fun getUserOrderStats(): List<Array<Any>>
}

// Usage
val stats = orderRepository.getUserOrderStats()
stats.forEach { row ->
    val name = row[0] as String
    val count = row[1] as Long
    val total = row[2] as BigDecimal
}
```

## Modifying Queries

### Update

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    fun updateStatus(@Param("id") id: Long, @Param("status") status: UserStatus): Int

    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.lastLoginAt < :before")
    fun deactivateInactiveUsers(
        @Param("status") status: UserStatus,
        @Param("before") before: LocalDateTime,
    ): Int

    @Modifying(clearAutomatically = true)  // Clear persistence context after update
    @Query("UPDATE User u SET u.name = :name WHERE u.id = :id")
    fun updateName(@Param("id") id: Long, @Param("name") name: String): Int
}
```

### Delete

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    @Modifying
    @Query("DELETE FROM User u WHERE u.status = :status")
    fun deleteByStatus(@Param("status") status: UserStatus): Int

    // Soft delete
    @Modifying
    @Query("UPDATE User u SET u.deletedAt = :now WHERE u.id = :id")
    fun softDelete(@Param("id") id: Long, @Param("now") now: LocalDateTime): Int
}
```

> **Note:** `@Modifying` queries bypass entity lifecycle - no events, no @Version update, no cache sync.

## Native Queries

Use when JPQL can't express the query (database-specific features).

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    @Query(
        value = "SELECT * FROM users WHERE email ILIKE :pattern",
        nativeQuery = true,
    )
    fun findByEmailPattern(@Param("pattern") pattern: String): List<User>

    @Query(
        value = """
            SELECT u.*, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            HAVING COUNT(o.id) >= :minOrders
        """,
        nativeQuery = true,
    )
    fun findUsersWithMinOrdersNative(@Param("minOrders") minOrders: Int): List<User>

    // Native with pagination
    @Query(
        value = "SELECT * FROM users WHERE status = :status",
        countQuery = "SELECT COUNT(*) FROM users WHERE status = :status",
        nativeQuery = true,
    )
    fun findByStatusNative(@Param("status") String: status, pageable: Pageable): Page<User>
}
```

## Custom Repository

For complex queries that need EntityManager.

```kotlin
// Custom interface
interface UserRepositoryCustom {
    fun findByComplexCriteria(criteria: UserSearchCriteria): List<User>
}

// Implementation (must end with "Impl")
class UserRepositoryImpl(
    private val entityManager: EntityManager,
) : UserRepositoryCustom {

    override fun findByComplexCriteria(criteria: UserSearchCriteria): List<User> {
        val cb = entityManager.criteriaBuilder
        val query = cb.createQuery(User::class.java)
        val root = query.from(User::class.java)

        val predicates = mutableListOf<Predicate>()

        criteria.name?.let {
            predicates.add(cb.like(cb.lower(root.get("name")), "%${it.lowercase()}%"))
        }

        criteria.status?.let {
            predicates.add(cb.equal(root.get<UserStatus>("status"), it))
        }

        criteria.createdAfter?.let {
            predicates.add(cb.greaterThan(root.get("createdAt"), it))
        }

        query.where(*predicates.toTypedArray())
        query.orderBy(cb.desc(root.get<LocalDateTime>("createdAt")))

        return entityManager.createQuery(query)
            .setMaxResults(criteria.limit)
            .resultList
    }
}

// Extend both interfaces
interface UserRepository : JpaRepository<User, Long>, UserRepositoryCustom {
    // ... other methods
}
```

## Query Hints & Performance

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    // Read-only hint (skip dirty checking)
    @QueryHints(QueryHint(name = "org.hibernate.readOnly", value = "true"))
    @Query("SELECT u FROM User u WHERE u.status = :status")
    fun findByStatusReadOnly(@Param("status") status: UserStatus): List<User>

    // Fetch size hint
    @QueryHints(QueryHint(name = "org.hibernate.fetchSize", value = "50"))
    @Query("SELECT u FROM User u")
    fun findAllWithFetchSize(): List<User>

    // Comment hint (for debugging in DB logs)
    @QueryHints(QueryHint(name = "org.hibernate.comment", value = "Find active users for daily report"))
    @Query("SELECT u FROM User u WHERE u.status = 'ACTIVE'")
    fun findActiveUsersForReport(): List<User>
}
```

## Common Patterns

> For Soft Delete, Auditing, Specification, and EntityGraph patterns, see [jpa.md](jpa.md).
