# Quiz: Repository

> Generated from `content/`.

## 1. Repository aims to present persistence as:

A. A set of HTTP endpoints
B. A collection-like interface over domain aggregates
C. A UI component tree
D. A message broker topic

**Answer: B.** It abstracts storage behind domain-oriented operations.

## 2. A common repository anti-pattern is:

A. Defining methods per aggregate use case
B. A one-size-fits-all generic CRUD interface that hides important domain queries
C. Using interfaces for testing
D. Separating domain and infrastructure

**Answer: B.** Overly generic repositories can leak persistence details or fail to express intent.
