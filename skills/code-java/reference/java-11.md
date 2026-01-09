# Java 11 Features & Best Practices

**Release Date:** September 2018
**LTS Status:** Long-Term Support (until September 2026)

## Key Features

### Local Variable Type Inference (var) - Enhanced
```java
// Java 10 introduced var, Java 11 allows in lambda parameters
var user = new User("John", "john@example.com");
var users = List.of(user1, user2, user3);

// Java 11: var in lambda parameters
users.forEach((var user) -> System.out.println(user.getName()));

// Useful for annotations on lambda parameters
users.forEach((@NonNull var user) -> process(user));
```

### String Methods
```java
// isBlank() - checks if empty or contains only whitespace
boolean blank = "   ".isBlank();  // true
boolean empty = "".isBlank();     // true

// lines() - split string into lines
Stream<String> lines = multilineString.lines();

// strip(), stripLeading(), stripTrailing()
String trimmed = "  hello  ".strip();  // "hello"
String leading = "  hello  ".stripLeading();  // "hello  "

// repeat()
String repeated = "abc".repeat(3);  // "abcabcabc"
```

### Collection to Array
```java
// Easier array conversion
List<String> list = List.of("a", "b", "c");

// Before Java 11
String[] array = list.toArray(new String[list.size()]);

// Java 11
String[] array = list.toArray(String[]::new);
```

### File Methods
```java
// Read file as String
String content = Files.readString(Path.of("file.txt"));

// Write String to file
Files.writeString(Path.of("output.txt"), "content");
```

### HTTP Client (Standard)
```java
HttpClient client = HttpClient.newHttpClient();

// Synchronous request
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Accept", "application/json")
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// Asynchronous request
CompletableFuture<HttpResponse<String>> future = client.sendAsync(request,
    HttpResponse.BodyHandlers.ofString());

future.thenApply(HttpResponse::body)
    .thenAccept(System.out::println);
```

### Predicate.not()
```java
// Before
List<String> nonEmpty = list.stream()
    .filter(s -> !s.isEmpty())
    .collect(Collectors.toList());

// Java 11
List<String> nonEmpty = list.stream()
    .filter(Predicate.not(String::isEmpty))
    .collect(Collectors.toList());
```

### Optional.isEmpty()
```java
// Before
if (!optional.isPresent()) {
    // handle empty case
}

// Java 11
if (optional.isEmpty()) {
    // handle empty case
}
```

## Best Practices

### Use var Judiciously
```java
// Good: type is obvious
var user = new User("John", "john@example.com");
var users = userRepository.findAll();

// Bad: type is not obvious
var result = process();  // What type is this?
var data = getData();    // Unclear return type

// Good: explicit type for clarity
UserDto result = process();
List<String> data = getData();
```

### HTTP Client Usage
```java
// Reuse HttpClient instance
private static final HttpClient HTTP_CLIENT = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// Use for multiple requests
public CompletableFuture<User> fetchUser(Long id) {
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://api.example.com/users/" + id))
        .build();

    return HTTP_CLIENT.sendAsync(request, HttpResponse.BodyHandlers.ofString())
        .thenApply(HttpResponse::body)
        .thenApply(this::parseUser);
}
```

### String Methods
```java
// Use isBlank() instead of trim().isEmpty()
if (!input.isBlank()) {
    process(input);
}

// Use lines() for processing multiline strings
long lineCount = text.lines().count();

List<String> nonEmptyLines = text.lines()
    .filter(Predicate.not(String::isBlank))
    .collect(Collectors.toList());
```

### File Operations
```java
// Simple file reading/writing
try {
    String content = Files.readString(path);
    String processed = process(content);
    Files.writeString(outputPath, processed);
} catch (IOException e) {
    log.error("File operation failed", e);
}
```

## Migration from Java 8

### Replace deprecated APIs
```java
// Java 8: deprecated in Java 11
new Integer(42);
new Long(42L);
new Double(3.14);

// Java 11: use valueOf or primitive
Integer.valueOf(42);
Long.valueOf(42L);
Double.valueOf(3.14);
```

### Module System Considerations
```java
// If using modules, create module-info.java
module com.example.myapp {
    requires java.net.http;
    requires java.sql;

    exports com.example.myapp.api;
}
```

### Update Dependencies
- Remove JavaEE modules (moved to Jakarta EE)
- Update libraries for Java 11 compatibility
- Check for deprecated API usage

## Common Pitfalls

### var with null
```java
// Bad: compiler can't infer type
var user = null;  // Compilation error

// Good: explicit type for null
User user = null;

// Good: use Optional if value might be absent
var userOpt = Optional.<User>empty();
```

### HTTP Client Error Handling
```java
// Handle errors properly
HttpClient client = HttpClient.newHttpClient();

client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(response -> {
        if (response.statusCode() != 200) {
            throw new RuntimeException("Request failed: " + response.statusCode());
        }
        return response.body();
    })
    .exceptionally(e -> {
        log.error("HTTP request failed", e);
        return null;
    });
```

### String strip() vs trim()
```java
// trim() uses different whitespace definition
String s = "\u2000hello\u2000";  // Unicode whitespace
s.trim();   // Doesn't remove Unicode whitespace
s.strip();  // Removes all whitespace including Unicode

// Use strip() for modern applications
String cleaned = input.strip();
```
