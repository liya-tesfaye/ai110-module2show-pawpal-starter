"""PawPal+ system skeleton: Owner, Pet, Task, and Scheduler classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


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

    def __init__(self, name: str, preferences: dict) -> None:
        """Initialize an owner with a name, preferences, and an empty pet list."""
        self.name: str = name
        self.preferences: dict = preferences
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
