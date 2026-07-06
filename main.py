"""Demo script for PawPal+: builds a small owner/pet/task setup and prints a plan."""

import sys
from datetime import date, time

from pawpal_system import Owner, Pet, Task, Scheduler

# Windows terminals default to cp1252, which can't encode emoji like ⚠️.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PRIORITY_LABELS = {1: "high", 2: "medium", 3: "low"}
TODAY = date(2026, 7, 6)


def format_task(task: Task) -> str:
    """Return a one-line summary of a task for printing."""
    day = task.due_date.isoformat() if task.due_date else "no-date"
    clock = task.preferred_time.strftime("%H:%M") if task.preferred_time else "--:--"
    priority = PRIORITY_LABELS.get(task.priority, str(task.priority))
    status = "done" if task.completed else "todo"
    return f"{day} {clock}  {task.name} ({task.pet_name}) [priority: {priority}, {status}]"


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a titled list of tasks."""
    print(f"\n{title}")
    for task in tasks:
        print(f"  {format_task(task)}")


def main() -> None:
    # 1-2. Create the owner.
    alex = Owner(name="Alex", preferences={})

    # 3. Create two pets and add them to the owner.
    biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3, notes="")
    mochi = Pet(name="Mochi", species="cat", breed="Domestic Shorthair", age=5, notes="")
    alex.add_pet(biscuit)
    alex.add_pet(mochi)

    # 4. Add tasks deliberately OUT of time order (6pm before 9am) and with a
    #    mix of completion statuses.
    mochi.add_task(
        Task("Play session", "Mochi", 20, 3, "enrichment", time(18, 0), "daily", False)
    )
    # Overlaps the 8:00 Morning walk to demonstrate conflict warnings.
    mochi.add_task(
        Task("Vet checkup", "Mochi", 45, 1, "health", time(8, 15), "none", False)
    )
    biscuit.add_task(
        Task("Feeding", "Biscuit", 10, 1, "food", time(9, 0), "daily", False)
    )
    mochi.add_task(
        Task("Litter cleaning", "Mochi", 15, 2, "hygiene", time(9, 30), "daily", True)
    )
    morning_walk = Task(
        "Morning walk", "Biscuit", 30, 1, "exercise", time(8, 0), "daily", False,
        due_date=TODAY,
    )
    biscuit.add_task(morning_walk)

    # 5. Build a scheduler from the owner's combined task list.
    scheduler = Scheduler(
        available_time=120,
        tasks=alex.get_all_tasks(),
        preferences=alex.preferences,
    )

    # 6. Build and print the daily plan.
    plan = scheduler.build_daily_plan()

    print("=" * 48)
    print(f"Today's Schedule for {alex.name}")
    print("=" * 48)
    for task in plan:
        clock = task.preferred_time.strftime("%H:%M")
        priority = PRIORITY_LABELS.get(task.priority, str(task.priority))
        print(f"  {clock}  {task.name} ({task.pet_name}) [priority: {priority}]")
    print("=" * 48)

    # Warn about any overlapping tasks (empty list -> nothing printed).
    warnings = scheduler.get_conflict_warnings()
    if warnings:
        print("\nConflicts:")
        for warning in warnings:
            print(f"  {warning}")

    # 7. Print the reasoning below the schedule.
    print("\nWhy this plan:")
    print(scheduler.explain_plan())

    # 8. Demonstrate the sorting and filtering helpers.
    print_tasks("Tasks added (insertion order):", scheduler.tasks)
    print_tasks("Sorted by time (sort_by_time):", scheduler.sort_by_time())
    print_tasks(
        "Biscuit's tasks (filter_tasks(pet_name='Biscuit')):",
        scheduler.filter_tasks(pet_name="Biscuit"),
    )
    print_tasks(
        "Incomplete tasks (filter_tasks(completed=False)):",
        scheduler.filter_tasks(completed=False),
    )

    # 9. Complete a recurring task; its next occurrence is auto-generated and
    #    added back to the owner's task list.
    print("\nRecurrence:")
    print(f"  before:    {format_task(morning_walk)}")
    next_walk = alex.complete_task(morning_walk)
    print(f"  completed: {format_task(morning_walk)}")
    if next_walk is not None:
        print(f"  next:      {format_task(next_walk)}")
    print_tasks("Biscuit's tasks after completing the walk:", biscuit.tasks)


if __name__ == "__main__":
    main()
