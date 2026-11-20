# Quiz: Prototype

> Generated from `content/`.

## 1. Prototype is especially helpful when:

A. You need one instance per process
B. Creating from a configured template is cheaper than full construction
C. Objects must never be copied
D. You must enforce access control

**Answer: B.** Cloning reuses an initialized template as the starting point.

## 2. A key risk with Prototype is:

A. Inability to support interfaces
B. Incorrect deep vs shallow copying of mutable state
C. Guaranteed memory leaks
D. Mandatory network calls during clone

**Answer: B.** Copy semantics determine whether clones share nested mutable objects.
