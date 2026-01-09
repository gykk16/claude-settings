# Aspect-Oriented Programming (AOP)

## When to Use AOP

AOP addresses cross-cutting concerns that span multiple layers:

- **Logging** - Log method entry, exit, and exceptions
- **Security** - Check permissions before method execution
- **Transactions** - Manage database transactions declaratively
- **Caching** - Cache method results automatically
- **Performance Monitoring** - Measure execution time

## Core Concepts

| Term | Description |
|------|-------------|
| **Aspect** | A class containing advice and pointcut definitions |
| **Advice** | Code executed at a specific point |
| **Pointcut** | Expression matching where advice should apply |
| **JoinPoint** | Actual point in code where advice executes |

## Advice Types

| Type | When It Runs | Use Case |
|------|--------------|----------|
| `@Before` | Before method execution | Validation, authentication |
| `@After` | After method completes (always) | Cleanup |
| `@AfterReturning` | After successful return | Log success |
| `@AfterThrowing` | After exception thrown | Error handling |
| `@Around` | Before and after execution | Timing, caching |

## Pointcut Expressions

```kotlin
// Match all methods in a package
@Pointcut("execution(* com.example.service.*.*(..))")

// Match by annotation
@Pointcut("@annotation(com.example.Tracked)")

// Match specific method names
@Pointcut("execution(* get*(..))")

// Combine conditions
@Pointcut("execution(* com.example.service.*.*(..)) && @annotation(com.example.Async)")
```

## Practical Examples

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

### Performance Monitoring Aspect

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

### Custom Annotation-Based Aspect

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

## Common Pitfalls

### Self-Invocation

Aspects don't apply when a method calls another method on the same object:

```kotlin
@Service
class MyService {

    @Timed
    fun trackedMethod() { }

    fun caller() {
        trackedMethod()  // Aspect NOT applied - calling within same object
    }
}
```

**Solution:** Inject the service and call through the proxy, or refactor into separate beans.

### Proxy Limitations

- AOP only applies to **public methods** called through Spring proxy
- **Private methods** cannot be advised
- **Constructor calls** are not intercepted
- **Static methods** cannot be advised
