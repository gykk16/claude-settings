# Java 21 Features & Best Practices

**Release Date:** September 2023
**LTS Status:** Long-Term Support (until September 2031)

## Key Features

### Pattern Matching for switch (Finalized)
```java
// Pattern matching with guards
String describe(Object obj) {
    return switch (obj) {
        case String s when s.isEmpty() -> "empty string";
        case String s when s.length() < 10 -> "short string: " + s;
        case String s -> "long string";
        case Integer i when i > 0 -> "positive integer";
        case Integer i when i < 0 -> "negative integer";
        case Integer i -> "zero";
        case null -> "null value";
        default -> "unknown type";
    };
}

// Record patterns in switch
record Point(int x, int y) { }

String describe(Object obj) {
    return switch (obj) {
        case Point(int x, int y) when x == y -> "diagonal point";
        case Point(int x, int y) when x == 0 -> "on y-axis";
        case Point(int x, int y) when y == 0 -> "on x-axis";
        case Point(int x, int y) -> "point at " + x + "," + y;
        case null -> "null";
        default -> "not a point";
    };
}

// Nested patterns
record ColoredPoint(Point point, String color) { }

String describe(ColoredPoint cp) {
    return switch (cp) {
        case ColoredPoint(Point(int x, int y), String color)
            when x == 0 && y == 0 -> color + " origin";
        case ColoredPoint(Point(int x, int y), String color)
            -> color + " point";
    };
}
```

### Record Patterns (Finalized)
```java
// Deconstruct records in instanceof
record Point(int x, int y) { }

if (obj instanceof Point(int x, int y)) {
    System.out.println("x: " + x + ", y: " + y);
}

// Nested record patterns
record Rectangle(Point topLeft, Point bottomRight) { }

if (obj instanceof Rectangle(Point(int x1, int y1), Point(int x2, int y2))) {
    int width = x2 - x1;
    int height = y2 - y1;
    System.out.println("Area: " + (width * height));
}

// Pattern matching in method parameters
int calculateDistance(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        return (int) Math.sqrt(x * x + y * y);
    }
    return 0;
}
```

### Virtual Threads (Project Loom)
```java
// Create virtual thread
Thread.startVirtualThread(() -> {
    System.out.println("Running in virtual thread");
});

// ExecutorService with virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> {
            // Each task runs in its own virtual thread
            processRequest();
        });
    }
}  // Auto-shutdown and wait for completion

// Convert existing code to use virtual threads
// Before: platform threads (limited by OS)
ExecutorService executor = Executors.newFixedThreadPool(100);

// After: virtual threads (millions possible)
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

### Sequenced Collections
```java
// New methods for List, Deque, LinkedHashSet, LinkedHashMap
List<String> list = List.of("a", "b", "c");

String first = list.getFirst();  // "a"
String last = list.getLast();    // "c"

List<String> reversed = list.reversed();  // ["c", "b", "a"]

// LinkedHashMap maintains insertion order
LinkedHashMap<String, Integer> map = new LinkedHashMap<>();
map.put("first", 1);
map.put("second", 2);

var firstEntry = map.firstEntry();  // first=1
var lastEntry = map.lastEntry();    // second=2

// Reverse iteration
map.reversed().forEach((k, v) ->
    System.out.println(k + ": " + v)
);
```

### String Templates (Preview)
```java
// Note: Preview feature in Java 21, use --enable-preview

// String interpolation
String name = "John";
int age = 30;

// Traditional
String message = String.format("Name: %s, Age: %d", name, age);

// String template (preview)
String message = STR."Name: \{name}, Age: \{age}";

// With expressions
String message = STR."Next year you'll be \{age + 1}";

// Multi-line with formatting
String json = STR."""
    {
        "name": "\{name}",
        "age": \{age},
        "email": "\{email}"
    }
    """;
```

### Unnamed Patterns and Variables
```java
// Unnamed patterns (don't care about value)
switch (obj) {
    case Point(int x, _) -> handleX(x);  // Don't care about y
    case ColoredPoint(_, String color) -> handleColor(color);
}

// Unnamed variables in catch blocks
try {
    riskyOperation();
} catch (Exception _) {  // Don't care about exception
    handleError();
}

// Unnamed variables in try-with-resources
try (var _ = lock.lock()) {  // Don't care about lock object
    performAction();
}
```

## Best Practices

### Virtual Threads for I/O-Bound Tasks
```java
// Perfect for I/O-bound operations
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // Handle thousands of concurrent HTTP requests
    users.forEach(user ->
        executor.submit(() -> sendEmail(user))
    );
}

// Not ideal for CPU-bound tasks
// Use regular ExecutorService with fixed thread pool
ExecutorService executor = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);
```

### Pattern Matching for Complex Conditionals
```java
// Before: multiple instanceof checks
if (obj instanceof String) {
    String s = (String) obj;
    if (s.length() > 5) {
        process(s.toUpperCase());
    }
} else if (obj instanceof Integer) {
    Integer i = (Integer) obj;
    if (i > 0) {
        process(i * 2);
    }
}

// After: pattern matching with guards
switch (obj) {
    case String s when s.length() > 5 -> process(s.toUpperCase());
    case Integer i when i > 0 -> process(i * 2);
    default -> { }
}
```

### Sequenced Collections
```java
// Use new methods for clarity
List<Order> orders = getOrders();

// Before
Order first = orders.isEmpty() ? null : orders.get(0);
Order last = orders.isEmpty() ? null : orders.get(orders.size() - 1);

// After
Order first = orders.getFirst();  // Throws if empty
Order last = orders.getLast();

// Or with isEmpty check
if (!orders.isEmpty()) {
    Order first = orders.getFirst();
    Order last = orders.getLast();
}
```

### Record Patterns for Data Processing
```java
// Process nested data structures
sealed interface Transaction permits Purchase, Refund { }
record Purchase(String item, Money amount) implements Transaction { }
record Refund(String item, Money amount) implements Transaction { }

Money processTransactions(List<Transaction> transactions) {
    return transactions.stream()
        .mapToLong(t -> switch (t) {
            case Purchase(_, Money(var amount, _)) -> amount;
            case Refund(_, Money(var amount, _)) -> -amount;
        })
        .sum();
}
```

## Migration from Java 17

### Adopt Virtual Threads
```java
// Before: ThreadPoolExecutor with limited threads
ExecutorService executor = Executors.newFixedThreadPool(100);

// After: Virtual threads for I/O operations
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// Or for single tasks
Thread.startVirtualThread(() -> handleRequest());
```

### Replace instanceof Chains
```java
// Before: multiple instanceof with casting
if (shape instanceof Circle) {
    Circle c = (Circle) shape;
    return Math.PI * c.radius() * c.radius();
} else if (shape instanceof Rectangle) {
    Rectangle r = (Rectangle) shape;
    return r.width() * r.height();
}

// After: pattern matching switch
return switch (shape) {
    case Circle(double r) -> Math.PI * r * r;
    case Rectangle(double w, double h) -> w * h;
    case Triangle t -> calculateTriangleArea(t);
};
```

### Use Sequenced Collections API
```java
// Before
Deque<String> deque = new ArrayDeque<>();
String first = deque.peek();
String last = deque.peekLast();

// After: more consistent API
SequencedCollection<String> collection = new ArrayDeque<>();
String first = collection.getFirst();
String last = collection.getLast();
```

## Common Pitfalls

### Virtual Threads and Thread-Local
```java
// Bad: ThreadLocal with virtual threads (memory leak risk)
private static ThreadLocal<User> currentUser = new ThreadLocal<>();

// Good: use scoped values (preview feature)
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

// Or pass context explicitly
void process(User user) {
    // Pass user as parameter
}
```

### Pattern Matching Completeness
```java
// Bad: missing cases
String describe(Object obj) {
    return switch (obj) {
        case String s -> "string";
        case Integer i -> "integer";
        // Missing: null, default
    };  // Compilation error!
}

// Good: handle all cases
String describe(Object obj) {
    return switch (obj) {
        case String s -> "string";
        case Integer i -> "integer";
        case null -> "null";
        default -> "other";
    };
}
```

### Virtual Thread Blocking
```java
// Bad: blocking virtual thread unnecessarily
Thread.startVirtualThread(() -> {
    Thread.sleep(1000);  // Don't use sleep in loops
    process();
});

// Good: use structured concurrency
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var task = scope.fork(() -> process());
    scope.join();
    scope.throwIfFailed();
    return task.get();
}
```

### Sequenced Collections Mutability
```java
// getFirst/getLast throw on empty collections
List<String> list = List.of();
String first = list.getFirst();  // NoSuchElementException!

// Use isEmpty check
if (!list.isEmpty()) {
    String first = list.getFirst();
}

// Or handle exception
try {
    String first = list.getFirst();
} catch (NoSuchElementException e) {
    // Handle empty list
}
```

## Performance Considerations

### Virtual Threads
- Ideal for I/O-bound tasks (network, database, file)
- Not better for CPU-bound tasks
- Millions of virtual threads possible
- Very low memory overhead per thread

### Pattern Matching
- No performance penalty vs traditional instanceof
- Compiler optimizes switch expressions
- Cleaner code without sacrificing performance

### Sequenced Collections
- Same performance as before
- New methods are convenience, not overhead
- Reversed views are lazy (no copying)
