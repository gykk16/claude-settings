# Aspect-Oriented Programming (AOP)

AOP addresses cross-cutting concerns that span multiple layers.

## When to Use AOP

| Use Case | Description |
|----------|-------------|
| **Logging** | Method entry, exit, exceptions |
| **Security** | Permission checks before execution |
| **Transactions** | Declarative transaction management |
| **Caching** | Automatic result caching |
| **Performance** | Execution time measurement |

---

## Core Concepts

| Term | Description |
|------|-------------|
| **Aspect** | Class containing advice and pointcut definitions |
| **Advice** | Code executed at a specific point |
| **Pointcut** | Expression matching where advice should apply |
| **JoinPoint** | Actual point in code where advice executes |

---

## Advice Types

| Type | When It Runs | Use Case |
|------|--------------|----------|
| `@Before` | Before method execution | Validation, authentication |
| `@After` | After method completes (always) | Cleanup |
| `@AfterReturning` | After successful return | Log success |
| `@AfterThrowing` | After exception thrown | Error handling |
| `@Around` | Before and after execution | Timing, caching, full control |

---

## Pointcut Expressions

| Pattern | Description |
|---------|-------------|
| `execution(* com.example.service.*.*(..))` | All methods in package |
| `@annotation(com.example.Tracked)` | Methods with annotation |
| `execution(* get*(..))` | Methods starting with "get" |
| `within(com.example.service.*)` | All methods within package |

---

## Common Patterns

### Logging Aspect

```kotlin
@Aspect
@Component
class LoggingAspect {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Before("execution(* com.example.service.*.*(..))")
    fun logBefore(joinPoint: JoinPoint) {
        logger.info("Executing: {}", joinPoint.signature.name)
    }

    @AfterThrowing("execution(* com.example.service.*.*(..))", throwing = "ex")
    fun logException(joinPoint: JoinPoint, ex: Exception) {
        logger.error("Exception in {}: {}", joinPoint.signature.name, ex.message)
    }
}
```

### Performance Monitoring

```kotlin
@Aspect
@Component
class PerformanceAspect {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Around("execution(* com.example.service.*.*(..))")
    fun monitorPerformance(joinPoint: ProceedingJoinPoint): Any? {
        val startTime = System.currentTimeMillis()
        return try {
            joinPoint.proceed()
        } finally {
            val duration = System.currentTimeMillis() - startTime
            logger.info("{} took {}ms", joinPoint.signature.name, duration)
        }
    }
}
```

### Custom Annotation Aspect

```kotlin
@Target(AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
annotation class Timed

@Aspect
@Component
class TimedAspect {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Around("@annotation(com.example.Timed)")
    fun timeMethod(joinPoint: ProceedingJoinPoint): Any? {
        val start = System.nanoTime()
        return try {
            joinPoint.proceed()
        } finally {
            val durationMs = (System.nanoTime() - start) / 1_000_000
            logger.info("{} executed in {}ms", joinPoint.signature.name, durationMs)
        }
    }
}

// Usage
@Service
class OrderService {
    @Timed
    fun processOrder(orderId: Long) { }
}
```

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Self-invocation | Aspect not applied for internal calls | Call through proxy or extract to separate bean |
| Private methods | Cannot be advised | Use public methods |
| Constructor calls | Not intercepted | Use `@PostConstruct` or factory methods |
| Static methods | Cannot be advised | Convert to instance methods |
| Final classes/methods | Cannot be proxied (CGLIB) | Remove `final` or use interface-based proxy |
