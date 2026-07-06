# PawPal+ Project Reflection

## 1. System Design

## System Design

### Core Actions

**a. Initial Design

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

**b. Design Changes

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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
