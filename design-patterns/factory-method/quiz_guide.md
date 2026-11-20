# Quiz: Factory Method

> Generated from `content/`.

## 1. Factory Method is most useful when:

A. One global object must be shared
B. Object creation must vary while the workflow stays fixed
C. Multiple objects must be created as a family atomically
D. An object graph is too expensive to copy

**Answer: B.** It defers instantiation to an overridable hook so workflows can stay generic.

## 2. Compared to putting `if type == ...` in the workflow, Factory Method:

A. Removes all runtime polymorphism
B. Moves variation to a dedicated creation point
C. Requires distributed messaging
D. Eliminates the need for interfaces

**Answer: B.** Creation variability is isolated behind the factory method.
