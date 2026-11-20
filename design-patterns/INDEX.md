# Design patterns

> Generated from `content/`. Edit the YAML, then run `tools/build.py`.

Object and application patterns are the bridge between data-structure reasoning and system architecture.

## Patterns

- [Abstract Factory](abstract-factory/README.md) — creational: Provide an interface for creating families of related objects without specifying concrete classes.
- [Adapter](adapter/README.md) — structural: Convert the interface of a component into one clients expect so incompatible interfaces can collaborate.
- [Bridge](bridge/README.md) — structural: Decouple an abstraction from its implementation so both can vary independently.
- [Builder](builder/README.md) — creational: Separate construction of a complex object from its representation so the same process can create different forms.
- [Chain of Responsibility](chain-of-responsibility/README.md) — behavioral: Pass a request along a chain of handlers until one handles or processes it.
- [Command](command/README.md) — behavioral: Encapsulate a request as an object, allowing parameterization, queuing, logging, and undo.
- [Composite](composite/README.md) — structural: Compose objects into tree structures and let clients treat individual objects and compositions uniformly.
- [Decorator](decorator/README.md) — structural: Attach additional responsibilities to an object dynamically by wrapping it.
- [Dependency Injection](dependency-injection/README.md) — application: Supply an object’s dependencies from the outside rather than having it construct or locate them internally.
- [Facade](facade/README.md) — structural: Provide a simplified interface to a complex subsystem.
- [Factory Method](factory-method/README.md) — creational: Let subclasses or hook implementations decide which concrete object to create.
- [Flyweight](flyweight/README.md) — structural: Share common intrinsic state across many fine-grained objects to reduce memory use.
- [Iterator](iterator/README.md) — behavioral: Provide a way to access elements of an aggregate sequentially without exposing its representation.
- [Mediator](mediator/README.md) — behavioral: Centralize complex interactions between related objects in a mediator to reduce direct dependencies.
- [Memento](memento/README.md) — behavioral: Capture and externalize an object’s internal state so it can be restored later without violating encapsulation.
- [Observer](observer/README.md) — behavioral: Define a one-to-many dependency so dependents are notified when a subject changes state.
- [Prototype](prototype/README.md) — creational: Create new objects by copying a prototypical instance instead of instantiating from scratch.
- [Proxy](proxy/README.md) — structural: Provide a surrogate or placeholder that controls access to another object.
- [Repository](repository/README.md) — application: Mediate between domain and data mapping layers through a collection-like interface for aggregates.
- [State](state/README.md) — behavioral: Allow an object to alter its behavior when its internal state changes by delegating to state objects.
- [Strategy](strategy/README.md) — behavioral: Define interchangeable algorithms behind a stable interface so behavior can vary at runtime.
- [Template Method](template-method/README.md) — behavioral: Define the skeleton of an algorithm in a base operation, deferring specific steps to subclasses or hooks.
- [Unit of Work](unit-of-work/README.md) — application: Track changes to objects during a business transaction and coordinate writing them out as a single unit.
- [Visitor](visitor/README.md) — behavioral: Represent an operation to be performed on elements of an object structure without changing the element classes.

## Explore

- Searchable local catalogue: `just -f site/justfile serve` then open `site/index.html`.

## Use it

- `just -f design-patterns/justfile build`
- `just -f design-patterns/justfile check`
- `just -f design-patterns/justfile quiz`

Cards feed `cards/deck.json` from `design-patterns/glossary.json`.
