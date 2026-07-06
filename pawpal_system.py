"""PawPal+ system skeleton: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass


@dataclass
class Pet:
    """Represents an individual pet owned by an Owner."""

    name: str
    species: str
    breed: str
    age: int
    notes: str


@dataclass
class Task:
    """Represents a single pet-care task and its scheduling attributes."""

    name: str
    duration: int
    priority: str
    category: str
    preferred_time: str
    recurrence: str
    completed: bool

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        # TODO: implement

    def conflicts_with(self, other_task: "Task") -> bool:
        """Return True if this task conflicts with another task."""
        # TODO: implement


class Owner:
    """Holds owner info, their pets, a shared task list, and preferences."""

    def __init__(self, name: str, preferences: dict) -> None:
        self.name: str = name
        self.preferences: dict = preferences
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        # TODO: implement

    def remove_pet(self, name: str) -> None:
        """Remove a pet from this owner's list of pets by name."""
        # TODO: implement

    def get_pet(self, name: str) -> Pet:
        """Return the owner's pet matching the given name."""
        # TODO: implement

    def add_task(self, task: Task) -> None:
        """Add a task to this owner's shared task list."""
        # TODO: implement

    def remove_task(self, task: Task) -> None:
        """Remove a task from this owner's shared task list."""
        # TODO: implement


class Scheduler:
    """Builds a daily plan from a set of tasks within an available time budget."""

    def __init__(self, available_time: int, tasks: list[Task]) -> None:
        self.available_time: int = available_time
        self.tasks: list[Task] = tasks

    def sort_tasks_by_priority(self) -> list[Task]:
        """Return the tasks sorted by priority."""
        # TODO: implement

    def detect_conflicts(self) -> list:
        """Return the set of conflicting tasks."""
        # TODO: implement

    def build_daily_plan(self) -> list[Task]:
        """Return a sorted list of tasks that make up the daily plan."""
        # TODO: implement

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        # TODO: implement
