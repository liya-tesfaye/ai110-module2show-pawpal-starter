# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

**Scheduling logic (`pawpal_system.py`)**

- **Priority-based sorting** — `Scheduler.sort_tasks_by_priority()` orders tasks by an integer priority (1 = high, 2 = medium, 3 = low).
- **Time-based sorting** — `Scheduler.sort_by_time()` orders tasks chronologically by `preferred_time`, placing untimed tasks (no `preferred_time`) last.
- **Filtering** — `Scheduler.filter_tasks(pet_name, completed)` filters by pet name and/or completion status; both filters are optional and can be combined.
- **Conflict detection** — `Task.conflicts_with()` compares two tasks' half-open time intervals `[start, start + duration)`; `Scheduler.detect_conflicts()` returns every overlapping pair.
- **Readable conflict warnings** — `Scheduler.get_conflict_warnings()` turns each conflict into a plain-English string (returns an empty list when there are no conflicts).
- **Automatic recurrence** — `Task.complete_and_recur()` marks a task done and, for `"daily"`/`"weekly"` recurrence, returns a new occurrence with its `due_date` shifted forward by 1 or 7 days; `Owner.complete_task()` adds that occurrence back to the pet.
- **Greedy daily planning** — `Scheduler.build_daily_plan()` schedules tasks in priority order, skipping completed tasks, tasks that exceed the remaining time budget, and tasks that conflict with already-scheduled ones.
- **Plan explanation** — `Scheduler.explain_plan()` returns a per-task reason for why each task was included or skipped.
- **Owner / pet / task management** — add and remove pets (`Owner.add_pet`/`remove_pet`/`get_pet`), manage a pet's own task list (`Pet.add_task`/`remove_task`/`get_tasks_by_priority`), and gather all tasks across pets (`Owner.get_all_tasks`).

**Streamlit app (`app.py`)**

- Add pets and tasks through forms, with the `Owner` persisted across reruns via `st.session_state`.
- "Today's Schedule" view sorts tasks chronologically and lays them out in columns (time, task, priority, status).
- Filter controls (a per-pet dropdown and a "show completed" checkbox) that drive `filter_tasks()`.
- Inline conflict warnings shown with `st.warning()` directly next to the conflicting tasks.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

PS C:\Users\DSU\ai110-module2show-pawpal-starter> python main.py
================================================
Today's Schedule for Alex
================================================
  09:00  Feeding (Biscuit) [priority: high]
  08:00  Morning walk (Biscuit) [priority: high]
  18:00  Play session (Mochi) [priority: low]
================================================

Conflicts:
  ⚠️ Conflict: 'Morning walk' (Biscuit, 8:00) overlaps with 'Vet checkup' (Mochi, 8:15)

Why this plan:
Feeding: included (10 min, 110 min remaining)
Morning walk: included (30 min, 80 min remaining)
Vet checkup: skipped: conflicts with Morning walk
Litter cleaning: skipped: already completed
Play session: included (20 min, 60 min remaining)

Tasks added (insertion order):
  no-date 09:00  Feeding (Biscuit) [priority: high, todo]
  2026-07-06 08:00  Morning walk (Biscuit) [priority: high, todo]
  no-date 18:00  Play session (Mochi) [priority: low, todo]
  no-date 08:15  Vet checkup (Mochi) [priority: high, todo]
  no-date 09:30  Litter cleaning (Mochi) [priority: medium, done]

Sorted by time (sort_by_time):
  2026-07-06 08:00  Morning walk (Biscuit) [priority: high, todo]
  no-date 08:15  Vet checkup (Mochi) [priority: high, todo]
  no-date 09:00  Feeding (Biscuit) [priority: high, todo]
  no-date 09:30  Litter cleaning (Mochi) [priority: medium, done]
  no-date 18:00  Play session (Mochi) [priority: low, todo]

Biscuit's tasks (filter_tasks(pet_name='Biscuit')):
  no-date 09:00  Feeding (Biscuit) [priority: high, todo]
  2026-07-06 08:00  Morning walk (Biscuit) [priority: high, todo]

Incomplete tasks (filter_tasks(completed=False)):
  no-date 09:00  Feeding (Biscuit) [priority: high, todo]
  2026-07-06 08:00  Morning walk (Biscuit) [priority: high, todo]
  no-date 18:00  Play session (Mochi) [priority: low, todo]
  no-date 08:15  Vet checkup (Mochi) [priority: high, todo]

Recurrence:
  before:    2026-07-06 08:00  Morning walk (Biscuit) [priority: high, todo]
  completed: 2026-07-06 08:00  Morning walk (Biscuit) [priority: high, done]
  next:      2026-07-07 08:00  Morning walk (Biscuit) [priority: high, todo]

Biscuit's tasks after completing the walk:
  no-date 09:00  Feeding (Biscuit) [priority: high, todo]
  2026-07-06 08:00  Morning walk (Biscuit) [priority: high, done]
  2026-07-07 08:00  Morning walk (Biscuit) [priority: high, todo]
PS C:\Users\DSU\ai110-module2show-pawpal-starter> 


## 🧪 Testing PawPal+

## 🧪 Testing PawPal+

Our test suite covers:
- **Task completion** — verifying `mark_complete()` correctly updates status
- **Task addition** — verifying adding a task increases a pet's task count
- **Sorting correctness** — verifying tasks are returned in chronological order
- **Recurrence logic** — verifying a completed daily/weekly task generates a 
  correctly-dated next occurrence
- **Conflict detection** — verifying overlapping tasks are flagged, and 
  non-overlapping tasks are not

\```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
\```

Sample test output:

\```
PS C:\Users\DSU\ai110-module2show-pawpal-starter> python -m pytest
================================================== test session starts ==================================================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\DSU\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 13 items

tests\test_pawpal.py .............                                                                                 [100%]

================================================== 13 passed in 0.05s ===================================================
\```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5)

All 13 tests pass, covering the core scheduling behaviors: sorting, filtering, 
conflict detection, recurrence, and basic task/pet management. I'd rate this 
a 4 rather than a 5 because coverage is focused on core logic rather than 
exhaustive edge cases (e.g., very large task lists, timezone edge cases, or 
malformed input from the UI layer).

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_tasks_by_priority()` | Sorts tasks chronologically by `preferred_time` (untimed tasks last), or by priority with 1 = high first. |
| Filtering | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Returns tasks filtered by pet name and/or completion status; both filters are optional and can be combined. |
| Conflict handling | `Scheduler.detect_conflicts()`, `Scheduler.get_conflict_warnings()`, `Task.conflicts_with()` | Detects pairs of tasks whose time intervals overlap and turns them into readable warning strings. |
| Recurring tasks | `Task.complete_and_recur()`, `Owner.complete_task()` | Completing a daily/weekly task returns a new occurrence with its `due_date` shifted forward (1 or 7 days) and re-adds it to the pet's task list. |

## 📸 Demo Walkthrough

1. On launch, the user enters their name to create an `Owner`, which is 
   stored in `st.session_state` so it persists across interactions.
2. The user adds one or more pets (name, species/breed, age) through the 
   "Add Pet" form; each new pet appears in a list immediately after submission.
3. The user adds care tasks (description, pet, time, priority, duration, 
   recurrence) through the "Add Task" form. Each task is linked to a specific 
   pet via a dropdown populated from the pets already added.
4. The app displays "Today's Schedule," built from `Scheduler.build_daily_plan()` 
   and sorted chronologically by `sort_by_time()`, laid out in columns showing 
   time, task, pet, priority, and status.
5. If two tasks overlap in time, a warning generated by 
   `get_conflict_warnings()` appears inline via `st.warning()` next to the 
   affected tasks, so the owner immediately sees which tasks conflict.
6. The user can narrow the schedule view using the pet dropdown filter and 
   the "show completed" checkbox, both powered by `filter_tasks()`.
7. Marking a daily or weekly task complete triggers `complete_and_recur()`, 
   which automatically schedules the next occurrence — it appears the next 
   time the schedule is viewed.

