# SQL Style & Best Practices Reference

A pragmatic guide for writing clean, readable, and maintainable SQL.

> **Core Philosophy**: Use lowercase. Leading commas. Align keywords. Optimize for readability.

---

## Formatting Rules

### Keyword Alignment

Align keywords to create readable structure:

- Main clauses (`select`, `from`, `where`, `group by`, `order by`, `limit`) right-aligned
- `having` left-aligned at column 0
- `join` indented under `from`
- `on` indented under `join`

```sql
select u.id
     , u.name
     , u.email
     , o.order_date
     , o.total_amount
  from users u
       inner join orders o
                  on u.id = o.user_id
 where u.status = 'active'
   and o.order_date >= '2024-01-01'
 group by u.id
        , u.name
        , u.email
        , o.order_date
        , o.total_amount
having count(*) > 1
 order by o.order_date desc
 limit 10
```

### Comma Placement

Place commas at the **beginning** of lines (leading commas):

```sql
-- Good: Leading commas
select id
     , name
     , email
     , created_at
  from users

-- Bad: Trailing commas
select id,
       name,
       email,
       created_at
  from users
```

Benefits of leading commas:
- Easy to comment out columns
- Clear visual alignment
- Simpler version control diffs

### Indentation

- Use consistent indentation
- Align related elements vertically
- `join` indented 7 spaces from `from`
- `on` indented to align after `join` clause

```sql
select p.product_id
     , p.product_name
     , c.category_name
     , sum(oi.quantity) as total_sold
  from products p
       join categories c
            on p.category_id = c.category_id
       join order_items oi
            on p.product_id = oi.product_id
 where p.is_active = true
   and c.category_name in ('Electronics', 'Clothing')
 group by p.product_id
        , p.product_name
        , c.category_name
```

---

## Naming Conventions

### Tables

- Use **snake_case** for table names
- Use **plural** nouns for table names
- Use meaningful, descriptive names

```sql
-- Good
users
order_items
product_categories

-- Bad
User
OrderItem
tbl_products
```

### Columns

- Use **snake_case** for column names
- Use consistent prefixes for related columns
- Avoid abbreviations unless widely understood

```sql
-- Good
user_id
created_at
is_active
total_amount

-- Bad
userId
createdAt
isActive
tot_amt
```

### Constraint Naming

| Type | Pattern | Example |
|------|---------|---------|
| Primary Key | `pk_{table_name}` | `pk_orders` |
| Unique Key | `uk_{table_name}_01`, `_02`, ... | `uk_users_01` |
| Foreign Key | `fk_{table_name}_01`, `_02`, ... | `fk_orders_01` |
| Index | `idx_{table_name}_01`, `_02`, ... | `idx_orders_01` |
| Sequence | `seq_{table_name}_01`, `_02`, ... | `seq_orders_01` |
| Check | `ck_{table_name}_01`, `_02`, ... | `ck_orders_01` |

---

## Primary Key Policy

### Always Use Bigint ID

**Always include `bigint` type `id` as primary key** when creating tables.

```sql
-- Always include bigint id as PK
create table users (
    id           bigint
  , name         varchar(100) not null
  , email        varchar(255) not null
  , created_at   timestamp default current_timestamp
  , constraint pk_users primary key (id)
);

create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  , constraint pk_orders primary key (id)
);
```

Benefits of `bigint id`:
- Consistent across all tables
- Sufficient range for large datasets
- Simple JOIN conditions
- Framework-friendly (ORM, etc.)

---

## Audit Columns Policy

### Always Include Audit Columns

**Always include these four audit columns** when creating tables:

| Column | Type | Description |
|--------|------|-------------|
| `created_by` | `varchar(100)` | User who created the record |
| `created_at` | `timestamp` | When the record was created |
| `modified_by` | `varchar(100)` | User who last modified the record |
| `modified_at` | `timestamp` | When the record was last modified |

```sql
create table orders (
    id           bigint
  , user_id      bigint not null
  , order_date   date not null
  , total_amount decimal(10, 2)
  , status       varchar(20) default 'pending'
  -- Audit columns (always required)
  , created_by   varchar(100) not null
  , created_at   timestamp not null default current_timestamp
  , modified_by  varchar(100) not null
  , modified_at  timestamp not null default current_timestamp
  , constraint pk_orders primary key (id)
);
```

Benefits of audit columns:
- Track who created/modified data
- Essential for debugging and auditing
- Required for compliance in many industries
- Supports soft delete patterns

---

## Column Type Policy

### Use Database Date Types

**Always use proper database date/time types** for temporal data:

| Purpose | Use | Don't Use |
|---------|-----|-----------|
| Date only | `date` | `varchar`, `int` |
| Time only | `time` | `varchar` |
| Date and time | `timestamp`, `datetime` | `varchar`, `bigint` |
| With timezone | `timestamptz` (PostgreSQL) | `timestamp` + separate tz |

```sql
-- Good: Proper date/time types
create table events (
    id           bigint
  , event_date   date                    -- date only
  , start_time   time                    -- time only
  , scheduled_at timestamp               -- date + time
  , created_at   timestamp default current_timestamp
  , constraint pk_events primary key (id)
);

-- Bad: String or numeric for dates
create table events (
    id           bigint
  , event_date   varchar(10)             -- Don't store dates as strings
  , start_time   varchar(8)              -- Don't store times as strings
  , scheduled_at bigint                  -- Don't use unix timestamp
);
```

### Do NOT Use Enum Types

**Never use enum types for columns.** Use `varchar` instead.

```sql
-- Bad: Enum type
create table users (
    id     bigint
  , status enum('active', 'inactive', 'suspended')  -- DON'T
);

-- Good: Varchar type
create table users (
    id     bigint
  , status varchar(20) not null    -- 'active', 'inactive', 'suspended'
);
```

Why avoid enum:
- **Schema changes are hard**: Adding/removing values requires `ALTER TABLE`
- **Database-specific**: Enum syntax differs between MySQL, PostgreSQL, Oracle
- **Migration issues**: Enum changes can be difficult to rollback
- **ORM compatibility**: Some ORMs handle enums poorly
- **Validation**: Better to validate at application layer

Alternative patterns:

```sql
-- Option 1: varchar with check constraint (when strict validation needed)
create table users (
    id     bigint
  , status varchar(20) not null
  , constraint ck_users_01 check (status in ('active', 'inactive', 'suspended'))
);

-- Option 2: Reference table (for complex status with metadata)
create table user_statuses (
    id          bigint
  , code        varchar(20) not null
  , name        varchar(100) not null
  , description varchar(500)
  , constraint pk_user_statuses primary key (id)
  , constraint uk_user_statuses_01 unique (code)
);

create table users (
    id          bigint
  , status_code varchar(20) not null   -- references user_statuses.code
  , constraint pk_users primary key (id)
);
```

---

## Foreign Key and Index Policy

### Default: No FK Constraints

**Do NOT add foreign key constraints by default** - only when user explicitly requests.

```sql
-- Default: No FK constraint, no index
create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  , created_at   timestamp default current_timestamp
  , constraint pk_orders primary key (id)
  , constraint uk_orders_01 unique (user_id, created_at)
);

-- Suggested indexes (as comments):
-- create index idx_orders_01 on orders(user_id);
-- create index idx_orders_02 on orders(created_at);
```

### When User Requests FK Constraints

```sql
-- Only when explicitly requested: With FK constraint
create table orders (
    id           bigint
  , user_id      bigint not null
  , total_amount decimal(10, 2)
  , created_at   timestamp default current_timestamp
  , constraint pk_orders primary key (id)
  , constraint fk_orders_01
      foreign key (user_id) references users(id)
);
```

---

## Query Patterns

### SELECT Statements

- Avoid `select *` in production code
- Always specify column names explicitly
- Use table aliases for multi-table queries

```sql
-- Good
select u.id
     , u.name
     , u.email
  from users u
 where u.status = 'active'

-- Bad
select *
  from users
 where status = 'active'
```

### JOIN Clauses

- Always use explicit JOIN syntax (not implicit comma joins)
- Place join conditions on separate lines with `on`

```sql
-- Good: Explicit JOIN
select u.name
     , o.order_date
  from users u
       inner join orders o
                  on u.id = o.user_id

-- Bad: Implicit join
select u.name
     , o.order_date
  from users u
     , orders o
 where u.id = o.user_id
```

### WHERE Clauses

- Place each condition on a new line
- Align `and` / `or` operators

```sql
select id
     , name
  from users
 where status = 'active'
   and created_at >= '2024-01-01'
   and (role = 'admin'
        or role = 'manager')
```

### Subqueries and CTEs

Use CTEs (Common Table Expressions) for complex queries:

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

### INSERT Statements

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

### UPDATE Statements

```sql
update users
   set name = 'Jane Doe'
     , email = 'jane@example.com'
     , updated_at = current_timestamp
 where id = 1;
```

### DELETE Statements

```sql
delete from orders
 where status = 'cancelled'
   and created_at < current_date - interval '1' year;
```

---

## Performance Best Practices

### EXISTS vs IN

Use `exists` instead of `in` for subqueries when possible:

```sql
-- Good: EXISTS
select u.name
  from users u
 where exists (
    select 1
      from orders o
     where o.user_id = u.id
       and o.status = 'completed'
)

-- Avoid: IN with subquery
select u.name
  from users u
 where u.id in (
    select o.user_id
      from orders o
     where o.status = 'completed'
)
```

### Avoid Functions on Indexed Columns

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

### Index Suggestions

When writing DDL, suggest indexes as comments:

```sql
create table orders (
    id           bigint
  , user_id      bigint not null
  , order_date   date
  , status       varchar(20)
  , constraint pk_orders primary key (id)
);

-- Suggested indexes:
-- create index idx_orders_01 on orders(user_id);
-- create index idx_orders_02 on orders(order_date);
-- create index idx_orders_03 on orders(status);
```

---

## Database-Specific Conventions

### MySQL

- Use backticks for reserved words if necessary
- Use `auto_increment` for primary keys
- Use `datetime` or `timestamp` for date/time columns

```sql
create table users (
    id         bigint auto_increment
  , name       varchar(100) not null
  , created_at timestamp default current_timestamp
  , constraint pk_users primary key (id)
);
```

### PostgreSQL

- Use `serial` or `bigserial` for auto-increment
- Use `timestamptz` for timezone-aware timestamps
- Leverage PostgreSQL-specific features (arrays, jsonb, etc.)

```sql
create table users (
    id         bigserial
  , name       varchar(100) not null
  , metadata   jsonb
  , created_at timestamptz default current_timestamp
  , constraint pk_users primary key (id)
);
```

### Oracle

- Use sequences for primary key generation
- Use `nvl` or `coalesce` for null handling
- Follow Oracle naming length limits (30 characters)

```sql
create sequence seq_users_01 start with 1 increment by 1;

create table users (
    id         number(19)
  , name       varchar2(100) not null
  , created_at timestamp default systimestamp
  , constraint pk_users primary key (id)
);
```

---

## Comments

Use comments to explain complex logic and document business rules:

```sql
-- Get users who have placed orders in the last 30 days
-- but have not logged in during the same period (potential churn risk)
with recent_orders as (
    select distinct user_id
      from orders
     where order_date >= current_date - interval '30' day
)
select u.id
     , u.name
     , u.email
  from users u
       join recent_orders ro
            on u.id = ro.user_id
 where u.last_login_at < current_date - interval '30' day
```

---

## Summary

| Do | Don't |
|----|-------|
| Use lowercase | Use UPPERCASE |
| Leading commas | Trailing commas |
| Explicit column names | `select *` |
| Explicit JOIN syntax | Implicit comma joins |
| Use table aliases | Repeat full table names |
| `bigint id` as PK | Use other types for PK |
| Include audit columns | Skip audit columns |
| `date`, `timestamp` for temporal | `varchar`, `bigint` for temporal |
| `varchar` for status/type | `enum` for status/type |
| CTE for complex queries | Deeply nested subqueries |
| Suggest indexes as comments | Create indexes by default |
| Add FK only when requested | Add FK constraints by default |
