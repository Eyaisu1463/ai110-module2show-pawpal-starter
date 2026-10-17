# PawPal+ Reflection

## 1. System Design

### 1a. Initial design

Three core actions a user should be able to do:

1. Add a pet with name, species, and age
2. Schedule a task for a pet at a specific time
3. View today's plan sorted by time with conflict warnings

Four classes:

- **`Task`** — one activity: description, time, frequency, status, duration, priority. Owns `mark_complete()`.
- **`Pet`** — one animal, holds its own list of tasks.
- **`Owner`** — the human. Holds pets and has `get_all_tasks()`, which returns every pet's tasks as `(pet_name, task)` tuples. This is what the Scheduler reads from, so it can reason across all pets at once.
- **`Scheduler`** — the brain. Sorts, filters, detects conflicts, and handles recurrence by reading from `Owner.get_all_tasks()`.

The `Owner → Pet → Task` chain is composition: Owner _has_ Pets, Pet _has_ Tasks. The Scheduler doesn't own anything — it just reads from the Owner.

### 1b. Design changes

### 1b. Design changes

When I asked AI to compare two ways to implement `Scheduler.detect_conflicts()`,
it showed me a pairwise nested-loop version (O(n²), returns conflicting *pairs*)
and a dict-by-time version (O(n) to group, returns *all tasks per conflicting
time*). I chose the **dict-by-time** version because my `detect_conflicts`
groups tasks by their `time` string in a single pass and then builds warning
strings from the groups. The AI's pairwise version returns conflicting *pairs*
directly, but that would require re-scanning the full task list for every check
and duplicating the "all tasks at 08:00" logic that the UI actually shows.
Grouping first means one pass over the tasks, and the "which tasks conflict"
question is answered by looking at any group with more than one entry. The
pairwise version is slightly more literal ("these two conflict"), but the dict
version matches how the Scheduler is used — one pass, then format the results.

> **Note:** Confirm that your `detect_conflicts` implementation matches this description. If your code uses a dict internally (`seen = {}`) and formats strings from it, swap the words "pairwise" and "dict" accordingly — the reflection should match the shipped code.

---

## 2. Algorithmic Layer

### 2a. Algorithms implemented

| Feature            | Method                         |
| ------------------ | ------------------------------ |
| Sorting            | `Scheduler.sort_by_time()`     |
| Filter by status   | `Scheduler.filter_by_status()` |
| Filter by pet      | `Scheduler.filter_by_pet()`    |
| Conflict detection | `Scheduler.detect_conflicts()` |
| Recurrence         | `Task.mark_complete()`         |

### 2b. Tradeoff

`detect_conflicts()` only flags exact time matches — two tasks at `08:00` get a warning, but a 30-min task at `08:00` and a 45-min task at `08:15` don't. Real overlap detection would need to compare `[start, start + duration)` intervals. I kept the simple version because it's easier to read, easier to test, and less likely to flag false positives from imprecise user input. Documenting the limitation is better than hiding it.

---

## 3. AI Strategy

### 3a. Most effective AI features

- **Writing one method at a time on an existing skeleton** — when `Owner.get_all_tasks()` was already in place, asking the AI for `Scheduler.sort_by_time()` produced correct code on the first try because the surrounding context was right.
- **Generating edge-case tests** — asking "what edge cases matter for a recurrence + conflict system?" surfaced the `once` non-recurrence test and the empty-owner test, neither of which I would have thought of on my own.

### 3b. An AI suggestion I rejected or modified

I asked my AI assistant whether I could simplify the design by moving the task list out of `Pet` and storing all tasks centrally in `Scheduler`. The AI agreed and went further — it actually refactored `pawpal_system.py`, removing `Pet.tasks`, `Pet.add_task()`, `Pet.get_tasks()`, and `Owner.get_all_tasks()`. It added `Scheduler.__init__` with an internal `self._tasks` list and a new `Scheduler.add_task(pet, task)` method, then updated the demo, tests, UML, README, and reflection to match. It reported "12 tests passing" as evidence the new design worked.

I rejected the refactor and reverted it with `git restore`. Three reasons:

1. It broke the UML relationship. My diagram shows `Pet has-a Task`. After the refactor, `Scheduler has-a Task` and `Pet` had nothing.
2. It deleted `Owner.get_all_tasks()`. The Phase 2 spec explicitly says the Scheduler "must read from that Owner method ... or it will not earn the multi-pet point." The refactored version collapsed all tasks into a central list, so Scheduler stopped reading from Owner and started owning the data directly.
3. `Pet.get_tasks()` became meaningless. A Pet could no longer answer "what are my own tasks?" without asking a Scheduler that might not exist yet.

The refactor passed all its own tests — but the tests had been rewritten to match the new design, so they were testing the wrong contract. My takeaway: passing tests prove internal consistency, not spec compliance. As the lead architect, my job was to read the spec, compare it against the AI's "simplification," and say no.

### 3c. How separate chat sessions helped

Starting a fresh chat for Phase 4 kept the AI from reusing Phase 2's scaffold context, which would have silently kept an old `mark_complete` signature. A separate chat for testing also forced me to state each method's contract explicitly ("sort by `HH:MM` string"), which surfaced an ambiguity in `detect_conflicts` before I wrote the test.

---

## 4. Lead Architect Lessons

AI speeds up writing code, but it does not make the design decisions. My job was to check each suggestion against the UML and the spec — and in the case of the Scheduler-owned-tasks refactor, the AI produced passing tests and a plausible-sounding justification, but the change silently violated the multi-pet requirement. Catching it meant reading the spec carefully and not trusting "12 tests passing" as proof of correctness. The biggest wins came from narrow, context-loaded questions ("using `Owner.get_all_tasks()` as written, write `sort_by_time`"), not from broad "build the app" prompts. Separate chats per phase kept me in control of the context.

---

## 5. Verification

**Final test run:** `11 passed in 0.16s`

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5)

All happy paths and most edge cases are covered. One star withheld because duration-overlap conflicts aren't detected or tested (see 2b).
