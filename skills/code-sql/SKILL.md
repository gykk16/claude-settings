---
name: code-sql
description: Guides SQL development following consistent style conventions. Enforces best practices for formatting, naming, and query optimization. Use when writing or reviewing SQL code.
---

# SQL Coding

$ARGUMENTS

For advanced usage, see [reference/reference.md](reference/reference.md)

## Core Principles

> **Core Philosophy**: Use lowercase. Leading commas. Align keywords. Optimize for readability.

1. **Lowercase** - All SQL keywords and identifiers in lowercase
2. **Leading Commas** - Commas at beginning of lines, not end
3. **Keyword Alignment** - Right-align main clauses for readability
4. **Explicit Joins** - Always use explicit JOIN syntax
5. **No SELECT \*** - Always specify column names
6. **Bigint ID PK** - Always include `bigint` type `id` as primary key
7. **Audit Columns** - Always include audit columns in tables
8. **Database Date Types** - Use proper database date/time types
9. **No Enum Types** - Use `varchar` instead of enum for status/type columns

| Do | Don't |
|----|-------|
| Use lowercase keywords | Use UPPERCASE |
| Leading commas | Trailing commas |
| Explicit column names | `select *` |
| Explicit JOIN syntax | Implicit comma joins |
| Table aliases | Repeat full table names |
| `bigint id` as PK | Use other types for PK |
| Include audit columns | Skip audit columns |
| `varchar` for status | `enum` for status |

> **Remember**: Readable SQL is maintainable SQL.

## Quick Reference

### Keyword Alignment

```sql
select u.id
     , u.name
     , u.email
  from users u
       inner join orders o
                  on u.id = o.user_id
 where u.status = 'active'
   and o.order_date >= '2024-01-01'
 group by u.id
        , u.name
        , u.email
having count(*) > 1
 order by o.order_date desc
 limit 10
```

### Naming Conventions

| Type | Style | Example |
|------|-------|---------|
| Tables | snake_case, plural | `users`, `order_items` |
| Columns | snake_case | `user_id`, `created_at` |
| Primary Key | `pk_{table}` | `pk_orders` |
| Unique Key | `uk_{table}_01` | `uk_users_01` |
| Foreign Key | `fk_{table}_01` | `fk_orders_01` |
| Index | `idx_{table}_01` | `idx_orders_01` |

### Primary Key Policy

> **Always use `bigint` type `id` as primary key.**

```sql
-- Always include bigint id as PK
create table users (
    id           bigint
  , name         varchar(100) not null
  , constraint pk_users primary key (id)
);
```

### Audit Columns Policy

> **Always include audit columns** for tracking data changes.

```sql
create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  -- Audit columns (required)
  , created_by   varchar(100) not null
  , created_at   timestamp not null default current_timestamp
  , modified_by  varchar(100) not null
  , modified_at  timestamp not null default current_timestamp
  , constraint pk_orders primary key (id)
);
```

### Column Type Policy

> **Use database date types.** Do NOT use enum types.

```sql
-- Good: varchar for status, database date types
create table users (
    id           bigint
  , status       varchar(20) not null   -- NOT enum
  , birth_date   date                   -- date type
  , login_at     timestamp              -- timestamp type
  , constraint pk_users primary key (id)
);

-- Bad: enum type
create table users (
    id           bigint
  , status       enum('active', 'inactive')  -- Don't use enum
);
```

### Foreign Key Policy

> **Default: No FK constraints.** Only add when user explicitly requests.

```sql
-- Default: No FK constraint
create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  , created_by   varchar(100) not null
  , created_at   timestamp not null default current_timestamp
  , modified_by  varchar(100) not null
  , modified_at  timestamp not null default current_timestamp
  , constraint pk_orders primary key (id)
);

-- Suggested indexes (as comments):
-- create index idx_orders_01 on orders(user_id);
```

## Key Patterns

### SELECT with JOIN

```sql
select u.id
     , u.name
     , o.order_date
     , o.total_amount
  from users u
       inner join orders o
                  on u.id = o.user_id
 where u.status = 'active'
```

### CTE (Common Table Expression)

```sql
with active_users as (
    select id
         , name
      from users
     where status = 'active'
)
, recent_orders as (
    select user_id
         , count(*) as order_count
      from orders
     where order_date >= current_date - interval '30' day
     group by user_id
)
select au.name
     , ro.order_count
  from active_users au
       join recent_orders ro
            on au.id = ro.user_id
```

### INSERT

```sql
insert into users (
    name
  , email
  , status
  , created_at
) values (
    'John Doe'
  , 'john@example.com'
  , 'active'
  , current_timestamp
);
```

### UPDATE

```sql
update users
   set name = 'Jane Doe'
     , email = 'jane@example.com'
     , updated_at = current_timestamp
 where id = 1;
```

### DELETE

```sql
delete from orders
 where status = 'cancelled'
   and created_at < current_date - interval '1' year;
```

### CREATE TABLE

```sql
create table orders (
    id           bigint
  , user_id      bigint not null
  , order_date   date not null
  , total_amount decimal(10, 2)
  , status       varchar(20) default 'pending'   -- varchar, NOT enum
  -- Audit columns (always required)
  , created_by   varchar(100) not null
  , created_at   timestamp not null default current_timestamp
  , modified_by  varchar(100) not null
  , modified_at  timestamp not null default current_timestamp
  , constraint pk_orders primary key (id)
  , constraint uk_orders_01 unique (user_id, order_date)
);

-- Suggested indexes:
-- create index idx_orders_01 on orders(user_id);
-- create index idx_orders_02 on orders(order_date);
-- create index idx_orders_03 on orders(status);
```

## Anti-Patterns to Avoid

### Implicit Joins

```sql
-- Bad: Implicit join
select u.name
     , o.order_date
  from users u
     , orders o
 where u.id = o.user_id

-- Good: Explicit join
select u.name
     , o.order_date
  from users u
       inner join orders o
                  on u.id = o.user_id
```

### Functions on Indexed Columns

```sql
-- Bad: Function on indexed column
select *
  from users
 where year(created_at) = 2024

-- Good: Range condition
select *
  from users
 where created_at >= '2024-01-01'
   and created_at < '2025-01-01'
```

### SELECT *

```sql
-- Bad
select *
  from users
 where status = 'active'

-- Good
select id
     , name
     , email
  from users
 where status = 'active'
```

## Performance Tips

- Use `exists` instead of `in` for subqueries
- Avoid functions on indexed columns in WHERE
- Use `limit` for large result sets
- Suggest indexes as comments, don't create by default
