# Dependency Injection

Dependency Injection (DI) in Spring Boot with Kotlin enables loose coupling and testability. Constructor injection is the recommended approach for required dependencies.

## Constructor Injection

The primary pattern for mandatory dependencies. Makes dependencies explicit and enables immutability.

```kotlin
@Service
class UserService(
    private val userRepository: UserRepository,
    private val emailService: EmailService,
) {
    fun createUser(name: String): User {
        val user = User(name = name)
        return userRepository.save(user)
    }
}
```

### Why Constructor Injection?

- **Immutability**: Dependencies are final, thread-safe
- **Testability**: Easy to pass mock objects
- **Required Dependencies**: Fails at application startup if missing
- **Clarity**: Dependencies visible in the constructor signature

## Optional Dependencies

Use nullable types for optional dependencies.

```kotlin
@Service
class ReportService(
    private val reportRepository: ReportRepository,
    private val analyticsService: AnalyticsService?,
) {
    fun generateReport(): Report {
        val report = reportRepository.findLatest()
        analyticsService?.track("report_generated")
        return report
    }
}
```

## Circular Dependencies

Avoid circular dependencies through proper application design. Use `@Lazy` only as a last resort.

```kotlin
@Service
class ServiceA(
    @Lazy private val serviceB: ServiceB,
) {
    // serviceB is lazily initialized on first use
}
```

**Prevention strategies:**
- Extract shared logic into a separate service
- Use event-driven architecture
- Refactor to eliminate coupling

## @Qualifier and @Primary

Use when multiple beans of the same type exist.

```kotlin
@Configuration
class DataSourceConfig {
    @Bean
    @Primary
    fun primaryDataSource(): DataSource = HikariDataSource()

    @Bean("secondaryDataSource")
    fun secondaryDataSource(): DataSource = HikariDataSource()
}

@Service
class DatabaseService(
    @Qualifier("secondaryDataSource")
    private val dataSource: DataSource,
)
```

## Configuration Injection

### @ConfigurationProperties (Typed, Preferred)

```kotlin
@ConfigurationProperties(prefix = "app.mail")
data class MailProperties(
    val host: String = "",
    val port: Int = 25,
    val username: String = "",
)

@Service
class MailService(
    private val mailProperties: MailProperties,
) {
    fun sendEmail(to: String) {
        // Use mailProperties.host, mailProperties.port
    }
}
```

### @Value (Simple, String-based)

```kotlin
@Service
class ConfigService(
    @Value("\${app.name}") private val appName: String,
    @Value("\${app.version}") private val appVersion: String,
)
```

## Testing with DI

```kotlin
@SpringBootTest
class UserServiceTest {

    @MockBean
    private lateinit var userRepository: UserRepository

    @SpyBean
    private lateinit var emailService: EmailService

    @Autowired
    private lateinit var userService: UserService

    @Test
    fun `should create user`() {
        whenever(userRepository.save(any())).thenReturn(User(1, "John"))

        val user = userService.createUser("John")

        verify(emailService).sendWelcomeEmail("John")
        assertThat(user.name).isEqualTo("John")
    }
}
```

- **@MockBean**: Replaces bean with mock (Mockito)
- **@SpyBean**: Wraps real bean, allows partial mocking
- **@Autowired**: Injects actual or mocked beans into test class
