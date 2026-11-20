# Lean 4 tactics and when to use them

A quick reference for common Lean 4 tactics: what goal/state change each makes and when to reach for it. Names and behavior can vary by Lean/mathlib version; use `#help tactic <name>` or mathlib docs for details in your environment.

## Introduce, name, and close goals

| Tactic | Use when | Effect |
| --- | --- | --- |
| `intro h` / `intros h₁ h₂` | Goal is `∀ x, P x`, `P → Q`, or a function/predicate you need arguments for | Moves binders/hypotheses into the local context with given names. |
| `exact t` | You already have a term `t` whose type is definitionally the goal | Closes the goal with `t` (no unification search beyond definitional equality). |
| `apply t` | A lemma/theorem/constructor `t` would prove the goal if its premises were proved | Rewrites goal to `t`’s premises; may leave metavariables to solve later. |
| `assumption` | Some hypothesis in context is exactly the goal | Closes the goal. |
| `rfl` | Goal is a reflexive equality `a = a` (or definitional) | Closes by reflexivity. |
| `trivial` | Goal is obvious (`True`, trivial equality, simple decidable facts) | Tries simple closing steps. |
| `decide` / `native_decide` | Goal is a decidable proposition that should compute to true | Closes by evaluation (be mindful of kernel/compile cost for `native_decide`). |

## Simplify and rewrite

| Tactic | Use when | Effect |
| --- | --- | --- |
| `simp` / `simp [h]` | Goal or hypothesis can be simplified by simp lemmas/definitions | Rewrites using the simp set (and optional lemmas) to a normal/simpler form. |
| `simp_all` | Many hypotheses and goal share simplifiable structure | Simplifies hypotheses and goal, using hypotheses as simp lemmas where safe. |
| `rw [h]` / `rewrite [h]` | You have equality/equivalence `h : a = b` and want to replace `a` with `b` | Rewrites goal (or target) using `h`; `rw [← h]` rewrites right-to-left. |
| `dsimp` | You want definitional unfolding/simp only (no heavy lemma search) | Simplifies by definitions/definitional simp lemmas. |
| `unfold f` | A definition `f` is blocking progress or clarity | Expands `f` to its definition. |
| `norm_num` | Goal involves concrete numeric computation/comparison | Evaluates numeric expressions and closes/proves numeric goals. |

## Split structure, cases, and induction

| Tactic | Use when | Effect |
| --- | --- | --- |
| `constructor` | Goal is a structure/inductive type with one constructor (e.g. `And`, `Exists`, `Iff`) or you choose the constructor | Splits into fields/arguments of the constructor. |
| `cases h` / `rcases h with ...` | You need to reason by cases on an inductive hypothesis/value | Splits into one goal per constructor; `rcases` destructures with patterns/names. |
| `induction n` / `induction h` | Proving a property over `Nat`, lists, trees, or another inductive type | Produces base and inductive/recursive cases with inductive hypotheses. |
| `left` / `right` | Goal is a disjunction `P ∨ Q` and you know which side holds | Chooses the corresponding branch. |
| `split` | Goal is a conjunction/equivalence/product that splits into subgoals | Produces subgoals for each component. |
| `ext` / `funext` | Goal is equality of functions/sets/structures proved pointwise or by extensionality | Reduces to proving equality on arguments/elements. |

## Build intermediate facts and calculate

| Tactic | Use when | Effect |
| --- | --- | --- |
| `have h : T := t` | You need a named intermediate lemma/value `T` | Adds `h : T` to context (proving `T` now or later depending on form). |
| `let x := t` | You want a local definition/abbreviation | Adds local definition `x`. |
| `suffices h : T by ...` | It is easier to show the goal follows from `T`, then prove `T` | Replaces goal flow: prove `T` implies goal, then prove `T`. |
| `show T` | You want to restate the goal in a definitionally equal form | Changes goal display/type to `T` if convertible. |
| `calc` | Goal is a chain of equalities/inequalities/relations | Builds a stepwise proof with explicit intermediate terms. |
| `specialize h x` | Hypothesis `h` is general (`∀`/implication) and you have a specific instance | Instantiates `h` with `x`. |

## Contradiction, classical, and automation

| Tactic | Use when | Effect |
| --- | --- | --- |
| `contradiction` | Context contains inconsistent hypotheses (e.g. `P` and `¬P`, `False`) | Closes the goal by contradiction. |
| `by_contra h` | Direct proof is awkward and negating the goal helps | Assumes negation of goal as `h` and asks to derive `False`. |
| `push_neg` | Goal/hypothesis has negations over quantifiers/connectives | Pushes negations inward (e.g. `¬∀` to `∃¬`) when available. |
| `linarith` | Goal follows from linear (in)equalities over ordered rings/fields | Solves linear arithmetic goals from context. |
| `omega` | Goal is linear integer/natural arithmetic | Solves many `Nat`/`Int` linear arithmetic and inequality goals. |
| `ring` / `ring_nf` | Goal is polynomial/ring algebra identity or normalization | Proves/normalizes commutative (semi)ring equations. |
| `aesop` | Goal may be solvable by safe, configurable search over rules | Tries automated proof search; good for routine logic/structure goals. |

## Practical workflow

- Start by making the goal shape explicit: `intro`/`intros` for binders and implications, `constructor`/`split`/`ext` for structured goals.
- Choose the proof principle: `induction` for inductive data, `cases`/`rcases` for destructuring, `by_contra` when negation is easier.
- Use `simp`/`rw` to align forms with known lemmas; prefer lemma-driven rewrites over broad unfolding when possible.
- Create footholds with `have`/`calc` for nontrivial steps, and close with `exact`/`apply`/`rfl`/`assumption` or domain automation (`linarith`, `omega`, `ring`, `aesop`) when appropriate.
- When stuck, inspect goal/context and try the smallest tactic that changes the goal in a meaningful way.
