# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- **UML Design:** The initial design established a modular, object-oriented architecture consisting of four core classes: `Owner`, `Pet`, `Task`, and `Scheduler`[cite: 1].
- **Responsibilities:**
  - `Owner`: Manages the household and maintains a collection of `Pet` objects.
  - `Pet`: Stores pet metadata (name, species, breed, age) and holds a dedicated list of `Task` objects.
  - `Task`: Represents individual care routines, tracking attributes like description, time, frequency, and completion status.
  - `Scheduler`: Acts as the core logic engine ("brain"), retrieving and organizing tasks across all pets in the household[cite: 1].

**b. Design changes**

- **Changes made:** Yes, the design evolved during implementation. While the base class skeletons remained stable, the `Scheduler` class was expanded to include dedicated algorithmic methods for chronological time sorting (`sort_by_time`) and duplicate time slot checking (`detect_conflicts`).
- **Reasoning:** These enhancements were added to bridge the gap between simple list storage and intelligent scheduling, ensuring users can view their day in order and catch scheduling overlaps immediately.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- **Constraints considered:** The scheduler primarily evaluates task execution times (`HH:MM` format), pet assignments, and completion statuses.
- **Priority decision:** Chronological ordering and time-based conflict detection were prioritized because pet care tasks (such as medication or time-sensitive walks) require strict adherence to daily timelines to ensure animal well-being.

**b. Tradeoffs**

- **Tradeoff made:** The scheduler checks for time conflicts using exact string matches on the task `time` attribute rather than calculating complex time-interval overlaps or durations.
- **Why it's reasonable:** For a lightweight, day-to-day pet management prototype, exact-time matching provides quick, reliable conflict warnings without introducing unnecessary date-time parsing overhead, keeping the codebase clean and maintainable.

---

## 3. AI Collaboration

**a. How you used AI**

- **Workflow usage:** AI tools were utilized across multiple phases, including brainstorming Python `dataclasses` skeletons, generating Mermaid.js UML diagrams, configuring Streamlit's `st.session_state` for data persistence, and drafting automated `pytest` test cases.
- **Helpful prompts:** Asking the AI to explain how the `Scheduler` should cleanly extract tasks across multiple pet objects and how to structure lambda keys for time-sorting proved most effective.

**b. Judgment and verification**

- **Evaluation moment:** When drafting the recurrence and conflict detection logic, initial AI suggestions occasionally returned complex loops. The logic was reviewed and refactored to use cleaner Pythonic dictionary lookups for performance and readability.
- **Verification method:** Every AI-assisted code snippet was rigorously verified by running standalone CLI demo scripts (`main.py`) and executing the automated test suite (`pytest`) to ensure zero regressions.

---

## 4. Testing and Verification

**a. What you tested**

- **Behaviors tested:** The automated test suite (`test_pawpal.py`) verified core behaviors including task completion status updates, successful task additions to pet records, chronological sorting correctness, and conflict detection flagging.
- **Importance:** These tests guaranteed that the backend logic layer remained robust and deterministic before wiring it into the Streamlit UI.

**b. Confidence**

- **Confidence level:** ⭐⭐⭐⭐⭐ (5/5). All automated tests pass successfully (`3 passed in 0.08s`), and the application behavior has been verified locally via both CLI and browser.
- **Next edge cases:** If given more time, test cases would be expanded to cover handling pets with zero tasks, overlapping multi-hour task windows, and automated date-increment calculations for recurring weekly tasks.

---

## 5. Reflection

**a. What went well**

- The transition from a CLI-first backend (`pawpal_system.py` and `main.py`) to a fully interactive Streamlit web application (`app.py`) went remarkably smoothly, resulting in a clean separation of concerns between business logic and presentation.

**b. What you would improve**

- In another iteration, data persistence would be added via a local `data.json` file or lightweight database so that user-added pets and tasks are saved between application reboots.

**c. Key takeaway**

- The most important takeaway is that effective AI-assisted engineering requires strong human oversight. Acting as the lead architect—defining clear architectural boundaries, verifying outputs with automated tests, and guiding implementation choices—is essential to building maintainable systems.
