# Quiz: Abstract Factory

> Generated from `content/`.

## 1. Abstract Factory differs from Factory Method because it:

A. Creates one product via inheritance hook only
B. Creates families of related products together
C. Clones existing instances
D. Builds objects step by step

**Answer: B.** Its focus is consistent families (e.g., queue + storage + metrics) per environment.

## 2. When adding a new product type to an Abstract Factory, you usually must:

A. Change only one concrete class
B. Update all factory interfaces and concrete factories
C. Add a database migration
D. Introduce an event bus

**Answer: B.** The abstraction declares creation for every family member, so it widens across implementations.
