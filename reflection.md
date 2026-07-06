# PawPal+ Project Reflection

## 1. System Design

## System Design

### Core Actions

When I read through the PawPal+ scenario, I identified three core actions a pet owner should be able to perform:

1. **Add and manage pet care tasks** — The owner needs to be able to enter tasks like walks, feedings, medications, and grooming sessions, each with a duration and a priority level. This is the raw input the rest of the system depends on.

2. **Generate a daily plan** — Once tasks exist, the owner should be able to ask the app to build a schedule for the day. The system needs to take into account how much time is available, how important each task is, and any constraints (like a task needing to happen at a specific time), and produce an ordered plan that fits.

3. **View and understand the plan** — The owner should be able to see the generated schedule clearly (what happens when) and get some explanation of why the app chose that order — for example, why a high-priority task was scheduled before a lower-priority one, or why a task got dropped if there wasn't enough time.

These three actions map roughly to the three main pieces of the system I'll need to design: something that represents a task, something that represents a pet/owner's data, and something that does the actual scheduling logic.

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
