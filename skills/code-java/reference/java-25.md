# Java 25 Features & Best Practices

**Release Date:** September 16, 2025
**LTS Status:** Long-Term Support

## Key Features

### Module Import Declarations (JEP 511) - Finalized
```java
// Before: verbose imports
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

// Java 25: module import
import module java.base;

// Now all java.base exports are available
List<String> list = List.of("a", "b", "c");
Set<Integer> set = Set.of(1, 2, 3);
Stream<String> stream = list.stream();
```

### Compact Source Files and Instance Main Methods (JEP 512) - Finalized
```java
// Traditional main method
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// Java 25: instance main method
void main() {
    println("Hello, World!");
}

// Or even simpler for scripts
void main() {
    var name = "Java";
    println("Hello, " + name + "!");
}

// Access to command-line arguments
void main(String[] args) {
    if (args.length > 0) {
        println("Hello, " + args[0]);
    }
}
```

### Flexible Constructor Bodies (JEP 513) - Finalized
```java
// Before: must call super() or this() first
public class User {
    private final String name;
    private final String email;

    public User(String name, String email) {
        // Can't do validation before super()
        super();
        if (name == null) throw new IllegalArgumentException();
        this.name = name;
        this.email = email;
    }
}

// Java 25: statements before super()
public class User {
    private final String name;
    private final String email;

    public User(String name, String email) {
        // Validation before super()
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name required");
        }

        // Normalize data
        name = name.trim().toLowerCase();

        super();
        this.name = name;
        this.email = email;
    }
}

// Complex initialization
public class ValidatedUser extends BaseUser {
    private final String username;

    public ValidatedUser(String username, UserRepository repo) {
        // Check uniqueness before construction
        if (repo.exists(username)) {
            throw new IllegalArgumentException("Username taken");
        }

        // Call parent constructor
        super(username);
        this.username = username;
    }
}
```

### Primitive Types in Patterns (JEP 507) - Third Preview
```java
// Pattern matching with primitives
Object obj = 42;

// Before: manual type checking
if (obj instanceof Integer) {
    int i = ((Integer) obj).intValue();
    if (i > 0) {
        process(i);
    }
}

// Java 25: primitive patterns
if (obj instanceof int i && i > 0) {
    process(i);
}

// Switch with primitive patterns
String describe(Object obj) {
    return switch (obj) {
        case int i when i > 0 -> "positive integer: " + i;
        case int i when i < 0 -> "negative integer: " + i;
        case int i -> "zero";
        case double d when d > 0.0 -> "positive double";
        case double d -> "non-positive double";
        case null -> "null";
        default -> "other type";
    };
}

// Narrowing conversions
void processNumber(Object obj) {
    switch (obj) {
        case long l when l <= Integer.MAX_VALUE -> {
            int i = (int) l;  // Safe narrowing
            processInt(i);
        }
        case double d when d == (float) d -> {
            float f = (float) d;  // Safe narrowing
            processFloat(f);
        }
        default -> processObject(obj);
    }
}
```

### Scoped Values (JEP 506) - Finalized
```java
// Alternative to ThreadLocal for sharing immutable data
public class UserContext {
    private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

    // Share user across call stack
    public static void runWithUser(User user, Runnable action) {
        ScopedValue.where(CURRENT_USER, user).run(action);
    }

    public static User getCurrentUser() {
        return CURRENT_USER.get();
    }
}

// Usage
UserContext.runWithUser(authenticatedUser, () -> {
    // User available in entire call stack
    processRequest();
    // user automatically "unbound" after
});

// Nested scopes
ScopedValue.where(REQUEST_ID, "123")
    .where(USER, user)
    .run(() -> {
        // Both REQUEST_ID and USER available
        handleRequest();
    });

// Better than ThreadLocal:
// - Immutable by design
// - No memory leaks
// - Better with virtual threads
// - Explicit scope boundaries
```

### Structured Concurrency (JEP 505) - Fifth Preview
```java
// Better concurrent programming
record UserData(User user, List<Order> orders, List<Address> addresses) {}

UserData fetchUserData(Long userId) throws InterruptedException, ExecutionException {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        // Fork multiple tasks
        var userTask = scope.fork(() -> userService.fetch(userId));
        var ordersTask = scope.fork(() -> orderService.fetchByUser(userId));
        var addressesTask = scope.fork(() -> addressService.fetchByUser(userId));

        // Wait for all to complete (or first failure)
        scope.join();
        scope.throwIfFailed();

        // All succeeded, get results
        return new UserData(
            userTask.get(),
            ordersTask.get(),
            addressesTask.get()
        );
    }
}

// Shutdown on success (first successful result)
String fetchFromMultipleSources(String query) throws InterruptedException {
    try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
        // Try multiple sources
        scope.fork(() -> source1.fetch(query));
        scope.fork(() -> source2.fetch(query));
        scope.fork(() -> source3.fetch(query));

        // Return first successful result
        scope.join();
        return scope.result();
    }
}
```

### Compact Object Headers (JEP 519) - Finalized
```java
// Automatic memory optimization - no code changes needed
// Reduces object header overhead from 12-16 bytes to 8 bytes

// Before Java 25:
// Object header = 12 bytes (compressed) or 16 bytes (uncompressed)

// Java 25:
// Object header = 8 bytes (always)

// Benefits:
// - Smaller memory footprint
// - Better cache utilization
// - Improved GC performance
// - More objects fit in same memory

// Example impact
class Point {
    private int x;  // 4 bytes
    private int y;  // 4 bytes
}

// Memory per instance:
// Java 21: 12 (header) + 8 (fields) + 4 (padding) = 24 bytes
// Java 25: 8 (header) + 8 (fields) = 16 bytes
// Savings: 33% memory reduction!
```

### Key Derivation Function API (JEP 510) - Finalized
```java
// Standardized password hashing and key derivation
import java.security.spec.KeyDerivationFunction;
import java.security.spec.KeyDerivationSpec;

// PBKDF2 (Password-Based Key Derivation)
KeyDerivationFunction kdf = KeyDerivationFunction.getInstance("PBKDF2WithHmacSHA256");

KeyDerivationSpec spec = KeyDerivationSpec.PBKDF2(
    password.toCharArray(),
    salt,
    100_000,  // iterations
    256       // key length in bits
);

byte[] derivedKey = kdf.deriveKey(spec);

// Argon2 (modern alternative)
KeyDerivationFunction argon2 = KeyDerivationFunction.getInstance("Argon2id");

KeyDerivationSpec argon2Spec = KeyDerivationSpec.Argon2(
    password.toCharArray(),
    salt,
    3,        // iterations
    65536,    // memory cost (64 MB)
    4         // parallelism
);

byte[] secureKey = argon2.deriveKey(argon2Spec);

// Use in password storage
public class SecurePasswordStorage {
    private static final KeyDerivationFunction KDF =
        KeyDerivationFunction.getInstance("Argon2id");

    public String hashPassword(String password) {
        byte[] salt = generateRandomSalt(16);
        byte[] hash = KDF.deriveKey(
            KeyDerivationSpec.Argon2(password.toCharArray(), salt, 3, 65536, 4)
        );
        return Base64.getEncoder().encodeToString(salt) + ":" +
               Base64.getEncoder().encodeToString(hash);
    }

    public boolean verifyPassword(String password, String stored) {
        String[] parts = stored.split(":");
        byte[] salt = Base64.getDecoder().decode(parts[0]);
        byte[] expectedHash = Base64.getDecoder().decode(parts[1]);

        byte[] actualHash = KDF.deriveKey(
            KeyDerivationSpec.Argon2(password.toCharArray(), salt, 3, 65536, 4)
        );

        return MessageDigest.isEqual(expectedHash, actualHash);
    }
}
```

## Best Practices

### Module Import Declarations
```java
// Good: use for quick scripts and small programs
import module java.base;

void main() {
    var list = List.of(1, 2, 3);
    println(list);
}

// Production code: explicit imports for clarity
import java.util.List;
import java.util.stream.Collectors;

public class ProductionService {
    public List<String> process(List<String> input) {
        return input.stream()
            .filter(s -> !s.isBlank())
            .collect(Collectors.toList());
    }
}
```

### Instance Main Methods
```java
// Perfect for:
// - Quick scripts
// - Learning examples
// - Command-line tools

// Quick script
void main(String[] args) {
    if (args.length == 0) {
        println("Usage: program <name>");
        return;
    }
    println("Hello, " + args[0]);
}

// Production applications: stick with traditional main
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Scoped Values vs ThreadLocal
```java
// Use Scoped Values (Java 25+)
private static final ScopedValue<RequestContext> REQUEST = ScopedValue.newInstance();

void handleRequest(RequestContext ctx) {
    ScopedValue.where(REQUEST, ctx).run(() -> {
        processRequest();
    });
}

// Avoid ThreadLocal for new code
// Only use ThreadLocal for backward compatibility
```

### Structured Concurrency
```java
// Use for coordinated concurrent tasks
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var task1 = scope.fork(() -> operation1());
    var task2 = scope.fork(() -> operation2());

    scope.join();
    scope.throwIfFailed();

    return combine(task1.get(), task2.get());
}

// Benefits:
// - Automatic cleanup
// - Clear error handling
// - No leaked threads
// - Cancellation propagation
```

## Migration from Java 21

### Adopt New Features Gradually
```java
// 1. Start with instance main methods for scripts
// Before
public class Script {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}

// After
void main() {
    println("Hello");
}

// 2. Replace ThreadLocal with Scoped Values
// Before
private static final ThreadLocal<User> currentUser = new ThreadLocal<>();

// After
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// 3. Use Structured Concurrency for parallel tasks
// Before
CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> fetchUser());
CompletableFuture<Orders> ordersFuture = CompletableFuture.supplyAsync(() -> fetchOrders());
CompletableFuture.allOf(userFuture, ordersFuture).join();

// After
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var user = scope.fork(() -> fetchUser());
    var orders = scope.fork(() -> fetchOrders());
    scope.join().throwIfFailed();
    process(user.get(), orders.get());
}
```

### Use Flexible Constructor Bodies
```java
// Before: workarounds for validation
public class User extends Entity {
    private final String name;

    public User(String name) {
        super();
        this.name = validate(name);
    }

    private static String validate(String name) {
        if (name == null) throw new IllegalArgumentException();
        return name.trim();
    }
}

// After: direct validation
public class User extends Entity {
    private final String name;

    public User(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name required");
        }
        name = name.trim();
        super();
        this.name = name;
    }
}
```

## Common Pitfalls

### Module Import Over-Use
```java
// Bad: module import in production code
import module java.base;
import module java.sql;

public class ProductionService {
    // Too broad, unclear dependencies
}

// Good: explicit imports
import java.util.List;
import java.sql.Connection;
import java.sql.PreparedStatement;

public class ProductionService {
    // Clear dependencies
}
```

### Scoped Values Mutability
```java
// Bad: trying to mutate scoped value
private static final ScopedValue<List<String>> DATA = ScopedValue.newInstance();

void process() {
    ScopedValue.where(DATA, new ArrayList<>()).run(() -> {
        DATA.get().add("item");  // Mutating shared state - BAD!
    });
}

// Good: treat as immutable
private static final ScopedValue<List<String>> DATA = ScopedValue.newInstance();

void process() {
    var items = new ArrayList<String>();
    items.add("item");
    ScopedValue.where(DATA, List.copyOf(items)).run(() -> {
        // DATA is immutable
        var data = DATA.get();
    });
}
```

### Structured Concurrency Exception Handling
```java
// Bad: ignoring exceptions
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    scope.fork(() -> riskyOperation());
    scope.join();
    // Forgot to check for failures!
}

// Good: always check
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var task = scope.fork(() -> riskyOperation());
    scope.join();
    scope.throwIfFailed();  // Essential!
    return task.get();
}
```

## Performance Improvements

### Compact Object Headers
- 33% memory reduction for small objects
- Better CPU cache utilization
- Improved GC performance
- No code changes required

### Generational Shenandoah (JEP 521)
```bash
# Enable generational mode
java -XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational App.java

# Benefits:
# - Lower pause times
# - Better throughput
# - Improved young generation collection
```

### Ahead-of-Time Optimizations (JEP 514, 515)
```bash
# Generate AOT profile
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf App.java

# Run with AOT optimizations
java -XX:AOTMode=on -XX:AOTConfiguration=app.aotconf App.java

# Benefits:
# - Faster startup
# - Better peak performance
# - Reduced warmup time
```

## Summary

### Major Features ✅
- Module import declarations for simpler scripts
- Instance main methods (no public static void main!)
- Flexible constructor bodies with pre-super statements
- Scoped values (finalized alternative to ThreadLocal)
- Structured concurrency for safer parallel programming
- Primitive types in patterns (preview)
- Compact object headers (automatic memory savings)

### Best For 🎯
- Greenfield projects starting in 2025+
- Projects requiring latest language features
- Teams wanting long-term support (until ~2033)
- Applications benefiting from memory optimizations

### Migration Priority 📋
1. **High**: Scoped Values, Structured Concurrency
2. **Medium**: Instance main methods, Flexible constructors
3. **Low**: Module imports (for scripts only)
4. **Preview**: Primitive patterns (wait for finalization)

> **Remember**: Java 25 is LTS - safe for production with long-term support!
