# PROFILE 6 — David Thomas & Andrew Hunt (The Pragmatic Programmer, 20th Anniversary Edition)

**Who they are.** Authors of *The Pragmatic Programmer* (1999, revised 2019), the book that named DRY, orthogonality, tracer bullets, and broken windows. Unlike Profiles 1–5 the evidence here is the book's own argument and examples, not a production repo. Companion to `design-best-practices.md`; same section shape. One section per topic, appended as the book is read.

**How to read.** Jump to the one section the decision needs. Read the directive block and the anti-pattern; the evidence is one paragraph by design.

---

### A1. DRY is about knowledge, not code text: one authoritative home per fact

**Principle.** Every piece of knowledge has a single, unambiguous, authoritative representation in the system. Tip 15: Don't Repeat Yourself. Tip 16: Make It Easy to Reuse. The unit is *knowledge*, not text: two identical snippets encoding independent rules are not a violation; two different-looking snippets encoding the same rule are.

**Why it matters.** Every copy of a fact is a place that must change in lockstep, and one is eventually forgotten. The failure is not the duplicate itself but the contradiction that appears when copies diverge.

**Evidence (the book, Chapter 2, Topic 9).** The authors name five places duplication hides, each with its own remedy:
1. **Code**: repeated rules, and formatting or printing mixed into data logic. Extract the rule, however small.
2. **Documentation**: comments restating code. Low-level *what* lives in code and names; comments carry *why*. (Converges with Profile 1 B3.)
3. **Data**: a derived field stored beside its source (`length` next to `start`/`end`). Compute on demand, or cache behind an accessor so only one class keeps it consistent.
4. **Representational**: hand-retyped copies of an external API, an internal contract, or a database schema. External API: generate the client from the spec (OpenAPI) or keep the payload as a map. Internal API: one neutral schema, generated code on every side, never hand-edited. Data source: reflect the schema from the source or use key-value maps; add runtime validation if you gave up compile-time checks. (Converges with Profile 1 E1.)
5. **Inter-developer**: two people solve the same problem unknowingly. No tool catches it; remedies are social: module ownership, a shared utilities area everyone checks first, frequent informal communication, a project librarian.

```python
# Data duplication: stored derived value drifts
class Line:
    def __init__(self, start, end):
        self.start, self.end, self.length = start, end, end - start   # bad

class Line:
    def __init__(self, start, end): self.start, self.end = start, end
    @property
    def length(self): return self.end - self.start                    # one home
```

> [!NOTE]
> **As an agent, you should:**
> - Before writing a second copy of any fact (a constant, a rule, a struct mirroring a schema, a comment explaining a line), ask which of the five kinds it is and apply that kind's remedy.
> - Before writing a new helper, `rg` for an existing one. If you find a near-duplicate, unify or reuse; do not add a third.
> - Never hand-write a type that mirrors an external API, protobuf, or DB table when a spec or the source itself can generate or supply it.
> - Store no derived field without an accessor that owns its consistency.
> - When you see two functions with the same shape and a different middle, extract the middle as a parameter.
> - Do **not** merge code that merely looks alike: confirm the two sites encode the same rule first. Deduplicating independent rules couples them.

**Anti-pattern.** "Deduplicating" two validation functions because their bodies match today, so that a change to one rule silently changes the other. Or the mirror image: a hand-maintained `User` class copied from API docs that breaks the day the vendor adds a field.


---

### A2. Orthogonality: a change to one thing touches one module

**Principle.** Two components are orthogonal when changing one does not affect the other. Tip 17: Eliminate Effects Between Unrelated Things. Each component has one focused responsibility and no hidden dependency on another's internals.

**Why it matters.** Changes and bugs stay local, modules test alone, and risky choices (a vendor, a framework, a database) stay contained. M orthogonal pieces combined with N give M x N capabilities; coupled pieces give one tangle.

**Evidence (the book, Chapter 2, Topic 10).** The design test: "If I dramatically change the requirement behind this function, how many modules are affected?" The answer should be one. Layered systems pass it because each layer uses only the abstractions below. In code the authors name three habits: keep code shy (do not reveal or reach into internals), avoid global data (every reader of a global is tied to every writer), and avoid similar functions (same start and end, different middle). Bug fixes are the running diagnostic: a fix that touches many modules is coupling showing itself. (Converges with Profile 2 F2 and Profile 4 A3.)

```python
CONFIG = {"tax_rate": 0.2}
def total(price): return price * (1 + CONFIG["tax_rate"])    # bad: hidden global

def total(price, tax_rate): return price * (1 + tax_rate)    # explicit, swappable
```

> [!NOTE]
> **As an agent, you should:**
> - Before a change, name the one module that should own it. If the diff spreads to unrelated modules, stop and report the coupling instead of patching each site.
> - Pass dependencies in; never read or add module-level mutable state to get a value into a function.
> - Do not reach through an object to its internals (`a.b.c.do()`); ask the owner for what you need.
> - Keep third-party and framework types at the edge, behind an interface you own, so the vendor can change without touching the core.
> - Treat a test that needs heavy setup or global resets as a coupling finding, not a testing problem.

**Anti-pattern.** A one-line requirement change (a tax rate, a date format) that edits eight files because each one reads the same global or formats the value itself. The helicopter: every control movement forces a compensating adjustment on all the others.


---

### A3. Tracer bullets: thin end-to-end path first, production quality, kept

**Principle.** When the target is uncertain, build one narrow slice through every real layer, then thicken it. Tip 20: Use Tracer Bullets to Find the Target. The feature set is thin; the code is not throwaway. It is the skeleton the product grows on.

**Why it matters.** Layers finished in isolation meet for the first time at the end, when a wrong shape is most expensive. A tracer shows where the shot landed after one round, so a miss ("that is not what I meant") costs one thin slice to correct.

**Evidence (the book, Chapter 2, Topic 12).** Pick the most important or riskiest requirement and implement it UI to storage and back, doing the least possible at each stage. The authors list the payoff: users see something working early, developers get a structure to build in, integration is continuous rather than big-bang, there is always something to demo, and progress is measured in features that work end to end. Tracer code differs from a prototype in exactly one way that matters: it is lean but complete, with real error handling, tests, and structure, and it stays. (Converges with Profile 1 B1.)

```python
def handle_get_order(request):                               # web layer, real
    order = OrderService(InMemoryOrderStore()).get(request.args["id"])
    if order is None: return json_response({"error": "not found"}, status=404)
    return json_response(order.to_dict())
# Every layer exists; only the store is a stand-in. Tests and errors are real.
```

> [!NOTE]
> **As an agent, you should:**
> - On a new feature or project, first deliver one request that travels every layer and runs, before completing any single layer.
> - Choose the slice by risk: the requirement most likely to prove the architecture wrong goes first.
> - Hold production standards in the slice: explicit errors, a test, logging. Thin means few features, not low quality.
> - Put stand-ins (in-memory store, fake client) behind the same interface the real one will use, so thickening is a swap.
> - State in the hand-off that this is tracer code and which parts are stand-ins.

**Anti-pattern.** A complete schema and data layer with no endpoint calling it, or three polished layers integrated for the first time in the final week.


---

### A4. Prototypes: answer one question cheaply, then delete the code

**Principle.** A prototype exists to learn one specific thing. Tip 21: Prototype to Learn. The deliverable is the answer; the code is disposable and is never deployed.

**Why it matters.** Testing a risky assumption in an hour is far cheaper than discovering it inside production code. The cost appears only when the prototype survives: it was written without correctness, completeness, robustness, or style, and it becomes the foundation anyway.

**Evidence (the book, Chapter 2, Topic 13).** Prototype anything unproven, unfamiliar, or critical: architecture, new functionality, the structure of external data, third-party tools, performance, user interface. Use the fastest medium, which is often not code: a whiteboard, Post-it Notes, a spreadsheet, a script. An architecture prototype answers questions such as: are responsibilities well defined, is coupling minimized, is there duplication, does every module have a path to the data it needs. The authors' rule for misuse: if there is any chance the prototype will be mistaken for the real thing, use tracer bullets (A3) instead.

> [!NOTE]
> **As an agent, you should:**
> - Before writing exploratory code, state the one question it answers and declare it a prototype. If no question can be stated, it is not a prototype.
> - Keep it outside the source tree (`/tmp`, `scratch/`), never imported by real code, and delete it once the answer is recorded.
> - Skip error handling, tests, and style freely here, and only here. Report the answer, not the script.
> - Never promote prototype code by editing it into shape. Rewrite it to production standards, using what was learned.
> - Decide the mode up front and say it: throwaway to learn (A4) or kept skeleton (A3). Do not blend the two.

**Anti-pattern.** The spike script that answered "does the vendor API return what the docs say" gains a retry loop, then a cron entry, and is now production with no tests and hard-coded credentials.


---
