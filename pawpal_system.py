"""PawPal+ system skeleton: Owner, Pet, Task, and Scheduler classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta

# Recurrence values that cause a completed task to become due again.
RECURRING_INTERVALS = {"daily", "weekly"}


def _format_clock(t: time | None) -> str:
    """Format a time as e.g. '8:00', or '??:??' if it is None."""
    if t is None:
        return "??:??"
    return f"{t.hour}:{t.minute:02d}"


@dataclass
class Task:
    """Represents a single pet-care task and its scheduling attributes."""

    name: str
    pet_name: str
    duration: int
    priority: int  # 1 = high, 2 = medium, 3 = low
    category: str
    preferred_time: time
    recurrence: str
    completed: bool
    # The calendar day the task is due. preferred_time is only the time of day,
    # so recurrence shifts this date forward. Optional for one-off/undated tasks.
    due_date: date | None = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def conflicts_with(self, other_task: "Task") -> bool:
        """Return True if this task's time interval overlaps other_task's."""
        # Only meaningful if both tasks have a preferred start time.
        if self.preferred_time is None or other_task.preferred_time is None:
            return False

        start_self = self.preferred_time.hour * 60 + self.preferred_time.minute
        end_self = start_self + self.duration
        start_other = other_task.preferred_time.hour * 60 + other_task.preferred_time.minute
        end_other = start_other + other_task.duration

        # Half-open intervals [start, end) overlap when each starts before the
        # other ends.
        return start_self < end_other and start_other < end_self

    def reset_for_next_occurrence(self) -> bool:
        """If this task recurs, mark it due again and return True; else False."""
        if self.recurrence in RECURRING_INTERVALS:
            self.completed = False
            return True
        return False

    def complete_and_recur(self) -> "Task | None":
        """Mark this task complete; if it recurs, return the next occurrence.

        Returns a new incomplete Task copy whose due_date is shifted forward
        (1 day for "daily", 7 days for "weekly"), or None if the task does not
        recur. The original task keeps its due_date and is marked completed.
        """
        self.completed = True
        if self.recurrence not in RECURRING_INTERVALS:
            return None

        # timedelta gives the gap to the next occurrence; adding it to a date
        # yields the next due date. A weekly task jumps 7 days, a daily one 1.
        shift = timedelta(days=7) if self.recurrence == "weekly" else timedelta(days=1)
        next_due = self.due_date + shift if self.due_date is not None else None

        return Task(
            name=self.name,
            pet_name=self.pet_name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            preferred_time=self.preferred_time,
            recurrence=self.recurrence,
            completed=False,
            due_date=next_due,
        )


@dataclass
class Pet:
    """Represents an individual pet and the care tasks belonging to it."""

    name: str
    species: str
    breed: str
    age: int
    notes: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks_by_priority(self) -> list[Task]:
        """Return this pet's tasks sorted by priority ascending (1 = high first)."""
        return sorted(self.tasks, key=lambda task: task.priority)


class Owner:
    """Holds owner info, their pets, and preferences."""

    def __init__(self, name: str, preferences: dict | None = None) -> None:
        """Initialize an owner with a name, preferences, and an empty pet list."""
        self.name: str = name
        self.preferences: dict = preferences if preferences is not None else {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove a pet from this owner's list of pets by name."""
        self.pets = [pet for pet in self.pets if pet.name != name]

    def get_pet(self, name: str) -> Pet:
        """Return the owner's pet matching the given name, or None if not found."""
        return next((pet for pet in self.pets if pet.name == name), None)

    def get_all_tasks(self) -> list[Task]:
        """Gather and return the tasks from every pet the owner has."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and, if it recurs, add its next occurrence back."""
        next_task = task.complete_and_recur()
        if next_task is not None:
            self.get_pet(next_task.pet_name).add_task(next_task)
        return next_task


class Scheduler:
    """Builds a daily plan from a set of tasks within an available time budget."""

    def __init__(self, available_time: int, tasks: list[Task], preferences: dict) -> None:
        """Initialize the scheduler with a time budget, tasks, and preferences."""
        self.available_time: int = available_time
        self.tasks: list[Task] = tasks
        self.preferences: dict = preferences

    def sort_tasks_by_priority(self) -> list[Task]:
        """Return the tasks sorted by priority ascending (1 = high first)."""
        return sorted(self.tasks, key=lambda task: task.priority)

    def sort_by_time(self) -> list[Task]:
        """Return self.tasks sorted by preferred_time ascending; None times last."""
        # Compare on the time objects directly. The first key element pushes
        # tasks with no preferred_time to the end, and time.max stands in for
        # None so the sort never compares None against a time.
        return sorted(
            self.tasks,
            key=lambda task: (task.preferred_time is None, task.preferred_time or time.max),
        )

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:
        """Return self.tasks filtered by pet name and/or completion status.

        Both filters are optional and combine: omit an argument (leave it None)
        to skip that filter.
        """
        result = list(self.tasks)
        if pet_name is not None:
            result = [task for task in result if task.pet_name == pet_name]
        if completed is not None:
            result = [task for task in result if task.completed == completed]
        return result

    def regenerate_completed_recurring(self) -> list[Task]:
        """Reset completed recurring tasks so they are due again; return them."""
        return [
            task
            for task in self.tasks
            if task.completed and task.reset_for_next_occurrence()
        ]

    def get_conflict_warnings(self) -> list[str]:
        """Return a readable warning string per conflicting pair; [] if none."""
        warnings: list[str] = []
        for a, b in self.detect_conflicts():
            warnings.append(
                f"⚠️ Conflict: '{a.name}' ({a.pet_name}, {_format_clock(a.preferred_time)}) "
                f"overlaps with '{b.name}' ({b.pet_name}, {_format_clock(b.preferred_time)})"
            )
        return warnings

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return every pair of tasks whose time intervals overlap."""
        conflicts: list[tuple[Task, Task]] = []
        for i in range(len(self.tasks)):
            for j in range(i + 1, len(self.tasks)):
                if self.tasks[i].conflicts_with(self.tasks[j]):
                    conflicts.append((self.tasks[i], self.tasks[j]))
        return conflicts

    def build_daily_plan(self) -> list[Task]:
        """Greedily schedule tasks by priority within time and conflict limits."""
        scheduled: list[Task] = []
        remaining_time = self.available_time

        for task in self.sort_tasks_by_priority():
            if task.completed:
                continue
            if task.duration > remaining_time:
                continue
            if any(task.conflicts_with(other) for other in scheduled):
                continue

            scheduled.append(task)
            remaining_time -= task.duration

        return scheduled

    def explain_plan(self) -> str:
        """Explain why each task was included in or skipped from the plan."""
        lines: list[str] = []
        scheduled: list[Task] = []
        remaining_time = self.available_time

        for task in self.sort_tasks_by_priority():
            if task.completed:
                lines.append(f"{task.name}: skipped: already completed")
                continue
            if task.duration > remaining_time:
                lines.append(f"{task.name}: skipped: not enough time remaining")
                continue

            conflict = next(
                (other for other in scheduled if task.conflicts_with(other)), None
            )
            if conflict is not None:
                lines.append(f"{task.name}: skipped: conflicts with {conflict.name}")
                continue

            scheduled.append(task)
            remaining_time -= task.duration
            lines.append(
                f"{task.name}: included ({task.duration} min, {remaining_time} min remaining)"
            )

        return "\n".join(lines)
