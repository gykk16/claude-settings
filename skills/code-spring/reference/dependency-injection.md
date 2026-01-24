# Dependency Injection

Dependency Injection (DI) in Spring Boot with Kotlin enables loose coupling and testability.

## Injection Types

| Type | Use Case | Recommendation |
|------|----------|----------------|
| **Constructor** | Required dependencies | **Recommended** |
| **Setter** | Optional dependencies | Avoid |
| **Field** | Legacy or tests | Avoid in production code |

---

## Constructor Injection (Recommended)

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val emailService: EmailService,
) {
    fun createUser(name: String): User = userRepository.save(User(name = name))
}
```

**Why Constructor Injection?**

| Benefit | Description |
|---------|-------------|
| **Immutability** | Dependencies are final, thread-safe |
| **Testability** | Easy to pass mock objects |
| **Required dependencies** | Fails at startup if missing |
| **Clarity** | Dependencies visible in constructor |

---

## Optional Dependencies

Use nullable types:

```kotlin
@Service
class ReportService(
    private val reportRepository: ReportRepository,
    private val analyticsService: AnalyticsService?,  // Optional
) {
    fun generateReport(): Report {
        val report = reportRepository.findLatest()
        analyticsService?.track("report_generated")
        return report
    }
}
```

---

## Multiple Beans of Same Type

### @Primary

```kotlin
@Configuration
class DataSourceConfig {
    @Bean
    @Primary
    fun primaryDataSource(): DataSource = HikariDataSource()

    @Bean("secondaryDataSource")
    fun secondaryDataSource(): DataSource = HikariDataSource()
}
```

### @Qualifier

```kotlin
@Service
class DatabaseService(
    @Qualifier("secondaryDataSource")
    private val dataSource: DataSource,
)
```

---

## Configuration Injection

### @ConfigurationProperties (Preferred)

```kotlin
@ConfigurationProperties(prefix = "app.mail")
data class MailProperties(
    val host: String = "",
    val port: Int = 25,
    val username: String = "",
)

@Service
class MailService(private val mailProperties: MailProperties) {
    fun sendEmail(to: String) {
        // Use mailProperties.host, mailProperties.port
    }
}
```

### @Value (Simple values)

```kotlin
@Service
class ConfigService(
    @Value("\${app.name}") private val appName: String,
    @Value("\${app.version}") private val appVersion: String,
)
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Circular dependencies | Application startup failure | Refactor, use `@Lazy`, or event-driven design |
| Field injection | Harder to test, hidden dependencies | Use constructor injection |
| Too many dependencies | Class doing too much | Split into smaller services |
| Missing `@Configuration` | Properties class not bound | Add `@EnableConfigurationProperties` |

### Circular Dependencies

**Prevention strategies:**
1. Extract shared logic to separate service
2. Use event-driven architecture
3. Use `@Lazy` as last resort

```kotlin
@Service
class ServiceA(@Lazy private val serviceB: ServiceB) { }
```

---

## Testing

| Annotation | Description |
|------------|-------------|
| `@MockBean` | Replace bean with mock |
| `@SpyBean` | Wrap real bean for partial mocking |
| `@Autowired` | Inject actual or mocked beans |

```kotlin
@SpringBootTest
class UserServiceTest {
    @MockBean lateinit var userRepository: UserRepository
    @Autowired lateinit var userService: UserService

    @Test
    fun `should create user`() {
        whenever(userRepository.save(any())).thenReturn(User(1, "John"))

        val user = userService.createUser("John")

        assertEquals("John", user.name)
    }
}
```
