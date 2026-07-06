"""Tests for core PawPal+ behaviors."""

from datetime import date, time, timedelta

from pawpal_system import Pet, Task, Scheduler


def make_task(**overrides) -> Task:
    """Build a Task with sensible defaults; pass keywords to override any field."""
    defaults = dict(
        name="Morning walk",
        pet_name="Biscuit",
        duration=30,
        priority=1,
        category="exercise",
        preferred_time=time(8, 0),
        recurrence="daily",
        completed=False,
    )
    defaults.update(overrides)
    return Task(**defaults)


# --- Existing core behaviors -------------------------------------------------

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


# --- Sorting -----------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    # Tasks added out of order should come back sorted by preferred_time.
    evening = make_task(name="Evening", preferred_time=time(18, 0))
    morning = make_task(name="Morning", preferred_time=time(8, 0))
    noon = make_task(name="Noon", preferred_time=time(12, 0))
    scheduler = Scheduler(available_time=120, tasks=[evening, morning, noon], preferences={})

    ordered = scheduler.sort_by_time()

    assert [t.name for t in ordered] == ["Morning", "Noon", "Evening"]


def test_sort_by_time_places_untimed_task_last():
    # A task with no preferred_time should sort to the end, not raise.
    timed = make_task(name="Timed", preferred_time=time(9, 0))
    untimed = make_task(name="Untimed", preferred_time=None)
    scheduler = Scheduler(available_time=120, tasks=[untimed, timed], preferences={})

    ordered = scheduler.sort_by_time()

    assert [t.name for t in ordered] == ["Timed", "Untimed"]


# --- Recurrence --------------------------------------------------------------

def test_daily_recurrence_creates_task_one_day_later():
    # Completing a daily task returns a fresh task due exactly one day later.
    start_date = date(2026, 7, 6)
    task = make_task(recurrence="daily", preferred_time=time(8, 0), due_date=start_date)

    next_task = task.complete_and_recur()

    assert task.completed is True             # original is marked done
    assert next_task is not None
    assert next_task.completed is False       # the new occurrence is not done
    assert next_task.due_date == start_date + timedelta(days=1)  # precise +1 day
    assert next_task.preferred_time == time(8, 0)  # time of day is unchanged


def test_weekly_recurrence_shifts_seven_days():
    # A weekly task's next occurrence is due exactly seven days later.
    start_date = date(2026, 7, 6)
    task = make_task(recurrence="weekly", due_date=start_date)

    next_task = task.complete_and_recur()

    assert next_task is not None
    assert next_task.due_date == start_date + timedelta(days=7)


def test_recurring_completed_multiple_times_advances_due_date():
    # Completing successive occurrences should keep advancing the due date.
    start_date = date(2026, 7, 6)
    task = make_task(recurrence="daily", due_date=start_date)

    second = task.complete_and_recur()
    third = second.complete_and_recur()

    assert second.due_date == start_date + timedelta(days=1)
    assert third.due_date == start_date + timedelta(days=2)


def test_non_recurring_task_returns_none_on_complete():
    # A one-off task is completed but generates no next occurrence.
    task = make_task(recurrence="none")

    result = task.complete_and_recur()

    assert result is None
    assert task.completed is True


# --- Conflict detection ------------------------------------------------------

def test_tasks_at_same_time_conflict():
    # Two tasks starting at the same time overlap, even across different pets.
    walk = make_task(name="Morning walk", pet_name="Biscuit", preferred_time=time(8, 0))
    vet = make_task(name="Vet checkup", pet_name="Mochi", preferred_time=time(8, 0))
    scheduler = Scheduler(available_time=120, tasks=[walk, vet], preferences={})

    assert len(scheduler.detect_conflicts()) == 1
    assert len(scheduler.get_conflict_warnings()) == 1


def test_tasks_at_different_times_do_not_conflict():
    # Non-overlapping tasks should produce no conflicts or warnings.
    walk = make_task(name="Walk", preferred_time=time(8, 0), duration=30)   # ends 8:30
    feed = make_task(name="Feed", preferred_time=time(10, 0), duration=30)
    scheduler = Scheduler(available_time=120, tasks=[walk, feed], preferences={})

    assert scheduler.detect_conflicts() == []
    assert scheduler.get_conflict_warnings() == []


def test_adjacent_tasks_do_not_conflict():
    # One task ending exactly when the next begins must NOT be a conflict,
    # because intervals are half-open [start, start + duration).
    first = make_task(name="First", preferred_time=time(8, 0), duration=30)   # 8:00-8:30
    second = make_task(name="Second", preferred_time=time(8, 30), duration=30)  # 8:30-9:00
    scheduler = Scheduler(available_time=120, tasks=[first, second], preferences={})

    assert scheduler.detect_conflicts() == []


def test_task_with_no_preferred_time_excluded_from_conflicts():
    # A task with preferred_time=None can't overlap anything and must not raise.
    timed = make_task(name="Walk", preferred_time=time(8, 0))
    untimed = make_task(name="Untimed", preferred_time=None)
    scheduler = Scheduler(available_time=120, tasks=[timed, untimed], preferences={})

    assert timed.conflicts_with(untimed) is False
    assert scheduler.detect_conflicts() == []


# --- Empty / boundary cases --------------------------------------------------

def test_pet_with_no_tasks_returns_empty():
    # A pet with no tasks and a scheduler over an empty list stay well-behaved.
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3, notes="")
    assert pet.get_tasks_by_priority() == []

    scheduler = Scheduler(available_time=120, tasks=[], preferences={})
    assert scheduler.build_daily_plan() == []
    assert scheduler.get_conflict_warnings() == []
