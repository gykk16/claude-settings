# Naming Conventions

## Packages
```java
// lowercase, no underscores
package com.example.project;
package org.company.feature.domain;
```

## Classes & Interfaces
```java
// UpperCamelCase
class UserRepository { }
class OrderProcessingService { }
interface PaymentGateway { }
```

## Methods & Variables
```java
// lowerCamelCase
void processOrder() { }
BigDecimal calculateTotalPrice() { }

String userName = "John";
int orderCount = 0;
```

## Constants
```java
// SCREAMING_SNAKE_CASE
public static final int MAX_RETRY_COUNT = 3;
private static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(30);
```

## Type Parameters
```java
// Single capital letter or descriptive uppercase
class Box<T> { }
class Repository<E extends Entity> { }
class Cache<K, V> { }

// Descriptive when needed
class Converter<INPUT, OUTPUT> { }
```

## Acronyms
```java
// Two letters: both uppercase
class IOStream { }

// Longer: capitalize first letter only
class XmlParser { }
class HttpClient { }
class HtmlRenderer { }
```
# Code Organization

## Class Layout Order

```java
public class UserService {
    // 1. Constants
    private static final int CACHE_SIZE = 100;
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    // 2. Static variables
    private static UserService instance;

    // 3. Instance variables (grouped by visibility)
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final Map<Long, User> cache;

    // 4. Constructors
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
        this.cache = new HashMap<>();
    }

    // Constructor overloads
    public UserService(UserRepository userRepository) {
        this(userRepository, new DefaultEmailService());
    }

    // 5. Factory methods (if any)
    public static UserService getInstance() {
        if (instance == null) {
            instance = new UserService(new DefaultUserRepository());
        }
        return instance;
    }

    // 6. Public methods
    public Optional<User> findUser(Long id) { }

    public User createUser(String name, String email) { }

    // 7. Package-private methods
    void clearCache() { }

    // 8. Protected methods
    protected void validateUser(User user) { }

    // 9. Private methods
    private void updateCache(User user) { }

    private void notifyListeners(User user) { }

    // 10. Static nested classes
    private static class CacheEntry {
        private final User user;
        private final Instant timestamp;

        CacheEntry(User user, Instant timestamp) {
            this.user = user;
            this.timestamp = timestamp;
        }
    }
}
```

## Group Related Members
```java
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;

    // Group: Order creation
    public Order createOrder(CreateOrderRequest request) { }

    private void validateOrderRequest(CreateOrderRequest request) { }

    private Money calculateOrderTotal(List<OrderItem> items) { }

    // Group: Order retrieval
    public Optional<Order> findOrder(Long id) { }

    public List<Order> findOrdersByUser(Long userId) { }

    private Order enrichOrderWithDetails(Order order) { }

    // Group: Order status management
    public Order cancelOrder(Long id) { }

    public Order completeOrder(Long id) { }

    private Order updateOrderStatus(Long id, OrderStatus status) { }
}
```

## Interface Implementation Order
```java
public class UserRepositoryImpl implements UserRepository, Closeable {

    private final Database database;

    // 1. Interface methods (in interface declaration order)
    @Override
    public Optional<User> findById(Long id) { }

    @Override
    public User save(User user) { }

    @Override
    public void delete(Long id) { }

    // 2. Additional interface methods (Closeable)
    @Override
    public void close() throws IOException {
        database.close();
    }

    // 3. Own public methods
    public Optional<User> findByEmail(String email) { }

    // 4. Private methods
    private UserEntity mapToEntity(User user) { }
}
```

## Keep Classes Focused
```java
// Bad: mixed responsibilities
class UserService {
    void createUser() { }
    void sendWelcomeEmail() { }    // Email responsibility
    void generateUserReport() { }  // Reporting responsibility
    void validateUserData() { }
    void exportUsersToCsv() { }    // Export responsibility
}

// Good: single responsibility per class
class UserService {
    Optional<User> findUser(Long id) { }
    User createUser(String name, String email) { }
    User updateUser(Long id, UpdateUserRequest request) { }
    void deleteUser(Long id) { }
}

class UserNotificationService {
    void sendWelcomeEmail(User user) { }
    void sendPasswordReset(User user) { }
}

class UserReportService {
    Report generateReport(ReportCriteria criteria) { }
    void exportToCsv(List<User> users, Path outputPath) { }
}
```

## Record Layout (Java 16+)
```java
public record User(
    // 1. Required components first
    Long id,
    String email,

    // 2. Optional components
    String name,
    Role role
) {
    // Compact constructor for validation
    public User {
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }

        // Normalize values
        name = name == null ? "" : name.trim();
        role = role == null ? Role.USER : role;
    }

    // Additional constructors
    public User(String email) {
        this(null, email, "", Role.USER);
    }

    // Computed properties
    public String displayName() {
        return name.isEmpty() ? email.substring(0, email.indexOf("@")) : name;
    }

    // Helper methods
    public boolean isAdmin() {
        return role == Role.ADMIN;
    }
}
```

## Sealed Class Layout (Java 17+)
```java
public sealed interface Result<T> permits Success, Error, Loading {

    // Common operations in parent
    default T getOrNull() {
        return this instanceof Success<T> s ? s.data() : null;
    }

    default T getOrThrow() {
        return switch (this) {
            case Success<T> s -> s.data();
            case Error e -> throw new IllegalStateException(e.message());
            case Loading l -> throw new IllegalStateException("Still loading");
        };
    }
}

// Success case first (most common)
public record Success<T>(T data) implements Result<T> { }

// Error cases
public record Error(String message, Throwable cause) implements Result<Object> {
    public Error(String message) {
        this(message, null);
    }
}

// State cases
public record Loading() implements Result<Object> { }
```
# Formatting

## Indentation & Braces
```java
// 4 spaces, opening brace at end of line
if (user != null) {
    processUser(user);
} else {
    handleMissingUser();
}

// Always use braces, even for single statements
if (isValid) {
    return result;
}
```

## Method Signatures
```java
// Short: single line
public Optional<User> findById(Long id) {
    return repository.find(id);
}

// Long: break parameters
public Order createOrder(
        Long userId,
        List<OrderItem> items,
        Address shippingAddress,
        PaymentMethod paymentMethod) {
    // ...
}

// Default parameters simulation
public Order createOrder(Long userId, List<OrderItem> items, Address address) {
    return createOrder(userId, items, address, PaymentMethod.CREDIT_CARD);
}
```

## Chained Calls
```java
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .sorted()
    .toList();
```

## Line Wrapping
```java
// Wrap after operators
String result = firstName + " " + middleName + " "
    + lastName + " " + suffix;

// Wrap before dot
String processed = someVeryLongExpression
    .transform()
    .normalize()
    .validate();
```
# Clean Code Principles

## Write Self-Documenting Code
```java
// Bad
int calc(int a, int b) {
    return a * b + (int)(a * 0.1);
}

// Good
int calculateTotalWithTax(int price, int quantity) {
    int subtotal = price * quantity;
    int tax = (int)(subtotal * TAX_RATE);
    return subtotal + tax;
}
```

## Keep Methods Small & Focused
```java
// Bad: doing too much
void processOrder(Order order) {
    // validate (20 lines)
    // calculate (15 lines)
    // save (10 lines)
    // notify (15 lines)
}

// Good: single responsibility
ProcessedOrder processOrder(Order order) {
    Order validated = validateOrder(order);
    Order priced = calculateTotals(validated);
    Order saved = orderRepository.save(priced);
    notificationService.sendConfirmation(saved);
    return saved;
}
```

## Avoid Deep Nesting
```java
// Bad
void processUser(User user) {
    if (user != null) {
        if (user.isActive()) {
            if (user.hasPermission("admin")) {
                // logic here
            }
        }
    }
}

// Good: early returns
void processUser(User user) {
    if (user == null) return;
    if (!user.isActive()) return;
    if (!user.hasPermission("admin")) return;

    // logic here
}

// Good: extract guard conditions
void processUser(User user) {
    if (!isValidAdminUser(user)) return;
    // logic here
}

private boolean isValidAdminUser(User user) {
    return user != null
        && user.isActive()
        && user.hasPermission("admin");
}
```

## Comments: Explain Why, Not What
```java
// Bad: explains what (obvious)
// Increment counter
counter++;

// Good: explains why (not obvious)
// Reset after successful connection to prevent accumulated retries
retryCount = 0;

// Good: explain complex business rules
// Apply discount if customer has been active for over a year
// and has made more than 10 purchases (loyalty program rule #3)
if (accountAge > Duration.ofDays(365) && purchaseCount > 10) {
    applyDiscount(order);
}
```
# Modern Java Features

## Records (Java 16+)
```java
// Simple data carrier
public record Point(int x, int y) { }

// With validation
public record User(String email, String name) {
    public User {
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
    }
}

// With additional methods
public record Order(Long id, List<OrderItem> items) {
    public Money totalPrice() {
        return items.stream()
            .map(OrderItem::price)
            .reduce(Money.ZERO, Money::add);
    }
}
```

## Sealed Classes (Java 17+)
```java
public sealed interface Shape permits Circle, Rectangle, Triangle { }

public final class Circle implements Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }
}

public final class Rectangle implements Shape {
    private final double width;
    private final double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
}

public final class Triangle implements Shape {
    private final double base;
    private final double height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }
}

// Exhaustive pattern matching
double calculateArea(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}
```

## Pattern Matching (Java 21+)
```java
// Pattern matching for instanceof
if (obj instanceof String s) {
    return s.toUpperCase();
}

// Pattern matching for switch
String result = switch (obj) {
    case String s -> s.toUpperCase();
    case Integer i -> i.toString();
    case null -> "null";
    default -> obj.toString();
};

// Record patterns
record Point(int x, int y) { }

if (obj instanceof Point(int x, int y)) {
    System.out.println("x: " + x + ", y: " + y);
}

// Pattern matching in switch with guards
String classify(Object obj) {
    return switch (obj) {
        case String s when s.isEmpty() -> "empty string";
        case String s -> "non-empty string";
        case Integer i when i > 0 -> "positive integer";
        case Integer i -> "non-positive integer";
        case null -> "null";
        default -> "unknown";
    };
}
```

## Text Blocks (Java 15+)
```java
String json = """
    {
        "name": "John",
        "email": "john@example.com",
        "age": 30
    }
    """;

String sql = """
    SELECT u.id, u.name, u.email
    FROM users u
    WHERE u.active = true
      AND u.created_at > ?
    ORDER BY u.name
    """;

String html = """
    <html>
        <body>
            <h1>Hello, %s!</h1>
        </body>
    </html>
    """.formatted(userName);
```

## Streams (Java 8+)
```java
// Filter and map
List<String> activeUserNames = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .toList();

// Reduce
int totalAge = users.stream()
    .mapToInt(User::getAge)
    .sum();

Optional<User> oldest = users.stream()
    .max(Comparator.comparing(User::getAge));

// Group by
Map<Role, List<User>> byRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole));

// Partition
Map<Boolean, List<User>> activePartition = users.stream()
    .collect(Collectors.partitioningBy(User::isActive));
```
# Immutability

## Immutable Collections (Java 9+)
```java
// Unmodifiable collections
List<String> names = List.of("Alice", "Bob", "Charlie");
Set<Integer> numbers = Set.of(1, 2, 3);
Map<String, Integer> scores = Map.of(
    "Alice", 100,
    "Bob", 95,
    "Charlie", 90
);

// Copying collections defensively
public class Users {
    private final List<User> users;

    public Users(List<User> users) {
        this.users = List.copyOf(users);  // Defensive copy
    }

    public List<User> getUsers() {
        return users;  // Already immutable
    }
}
```

## Using final
```java
// final for parameters and local variables
public void processUser(final User user) {
    final String name = user.getName();
    final int age = user.getAge();

    // Prevents accidental reassignment
}

// final for instance variables
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;

    public UserService(UserRepository repository, EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
    }
}
```

## Immutable Objects
```java
// Use records for simple immutable data (Java 16+)
public record Point(int x, int y) { }

// Traditional immutable class
public final class User {
    private final String name;
    private final String email;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() { return name; }
    public String getEmail() { return email; }

    // Return new instance for modifications
    public User withName(String newName) {
        return new User(newName, this.email);
    }
}
```
# Error Handling

## Optional for Expected Absence (Java 8+)
```java
public Optional<User> findUser(Long id) {
    return userRepository.findById(id);
}

// Using Optional
user.ifPresent(this::processUser);
String name = user.map(User::getName).orElse("Unknown");
User found = findUser(id).orElseThrow(() -> new UserNotFoundException(id));
```

## Exceptions for Exceptional Conditions
```java
public User createUser(String name, String email) {
    if (name == null || name.isBlank()) {
        throw new IllegalArgumentException("Name cannot be blank");
    }
    if (email == null || !email.contains("@")) {
        throw new IllegalArgumentException("Invalid email format");
    }
    return userRepository.save(new User(name, email));
}
```

## Custom Exceptions
```java
public class UserNotFoundException extends RuntimeException {
    private final Long userId;

    public UserNotFoundException(Long userId) {
        super("User not found: " + userId);
        this.userId = userId;
    }

    public Long getUserId() {
        return userId;
    }
}

public class ValidationException extends RuntimeException {
    private final List<String> errors;

    public ValidationException(List<String> errors) {
        super("Validation failed: " + String.join(", ", errors));
        this.errors = List.copyOf(errors);
    }

    public List<String> getErrors() {
        return errors;
    }
}
```

## Try-with-Resources (Java 7+)
```java
// Automatic resource management
public List<String> readLines(Path path) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(path)) {
        return reader.lines().toList();
    }
}

// Multiple resources
public void copyFile(Path source, Path target) throws IOException {
    try (InputStream in = Files.newInputStream(source);
         OutputStream out = Files.newOutputStream(target)) {
        in.transferTo(out);
    }
}
```

## Exception Best Practices

### Catch Specific Exceptions
```java
// Bad: catching generic Exception
try {
    processData();
} catch (Exception e) {
    log.error("Error", e);
}

// Good: catch specific exceptions
try {
    processData();
} catch (FileNotFoundException e) {
    log.error("File not found", e);
} catch (IOException e) {
    log.error("IO error", e);
}
```

### Don't Swallow Exceptions
```java
// Bad: empty catch block
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure
}

// Good: handle or rethrow
try {
    riskyOperation();
} catch (Exception e) {
    log.error("Operation failed", e);
    throw new RuntimeException("Failed to complete operation", e);
}
```
# Testing Best Practices

## Descriptive Test Names
```java
@Test
void shouldReturnEmptyListWhenNoUsersMatchCriteria() { }

@Test
void shouldThrowExceptionWhenUserIdIsNegative() { }

@Test
void shouldApplyDiscountForLoyaltyProgramMembers() { }
```

## Arrange-Act-Assert Pattern
```java
@Test
void shouldCalculateCorrectTotalWithDiscount() {
    // Arrange
    Order order = new Order(
        List.of(new OrderItem(Money.of(100))),
        10  // 10% discount
    );

    // Act
    Money total = calculator.calculateTotal(order);

    // Assert
    assertEquals(Money.of(90), total);
}
```

## Test Data Builders
```java
class UserBuilder {
    private String name = "Default Name";
    private String email = "default@example.com";
    private Role role = Role.USER;

    UserBuilder withName(String name) {
        this.name = name;
        return this;
    }

    UserBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    UserBuilder withRole(Role role) {
        this.role = role;
        return this;
    }

    User build() {
        return new User(name, email, role);
    }
}

@Test
void shouldProcessAdminUsers() {
    User admin = new UserBuilder()
        .withRole(Role.ADMIN)
        .build();

    service.process(admin);

    // assertions
}
```

## Parameterized Tests (JUnit 5)
```java
@ParameterizedTest
@ValueSource(strings = {"", "  ", "\t", "\n"})
void shouldRejectBlankNames(String name) {
    assertThrows(IllegalArgumentException.class, () -> {
        new User(name, "email@example.com");
    });
}

@ParameterizedTest
@CsvSource({
    "10, 100, 1000",
    "5, 200, 1000",
    "20, 50, 1000"
})
void shouldCalculateCorrectTotal(int quantity, int price, int expected) {
    int total = quantity * price;
    assertEquals(expected, total);
}
```

## Test Organization
```java
@Nested
@DisplayName("User creation")
class UserCreation {

    @Test
    void shouldCreateUserWithValidData() { }

    @Test
    void shouldThrowExceptionForInvalidEmail() { }

    @Nested
    @DisplayName("with admin role")
    class WithAdminRole {

        @Test
        void shouldGrantAdminPermissions() { }
    }
}
```

## Mocking (Mockito)
```java
@Test
void shouldSendEmailAfterUserCreation() {
    // Arrange
    EmailService emailService = mock(EmailService.class);
    UserService userService = new UserService(repository, emailService);

    // Act
    User user = userService.createUser("John", "john@example.com");

    // Assert
    verify(emailService).sendWelcomeEmail(user);
}
```
# Anti-Patterns to Avoid

## Over-Engineering
```java
// Bad: unnecessary abstraction
interface StringProcessor {
    String process(String s);
}

class UpperCaseProcessor implements StringProcessor {
    @Override
    public String process(String s) {
        return s.toUpperCase();
    }
}

class ProcessorFactory {
    StringProcessor create(String type) {
        return new UpperCaseProcessor();
    }
}

// Good: simple and direct
String toUpperCase(String s) {
    return s.toUpperCase();
}
```

## God Classes
```java
// Bad: class does everything
class UserManager {
    void createUser() { }
    void sendEmail() { }
    void generateReport() { }
    void processPayment() { }
    void validateData() { }
    // ... 50 more methods
}

// Good: split by responsibility
class UserService { }
class EmailService { }
class ReportGenerator { }
class PaymentProcessor { }
class DataValidator { }
```

## Null Checking Instead of Optional
```java
// Bad: returning null
public User findUser(Long id) {
    User user = userRepository.findById(id);
    return user;  // Can be null
}

// Calling code forced to check
User user = service.findUser(id);
if (user != null) {
    process(user);
}

// Good: Optional
public Optional<User> findUser(Long id) {
    return userRepository.findById(id);
}

// Calling code more expressive
service.findUser(id).ifPresent(this::process);
```

## Primitive Obsession
```java
// Bad: using primitives everywhere
void createOrder(String userId, String productId, int quantity, double price) { }

// Good: use value objects
void createOrder(UserId userId, ProductId productId, Quantity quantity, Money price) { }

// Value objects provide type safety and validation
public record UserId(String value) {
    public UserId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("User ID cannot be blank");
        }
    }
}
```

## Magic Numbers
```java
// Bad: unexplained numbers
if (user.getAge() > 18) {
    grantAccess();
}

if (retryCount > 3) {
    fail();
}

// Good: named constants
private static final int LEGAL_AGE = 18;
private static final int MAX_RETRY_COUNT = 3;

if (user.getAge() > LEGAL_AGE) {
    grantAccess();
}

if (retryCount > MAX_RETRY_COUNT) {
    fail();
}
```

## Excessive Comments
```java
// Bad: commenting obvious code
// Get the user name
String name = user.getName();

// Check if age is greater than 18
if (user.getAge() > 18) {
    // Grant access to the user
    grantAccess(user);
}

// Good: self-documenting code
String userName = user.getName();

if (user.isAdult()) {
    grantAccess(user);
}
```

## Mutable Static State
```java
// Bad: mutable static state
public class Configuration {
    private static String apiKey;  // Mutable static field

    public static void setApiKey(String key) {
        apiKey = key;
    }
}

// Good: immutable configuration
public class Configuration {
    private final String apiKey;

    public Configuration(String apiKey) {
        this.apiKey = apiKey;
    }

    public String getApiKey() {
        return apiKey;
    }
}
```

## Exception as Flow Control
```java
// Bad: using exceptions for normal flow
try {
    User user = findUser(id);
    process(user);
} catch (UserNotFoundException e) {
    createDefaultUser();
}

// Good: use Optional or explicit checks
Optional<User> userOpt = findUser(id);
if (userOpt.isPresent()) {
    process(userOpt.get());
} else {
    createDefaultUser();
}
```
