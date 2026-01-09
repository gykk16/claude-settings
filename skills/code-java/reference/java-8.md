# Java 8 Features & Best Practices

**Release Date:** March 2014
**LTS Status:** Extended support ended in 2022 (use Java 11 or later for new projects)

## Key Features

### Lambda Expressions
```java
// Before Java 8
List<String> names = new ArrayList<>();
for (User user : users) {
    names.add(user.getName());
}

// Java 8
List<String> names = users.stream()
    .map(User::getName)
    .collect(Collectors.toList());
```

### Functional Interfaces
```java
@FunctionalInterface
interface Processor<T> {
    T process(T input);
}

// Usage with lambda
Processor<String> uppercase = s -> s.toUpperCase();

// Built-in functional interfaces
Function<String, Integer> length = String::length;
Predicate<String> isEmpty = String::isEmpty;
Consumer<String> printer = System.out::println;
Supplier<LocalDate> today = LocalDate::now;
```

### Stream API
```java
// Filter and collect
List<String> activeUsers = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());

// Reduce operations
int totalAge = users.stream()
    .mapToInt(User::getAge)
    .sum();

Optional<User> oldest = users.stream()
    .max(Comparator.comparing(User::getAge));

// Group by
Map<Role, List<User>> byRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole));
```

### Optional
```java
// Avoid null returns
Optional<User> findUser(Long id) {
    return Optional.ofNullable(userRepository.findById(id));
}

// Using Optional
user.ifPresent(u -> System.out.println(u.getName()));
String name = user.map(User::getName).orElse("Unknown");
User found = user.orElseThrow(() -> new UserNotFoundException());
```

### Method References
```java
// Static method reference
Function<String, Integer> parser = Integer::parseInt;

// Instance method reference
Function<String, String> uppercase = String::toUpperCase;

// Constructor reference
Supplier<List<String>> listFactory = ArrayList::new;
Function<String, User> userFactory = User::new;
```

### Default Methods in Interfaces
```java
interface Calculator {
    int calculate(int a, int b);

    // Default method
    default void printResult(int result) {
        System.out.println("Result: " + result);
    }
}
```

### Date and Time API
```java
// Old way (avoid)
Date date = new Date();
Calendar cal = Calendar.getInstance();

// Java 8 way
LocalDate today = LocalDate.now();
LocalTime time = LocalTime.now();
LocalDateTime dateTime = LocalDateTime.now();
ZonedDateTime zonedDateTime = ZonedDateTime.now();

// Formatting
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String formatted = today.format(formatter);

// Parsing
LocalDate parsed = LocalDate.parse("2024-01-09", formatter);

// Manipulation
LocalDate tomorrow = today.plusDays(1);
LocalDate nextWeek = today.plusWeeks(1);
```

## Best Practices

### Prefer Method References
```java
// Less clear
users.forEach(u -> System.out.println(u));

// More clear
users.forEach(System.out::println);
```

### Use Optional Correctly
```java
// Bad: Optional as parameter
void process(Optional<User> user) { }

// Good: use null-safe parameter or overload
void process(User user) { }
void process() { }

// Bad: Optional field
class UserService {
    private Optional<User> currentUser;
}

// Good: nullable field
class UserService {
    private User currentUser;  // Can be null
}
```

### Stream Performance
```java
// Use parallel streams for large collections
List<String> results = largeList.parallelStream()
    .filter(this::expensiveOperation)
    .collect(Collectors.toList());

// But avoid for small collections (overhead not worth it)
List<String> results = smallList.stream()  // Regular stream
    .filter(String::isEmpty)
    .collect(Collectors.toList());
```

### Collectors
```java
// Common collectors
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
String joined = stream.collect(Collectors.joining(", "));

// Grouping
Map<Role, List<User>> byRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole));

// Partitioning
Map<Boolean, List<User>> byActive = users.stream()
    .collect(Collectors.partitioningBy(User::isActive));

// Counting
Map<Role, Long> countByRole = users.stream()
    .collect(Collectors.groupingBy(User::getRole, Collectors.counting()));
```

## Migration Tips

### Replace Anonymous Classes
```java
// Before
Runnable task = new Runnable() {
    @Override
    public void run() {
        System.out.println("Running");
    }
};

// After
Runnable task = () -> System.out.println("Running");
```

### Replace for loops with Streams
```java
// Before
List<String> names = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        names.add(user.getName());
    }
}

// After
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());
```

### Use New Date/Time API
```java
// Before
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
Date date = sdf.parse("2024-01-09");

// After
LocalDate date = LocalDate.parse("2024-01-09");
```

## Common Pitfalls

### Stream Reuse
```java
// Bad: streams can only be used once
Stream<String> stream = list.stream();
long count = stream.count();
List<String> filtered = stream.filter(s -> s.length() > 5)  // IllegalStateException!
    .collect(Collectors.toList());

// Good: create new stream
long count = list.stream().count();
List<String> filtered = list.stream()
    .filter(s -> s.length() > 5)
    .collect(Collectors.toList());
```

### Optional.get() without check
```java
// Bad: can throw NoSuchElementException
User user = findUser(id).get();

// Good: use safe methods
User user = findUser(id).orElseThrow(() -> new UserNotFoundException());
User user = findUser(id).orElse(defaultUser);
```

### Modifying external variables in lambdas
```java
// Bad: modifying external variable
int sum = 0;
list.forEach(i -> sum += i);  // Compilation error: variable must be final

// Good: use reduce
int sum = list.stream()
    .mapToInt(Integer::intValue)
    .sum();
```
