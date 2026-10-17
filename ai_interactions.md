# AI Interactions Log

---

## Agent Workflow (SF7)

**What task did you give the agent?**

I asked my AI assistant if it would be simpler to move the task lists out of the `Pet` class and store all tasks centrally inside the `Scheduler` class instead. I just wanted to see if it made the code cleaner.

**What did the agent do?**

The AI agreed it was a good idea and went ahead and changed everything automatically. It removed the task lists from `Pet` and deleted `Owner.get_all_tasks()`. It moved all tasks into a central list inside `Scheduler`. Then it updated my `main.py`, rewrote `test_pawpal.py`, and even changed my `README.md` and `reflection.md` to say I made this change. It reported that "12 tests passed," so it looked like it worked perfectly.

**What did you have to verify or fix manually?**

I had to fix everything because the AI's change actually broke the project rules. My Phase 2 instructions specifically said the Scheduler must read from `Owner.get_all_tasks()` to get the multi-pet points. By deleting that method, the AI made me fail the requirement. It also broke my UML diagram (Pet is supposed to _have_ Tasks).

I used `git restore` to undo the AI's changes to my code files. The AI had overwritten some of my tests that I hadn't saved in Git yet, so I had to paste those 8 tests back in. Then I manually went into my `README.md` and `reflection.md` and deleted the paragraphs the AI wrote about moving the tasks, because I rejected that idea.

This taught me that even if an AI makes all the tests pass, it can still be wrong. It just rewrote the tests to match its new broken code. I had to be the "lead architect" and check the code against the actual instructions.

---

## Prompt Comparison (SF11)

I asked the AI to show me two ways to detect scheduling conflicts.

|                     | Option A (Pairwise)                      | Option B (Dictionary)                                          |
| ------------------- | ---------------------------------------- | -------------------------------------------------------------- |
| **Tool used**       | VS Code AI                               | VS Code AI                                                     |
| **Prompt**          | "Find conflicts using a nested loop."    | "Find conflicts using a dictionary."                           |
| **Response**        | Compares every task to every other task. | Groups tasks by time in one pass.                              |
| **What was useful** | Easy to read and returns exact pairs.    | Much shorter, cleaner code.                                    |
| **Problems**        | Very slow (O(n²)).                       | Returned a dictionary instead of the warning strings I needed. |
| **Decision**        | Rejected                                 | Used in final code                                             |

**Which approach did you use and why?**
I used Option B. Even though I had to tweak it to output warning strings, grouping tasks in a single pass was cleaner and fit perfectly with my final UI warnings.
