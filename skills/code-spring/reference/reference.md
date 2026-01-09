# Spring Boot Style & Best Practices Reference

A pragmatic guide for writing clean, maintainable Spring Boot applications with Kotlin.

> **Core Philosophy**: Follow Spring conventions. Use constructor injection. Keep layers clean.

Based on [Spring Framework Reference](https://docs.spring.io/spring-framework/reference/) and [Spring Boot Reference](https://docs.spring.io/spring-boot/reference/).

---

## Topic Areas

### [Dependency Injection](dependency-injection.md)

Learn Spring's DI container, constructor injection best practices, and how to write testable, loosely-coupled components.

### [Controller Layer](controller.md)

Guidelines for REST controllers: request mapping, validation, error handling, and response design.

### [Service Layer](service.md)

Business logic organization: service responsibilities, composition patterns, and testing strategies.

### [Repository Layer](repository.md)

Spring Data JPA: query methods, JPQL, projections, pagination, and custom repositories.

### [JPA & Hibernate](jpa.md)

Entity mapping, associations, fetch strategies, locking, specifications, and entity state management.

### [Transaction Management](transaction.md)

Declarative transactions, propagation levels, rollback rules, and avoiding common pitfalls.

### [AOP](aop.md)

Aspect-oriented programming: cross-cutting concerns, pointcuts, advice, and practical use cases.
