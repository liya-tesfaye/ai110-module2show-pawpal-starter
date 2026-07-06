# PawPal+ Project Reflection

## 1. System Design

## System Design

### Core Actions

**a. Initial Design**

I designed PawPal+ around four core classes, each with a single clear responsibility:

- **Owner** — Represents the pet owner using the app. Holds their list of pets, 
  their shared list of care tasks (one task list covering all their pets, rather 
  than per-pet task lists), and any scheduling preferences. Responsible for 
  managing which pets and tasks exist in the system.

- **Pet** — Represents an individual animal (name, species/breed, age, notes). 
  Implemented as a dataclass since it's mostly a data container with no complex 
  behavior of its own.

- **Task** — Represents a single care activity (walk, feeding, meds, etc.), with 
  duration, priority, category, timing info, and recurrence. Also a dataclass, 
  but includes methods like conflicts_with() since tasks need to check for 
  overlaps with each other.

- **Scheduler** — A separate class responsible for turning a pool of tasks into 
  an actual daily plan. It handles sorting by priority, detecting conflicts, and 
  building the final schedule. I kept this separate from Owner and Task so the 
  scheduling *logic* is isolated from the *data* — this should make it easier to 
  test and to change the scheduling algorithm later without touching Owner or Task.

I decided tasks live on Owner rather than on Pet, since in practice an owner is 
managing one daily schedule across all their pets, not a separate schedule per pet.

**b. Design Changes**

After reviewing my skeleton with my AI assistant, I made the following changes:

- **Added `pet_name` to Task** — Since tasks live in a shared list on Owner 
  rather than per-pet, there was no way to tell which pet a task belonged to. 
  My assistant pointed out this also validates keeping the task list on Owner 
  in the first place: a shared list lets the scheduler catch conflicts across 
  all pets (e.g., can't walk two dogs at the same time), which a per-pet list 
  would hide. Adding `pet_name` gets the benefit without losing per-pet detail.

- **Changed `priority` from str to int** — Sorting "high"/"medium"/"low" as 
  strings sorts alphabetically, not by actual priority. Using an int ranking 
  (1 = high, 2 = medium, 3 = low) makes sort_tasks_by_priority() correct and 
  simple.

- **Changed `preferred_time` from str to datetime.time** — String comparison 
  of times like "9:00" vs "10:00" doesn't sort correctly. Using datetime.time 
  makes ordering and future interval math (start time + duration) reliable.

- **Added a `preferences` parameter to Scheduler** — My original design didn't 
  give Scheduler access to owner preferences, even though the scenario requires 
  the plan to consider them. Rather than passing a whole Owner object (which 
  would couple Scheduler to Owner unnecessarily), I pass just the preferences 
  data it needs, keeping Scheduler easier to test in isolation.

I did not yet resolve the deeper semantic question my assistant raised — 
whether a "conflict" requires a true time interval (start + duration) rather 
than just a preferred_time point — since that's implementation logic I'll 
pin down in Phase 2, not a structural/skeleton change.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers three main constraints when building a daily plan:

- **Available time** — the total minutes the owner has available in a day. 
  `build_daily_plan()` stops adding tasks once this budget is used up, so 
  lower-priority tasks may get dropped rather than overflow the day.
- **Priority** — tasks are ranked 1 (high) to 3 (low) and sorted so the most 
  important tasks (like medications) are considered before optional ones 
  (like enrichment play) when time is tight.
- **Time conflicts** — tasks with overlapping preferred_time + duration 
  intervals can't both be scheduled, so the scheduler checks for overlaps 
  before finalizing the plan.

I decided priority mattered most, since a real pet owner would rather see a 
medication task guaranteed a spot than a lower-stakes task like grooming. 
Available time mattered next, since without it the plan could recommend more 
than a day can actually hold. Preferences (like "no tasks after 9pm") were 
treated as a secondary filter layered on top of these two, rather than a 
primary sorting factor, since they narrow the pool of valid times rather 
than rank tasks against each other.

**b. Tradeoffs**

My conflict detection only checks for overlapping time intervals based on 
preferred_time + duration. This means a few tradeoffs:

- Tasks with no preferred_time set are never checked for conflicts, since 
  there's no interval to compare. This keeps the logic simple but means the 
  scheduler could still silently schedule two "flexible" tasks back-to-back 
  without warning.
- I chose exact interval overlap (start/end times) rather than a fuzzier 
  "too close together" check (e.g., flagging tasks less than 15 minutes 
  apart). This is more predictable and easier to test, but it means a walk 
  ending at 8:00 and a feeding starting at 8:00 exactly are treated as 
  conflicting, even though back-to-back might be fine in practice for a real 
  owner.

I decided this tradeoff is acceptable for the scope of this project — a more 
nuanced buffer-time system would add real value but also real complexity 
(deciding buffer length per task type, etc.) that's beyond what this 
scheduler needs to demonstrate.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project for several distinct purposes: brainstorming 
the initial class design and UML relationships, scaffolding class skeletons 
from that design, generating first-pass implementations of scheduling logic 
(sorting, conflict detection, recurrence), drafting and debugging pytest 
tests, and reviewing my own code for gaps I hadn't noticed (like the missing 
Task → Pet link).

The most helpful prompts were the ones that asked for **review rather than 
generation** — e.g., "review this skeleton and tell me what relationships 
are missing" surfaced real design issues (the pet_name gap, the priority-as-
string sorting bug) that I hadn't caught myself. Prompts that specified exact 
constraints (e.g., "don't add anything beyond what I've listed") also 
produced cleaner results than open-ended "build me a scheduler" requests, 
which tended to over-build.

**b. Judgment and verification**

One moment I didn't accept an AI suggestion as-is: when I asked how to 
simplify `build_daily_plan()` for readability, the suggested version 
collapsed the sort/filter/conflict-check steps into a single chained 
comprehension. It was more compact, but harder to trace when something went 
wrong — I couldn't tell at a glance which step (sorting, time-budget 
filtering, or conflict avoidance) had produced a given result. I kept my 
original step-by-step version with named intermediate variables instead, 
since I judged debuggability to matter more than line count for this project.

I verified AI-generated logic mainly through the pytest suite — writing 
tests for sorting, recurrence, and conflict detection let me confirm the 
implementation actually matched what I asked for, rather than just assuming 
generated code was correct because it ran without errors.

---

## 4. Testing and Verification

**a. What you tested**

My test suite covers: task completion status changes, task addition 
increasing a pet's task count, sorting correctness (tasks returned in 
chronological order), recurrence logic (a completed daily/weekly task 
generates a correctly-dated next occurrence), and conflict detection 
(overlapping tasks are flagged, non-overlapping tasks are not).

These behaviors mattered most because they're the core "intelligence" of the 
app — a scheduler that sorts incorrectly, misses conflicts, or mishandles 
recurrence would give a pet owner an unreliable or even unsafe plan (e.g., a 
missed medication reminder). Simpler behaviors like adding a pet were tested 
too, since they're the foundation everything else depends on.

**b. Confidence**

I'm confident (4/5) that the core scheduling logic works correctly, since all 
13 tests pass and cover the main happy paths and a few key edge cases. If I 
had more time, I'd test: tasks with no preferred_time interacting with 
conflict detection, an owner with zero pets or zero tasks calling 
build_daily_plan(), a recurring task completed multiple days in a row, and 
performance with a much larger number of tasks.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the separation between Scheduler and the data 
classes (Owner, Pet, Task). Keeping scheduling logic out of Owner made it 
much easier to test in isolation and to reason about — I could change how 
build_daily_plan() worked without worrying about breaking pet or task 
management.

**b. What you would improve**

If I had another iteration, I'd redesign conflict detection to use a real 
buffer window (e.g., flag tasks less than 10 minutes apart, not just exact 
overlaps) and add proper date tracking to Task, rather than relying only on 
time-of-day, so recurrence and "today's schedule" logic would be more robust.

**c. Key takeaway**

The biggest thing I learned is that AI is very good at producing correct-
looking code quickly, but it can't decide what tradeoffs are right for a 
specific system — that stayed my responsibility throughout. Decisions like 
keeping tasks on Owner instead of Pet, or choosing readability over a 
"cleverer" one-liner, only made sense in the context of this specific app, 
and being the one who made and could explain those calls is what "lead 
architect" actually meant in practice.