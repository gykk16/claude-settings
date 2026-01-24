# Repository Layer

Repository layer handles data access using Spring Data JPA.

For JPA entity mapping, fetch strategies, and locking, see [jpa.md](jpa.md).

## When to Use Which Query Method

| Complexity | Approach | Example |
|------------|----------|---------|
| Simple | Query methods | `findByEmail(email)` |
| Multiple conditions | Query methods | `findByNameAndStatus(name, status)` |
| Joins, aggregations | JPQL `@Query` | `SELECT u FROM User u JOIN u.orders` |
| Partial results | Projections | Interface or DTO projection |
| DB-specific features | Native SQL | `@Query(nativeQuery = true)` |
| Dynamic criteria | Specification | `JpaSpecificationExecutor` |

## Key Principles

> **Keep queries simple.** Query methods first, JPQL for complex cases, native SQL as last resort.

| Guideline | Description |
|-----------|-------------|
| **Interface-based** | Extend `JpaRepository`, no implementation needed |
| **Query methods first** | Use method naming conventions for simple queries |
| **JPQL for complex** | Use `@Query` for joins, aggregations, projections |
| **Native SQL last resort** | Only when JPQL can't express the query |

## Query Methods

Spring Data JPA generates queries from method names.

### Naming Conventions

| Keyword | Example | SQL Equivalent |
|---------|---------|----------------|
| `findBy` | `findByEmail(email)` | `WHERE email = ?` |
| `And` | `findByNameAndStatus(n, s)` | `WHERE name = ? AND status = ?` |
| `Or` | `findByNameOrEmail(n, e)` | `WHERE name = ? OR email = ?` |
| `Between` | `findByAgeBetween(a, b)` | `WHERE age BETWEEN ? AND ?` |
| `LessThan` | `findByAgeLessThan(a)` | `WHERE age < ?` |
| `GreaterThan` | `findByAgeGreaterThan(a)` | `WHERE age > ?` |
| `IsNull` | `findByDeletedAtIsNull()` | `WHERE deleted_at IS NULL` |
| `Containing` | `findByNameContaining(s)` | `WHERE name LIKE %?%` |
| `In` | `findByStatusIn(list)` | `WHERE status IN (?, ?)` |
| `OrderBy` | `findByStatusOrderByCreatedAtDesc()` | `ORDER BY created_at DESC` |
| `First`, `Top` | `findFirstByOrderByCreatedAtDesc()` | `LIMIT 1` |

```kotlin
interface UserRepository : JpaRepository<User, Long> {
    fun findByEmail(email: String): User?
    fun findByStatus(status: UserStatus): List<User>
    fun findByNameContainingIgnoreCase(keyword: String): List<User>
    fun existsByEmail(email: String): Boolean
    fun countByStatus(status: UserStatus): Long
}
```

## Pagination

| Type | When to Use | Total Count |
|------|-------------|-------------|
| `Page<T>` | Pagination UI needs total | Yes (extra query) |
| `Slice<T>` | Infinite scroll, "Load more" | No |
| `List<T>` | Simple list, no pagination info | No |

```kotlin
interface UserRepository : JpaRepository<User, Long> {
    fun findByStatus(status: UserStatus, pageable: Pageable): Page<User>
    fun findSliceByStatus(status: UserStatus, pageable: Pageable): Slice<User>
}

// Usage
val pageable = PageRequest.of(page, size, Sort.by("createdAt").descending())
val result = userRepository.findByStatus(UserStatus.ACTIVE, pageable)
```

## JPQL Queries

Use `@Query` when query methods become too complex.

### When to Use JPQL

- JOIN queries
- Aggregations (COUNT, SUM, AVG)
- GROUP BY
- Subqueries
- Complex conditions

```kotlin
interface OrderRepository : JpaRepository<Order, Long> {

    // JOIN FETCH - prevents N+1
    @Query("SELECT o FROM Order o JOIN FETCH o.user WHERE o.id = :id")
    fun findByIdWithUser(@Param("id") id: Long): Order?

    // Aggregation
    @Query("SELECT SUM(o.totalAmount) FROM Order o WHERE o.user.id = :userId")
    fun sumTotalByUserId(@Param("userId") userId: Long): BigDecimal?

    // GROUP BY with projection
    @Query("""
        SELECT o.status as status, COUNT(o) as count
        FROM Order o GROUP BY o.status
    """)
    fun countByStatus(): List<StatusCount>
}

interface StatusCount {
    fun getStatus(): OrderStatus
    fun getCount(): Long
}
```

## Projections

Return only needed fields instead of full entities.

| Type | Use Case | Example |
|------|----------|---------|
| Interface projection | Simple field subset | `interface UserSummary { fun getName(): String }` |
| DTO projection | Complex mapping | `SELECT new com.example.UserDto(u.id, u.name) FROM User u` |

```kotlin
// Interface projection
interface UserSummary {
    fun getId(): Long
    fun getName(): String
}

interface UserRepository : JpaRepository<User, Long> {
    fun findByStatus(status: UserStatus): List<UserSummary>
}
```

## Modifying Queries

```kotlin
interface UserRepository : JpaRepository<User, Long> {

    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.lastLoginAt < :before")
    fun deactivateInactive(
        @Param("status") status: UserStatus,
        @Param("before") before: LocalDateTime,
    ): Int

    @Modifying(clearAutomatically = true)  // Clear persistence context after
    @Query("DELETE FROM User u WHERE u.status = :status")
    fun deleteByStatus(@Param("status") status: UserStatus): Int
}
```

> **Warning:** `@Modifying` queries bypass entity lifecycle - no `@Version` update, no cache sync.

## Native Queries

Use when JPQL can't express the query (DB-specific features):

```kotlin
@Query(
    value = "SELECT * FROM users WHERE email ILIKE :pattern",
    nativeQuery = true,
)
fun findByEmailPattern(@Param("pattern") pattern: String): List<User>

// With pagination
@Query(
    value = "SELECT * FROM users WHERE status = :status",
    countQuery = "SELECT COUNT(*) FROM users WHERE status = :status",
    nativeQuery = true,
)
fun findByStatusNative(@Param("status") status: String, pageable: Pageable): Page<User>
```

## Query Hints

```kotlin
// Read-only (skip dirty checking)
@QueryHints(QueryHint(name = "org.hibernate.readOnly", value = "true"))
@Query("SELECT u FROM User u WHERE u.status = :status")
fun findByStatusReadOnly(@Param("status") status: UserStatus): List<User>
```

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| N+1 queries | 1 + N queries for lazy associations | Use `JOIN FETCH` or `@EntityGraph` |
| Missing pagination | Loading all data into memory | Always paginate large result sets |
| Query methods too complex | Unreadable method names | Switch to JPQL `@Query` |
| `@Modifying` without `clearAutomatically` | Stale data in persistence context | Use `@Modifying(clearAutomatically = true)` |
| Native SQL everywhere | Not portable, bypasses JPA features | Prefer JPQL, use native SQL only when necessary |
