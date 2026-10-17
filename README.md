# PawPal+ (Module 2 Project)

**PawPal+** is a smart pet care management system built with Python OOP and Streamlit. It helps a busy pet owner keep their pets happy and healthy by tracking daily routines (feedings, walks, medications, appointments), sorting them chronologically, detecting scheduling conflicts, and automatically creating recurring tasks.

---

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

---

## Features

- 🐾 **Multi-pet support** — one owner manages many pets
- ⏰ **Time-based sorting** — every task appears in chronological order
- 🔍 **Filtering** — by pet name or completion status
- ⚠️ **Conflict detection** — flags tasks scheduled at the same time across pets
- 🔁 **Recurring tasks** — daily and weekly tasks spawn the next occurrence when marked complete
- 💾 **Session persistence** — Streamlit `st.session_state` keeps your data alive between clicks

---

## Architecture

The system is built on four classes:

| Class           | Responsibility                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------------------- | --- |
| **`Task`**      | A single activity with description, time (`HH:MM`), frequency, status, duration, and priority             |
| **`Pet`**       | Stores pet details and a list of tasks                                                                    |
| **`Owner`**     | Manages multiple pets; exposes `get_all_tasks()` returning every pet's tasks as `(pet_name, task)` tuples |
| **`Scheduler`** | Reads from `Owner.get_all_tasks()`; sorts, filters, detects conflicts, and builds schedules               |     |

Tasks live on each `Pet` (`Pet.tasks`). The `Scheduler` reads via `Owner.get_all_tasks()`, which flattens every pet's tasks into `(pet_name, task)` tuples. This keeps the `Pet has-a Task` relationship intact while still letting the Scheduler reason across all pets in one pass — which is the multi-pet requirement from the spec.

See `diagrams/uml_final.mmd` for the full UML class diagram.

---

## Smarter Scheduling

| Feature                | Method                                      | Description                                                                           |
| ---------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Sorting**            | `Scheduler.sort_by_time(owner)`             | Returns all tasks sorted by their `HH:MM` string                                      |
| **Filter by status**   | `Scheduler.filter_by_status(owner, status)` | Returns only tasks matching `pending` / `completed`                                   |
| **Filter by pet**      | `Scheduler.filter_by_pet(owner, pet_name)`  | Returns only the named pet's tasks                                                    |
| **Conflict detection** | `Scheduler.detect_conflicts(owner)`         | Returns warning strings for tasks sharing the same time slot                          |
| **Recurrence**         | `Task.mark_complete()`                      | If frequency is `daily` or `weekly`, returns a fresh pending `Task`; otherwise `None` |

**Tradeoff:** Conflict detection only checks for **exact time matches** (e.g., both at `08:00`). It does not model overlapping durations (e.g., a 30-min walk at 08:00 and a 45-min feeding at 08:15 would not be flagged). This keeps the algorithm simple and readable; a duration-aware version would need interval-overlap math.

---

## Demo Walkthrough

The Streamlit UI (`app.py`) offers:

1. **Owner setup** — enter your name once; it persists in `st.session_state`
2. **Add a pet** — name, species, breed, age
3. **Add a task** — description, time (`HH:MM`), frequency (`daily`, `weekly`, `once`), duration, priority
4. **View today's schedule** — the Scheduler sorts tasks by time and displays them in a table
5. **Conflict warnings** — any same-time collision surfaces as a red `st.warning()`
6. **Mark complete** — completing a daily task spawns tomorrow's version automatically

**Example workflow:**

> Add pet "Max" (Dog) → schedule "Morning Walk" at `08:00` daily → add "Luna" (Cat) with "Vet Visit" at `08:00` → the schedule shows both tasks sorted, and a ⚠️ conflict warning appears because 08:00 is double-booked.

---

## CLI Sample Output

Running `python main.py` demonstrates all four algorithms in the terminal:

```text
=== Alex's Raw Task List (unsorted) ===
  Max   | 18:30 | Evening Walk
  Max   | 08:00 | Morning Walk
  Luna  | 14:00 | Brushing
  Luna  | 12:00 | Lunch Snack

=== Sorted by Time ===
  08:00 | Max   | Morning Walk [pending]
  12:00 | Luna  | Lunch Snack [pending]
  14:00 | Luna  | Brushing [pending]
  18:30 | Max   | Evening Walk [pending]

=== Pending Tasks Only ===
  18:30 | Max   | Evening Walk
  08:00 | Max   | Morning Walk
  14:00 | Luna  | Brushing
  12:00 | Luna  | Lunch Snack

=== Max's Tasks Only ===
  18:30 | Evening Walk
  08:00 | Morning Walk

=== Conflict Detection ===
  ⚠️ Conflict at 08:00: Max's 'Morning Walk' and Luna's 'Vet Visit'

=== Recurrence ===
  'Morning Walk' marked 'completed'.
  New recurring task auto-created: 'Morning Walk' at 08:00 (pending)
```
