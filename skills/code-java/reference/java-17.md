# Java 17 Features & Best Practices

**Release Date:** September 2021
**LTS Status:** Long-Term Support (until September 2029)

## Key Features

### Sealed Classes
```java
// Define sealed hierarchy
public sealed interface Shape permits Circle, Rectangle, Triangle { }

public final class Circle implements Shape {
    private final double radius;
    public Circle(double radius) { this.radius = radius; }
    public double radius() { return radius; }
}

public final class Rectangle implements Shape {
    private final double width;
    private final double height;
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
}

// Can be non-sealed to allow further extension
public non-sealed class Triangle implements Shape { }

// Pattern matching with sealed classes
double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> calculateTriangleArea(t);
    };  // Exhaustive - no default needed
}
```

### Records (Enhanced from Java 16)
```java
// Simple record
public record Point(int x, int y) { }

// Record with validation
public record User(String email, String name) {
    public User {
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
    }
}

// Record with additional methods
public record Order(Long id, List<OrderItem> items) {
    public Money totalPrice() {
        return items.stream()
            .map(OrderItem::price)
            .reduce(Money.ZERO, Money::add);
    }

    // Custom constructor
    public Order(Long id) {
        this(id, List.of());
    }
}

// Records can implement interfaces
public record UserDto(Long id, String name) implements Serializable { }
```

### Pattern Matching for instanceof
```java
// Before
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.toUpperCase());
}

// Java 17
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}

// With logical operators
if (obj instanceof String s && s.length() > 5) {
    System.out.println(s);
}
```

### Text Blocks (from Java 15)
```java
String json = """
    {
        "name": "John",
        "email": "john@example.com",
        "role": "admin"
    }
    """;

String sql = """
    SELECT u.id, u.name, u.email
    FROM users u
    WHERE u.active = true
      AND u.role = ?
    ORDER BY u.name
    """;

// With formatting
String html = """
    <html>
        <body>
            <h1>Hello, %s!</h1>
            <p>You have %d messages.</p>
        </body>
    </html>
    """.formatted(userName, messageCount);
```

### Switch Expressions (from Java 14)
```java
// Traditional switch
String result;
switch (day) {
    case MONDAY:
    case TUESDAY:
    case WEDNESDAY:
    case THURSDAY:
    case FRIDAY:
        result = "Weekday";
        break;
    case SATURDAY:
    case SUNDAY:
        result = "Weekend";
        break;
    default:
        result = "Unknown";
}

// Switch expression
String result = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Weekday";
    case SATURDAY, SUNDAY -> "Weekend";
};

// With yield
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> {
        System.out.println("Six letters");
        yield 6;
    }
    case TUESDAY -> {
        System.out.println("Seven letters");
        yield 7;
    }
    default -> {
        System.out.println("Other");
        yield day.toString().length();
    }
};
```

### Helpful NullPointerExceptions
```java
// Before: unclear NPE message
// Exception in thread "main" java.lang.NullPointerException

// Java 17: helpful NPE message
// Exception in thread "main" java.lang.NullPointerException:
//   Cannot invoke "String.length()" because "user.getName()" is null

user.getName().length();  // Now shows exactly what was null
```

## Best Practices

### Use Sealed Classes for Domain Modeling
```java
// Define closed type hierarchies
public sealed interface Result<T> permits Success, Error {
    record Success<T>(T data) implements Result<T> { }
    record Error(String message, Throwable cause) implements Result<Object> {
        public Error(String message) {
            this(message, null);
        }
    }
}

// Exhaustive pattern matching
<T> void handle(Result<T> result) {
    switch (result) {
        case Success<T> s -> process(s.data());
        case Error e -> log.error(e.message(), e.cause());
    }  // No default needed - compiler ensures exhaustiveness
}
```

### Records for DTOs and Value Objects
```java
// API DTOs
public record UserDto(Long id, String name, String email) { }

public record CreateUserRequest(String name, String email) {
    public CreateUserRequest {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name is required");
        }
    }
}

// Value objects
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(amount.add(other.amount), currency);
    }
}
```

### Pattern Matching
```java
// Complex pattern matching
Object processValue(Object obj) {
    return switch (obj) {
        case Integer i -> i * 2;
        case String s -> s.toUpperCase();
        case List<?> list -> list.size();
        case null -> "null value";
        default -> "unknown";
    };
}

// With guards
boolean isValidUser(Object obj) {
    return obj instanceof User u
        && u.isActive()
        && u.hasPermission("read");
}
```

### Text Blocks Best Practices
```java
// Use for multi-line strings
String query = """
    SELECT *
    FROM users
    WHERE active = true
    """;

// Escape special characters when needed
String withQuotes = """
    He said: "Hello!"
    """;

// Control indentation
String indented = """
        Indented line
    Less indented
    """;
```

## Migration from Java 11

### Replace Data Classes with Records
```java
// Before
public class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int x() { return x; }
    public int y() { return y; }

    @Override
    public boolean equals(Object o) { /* ... */ }

    @Override
    public int hashCode() { /* ... */ }

    @Override
    public String toString() { /* ... */ }
}

// After
public record Point(int x, int y) { }
```

### Use Sealed Classes for Type Safety
```java
// Before: open hierarchy with instanceof checks
if (payment instanceof CreditCardPayment) {
    processCreditCard((CreditCardPayment) payment);
} else if (payment instanceof PayPalPayment) {
    processPayPal((PayPalPayment) payment);
} else {
    // Might miss new payment types!
    throw new IllegalArgumentException("Unknown payment type");
}

// After: sealed hierarchy with exhaustive switch
sealed interface Payment permits CreditCardPayment, PayPalPayment { }

void process(Payment payment) {
    switch (payment) {
        case CreditCardPayment cc -> processCreditCard(cc);
        case PayPalPayment pp -> processPayPal(pp);
    }  // Compiler ensures all cases covered
}
```

## Common Pitfalls

### Sealed Classes Must Be in Same Module/Package
```java
// Bad: trying to extend sealed class from different package
package com.example.shapes;
public sealed interface Shape permits Circle { }

package com.example.other;  // Different package
public final class Square implements Shape { }  // Compilation error!

// Good: all in same package or module
package com.example.shapes;
public sealed interface Shape permits Circle, Square { }
public final class Circle implements Shape { }
public final class Square implements Shape { }
```

### Records Are Immutable
```java
// Bad: trying to modify record
public record User(String name) {
    public void setName(String name) {  // Can't do this!
        this.name = name;  // Compilation error
    }
}

// Good: create new instance
public record User(String name) {
    public User withName(String newName) {
        return new User(newName);
    }
}
```

### Pattern Matching Scope
```java
// Pattern variable scope
if (obj instanceof String s) {
    System.out.println(s.length());  // OK
}
System.out.println(s.length());  // Compilation error: s not in scope

// Scope in logical operators
if (obj instanceof String s && s.length() > 5) {  // OK
    System.out.println(s);
}

if (obj instanceof String s || s.length() > 5) {  // Error: s might not be assigned
    System.out.println(s);
}
```
