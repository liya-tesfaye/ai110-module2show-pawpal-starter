"""Demo script for PawPal+: builds a small owner/pet/task setup and prints a plan."""

from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler

PRIORITY_LABELS = {1: "high", 2: "medium", 3: "low"}


def main() -> None:
    # 1-2. Create the owner.
    alex = Owner(name="Alex", preferences={})

    # 3. Create two pets and add them to the owner.
    biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3, notes="")
    mochi = Pet(name="Mochi", species="cat", breed="Domestic Shorthair", age=5, notes="")
    alex.add_pet(biscuit)
    alex.add_pet(mochi)

    # 4. Add tasks with different times, priorities, and pet_names.
    biscuit.add_task(
        Task("Morning walk", "Biscuit", 30, 1, "exercise", time(8, 0), "daily", False)
    )
    biscuit.add_task(
        Task("Feeding", "Biscuit", 10, 1, "food", time(9, 0), "daily", False)
    )
    mochi.add_task(
        Task("Litter cleaning", "Mochi", 15, 2, "hygiene", time(9, 30), "daily", False)
    )
    mochi.add_task(
        Task("Play session", "Mochi", 20, 3, "enrichment", time(18, 0), "daily", False)
    )

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

    # 7. Print the reasoning below the schedule.
    print("\nWhy this plan:")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
