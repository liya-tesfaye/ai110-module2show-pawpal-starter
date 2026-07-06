"""Tests for core PawPal+ behaviors."""

from datetime import time

from pawpal_system import Pet, Task


def make_task() -> Task:
    """Build a simple, incomplete Task for use in tests."""
    return Task(
        name="Morning walk",
        pet_name="Biscuit",
        duration=30,
        priority=1,
        category="exercise",
        preferred_time=time(8, 0),
        recurrence="daily",
        completed=False,
    )


def test_mark_complete():
    task = make_task()
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3, notes="")
    assert len(pet.tasks) == 0

    pet.add_task(make_task())

    assert len(pet.tasks) == 1
