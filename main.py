from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Alex", preferences="Prefers morning walks")

    dog = Pet(name="Max", species="Dog", breed="Golden Retriever", age=3)
    cat = Pet(name="Luna", species="Cat", breed="Siamese", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Added OUT of chronological order on purpose
    dog.add_task(Task("Evening Walk", "18:30", frequency="daily"))
    cat.add_task(Task("Brushing", "14:00", frequency="weekly"))
    dog.add_task(Task("Morning Walk", "08:00", frequency="daily"))
    cat.add_task(Task("Lunch Snack", "12:00", frequency="daily"))

    scheduler = Scheduler()

    print(f"\n=== {owner.name}'s Raw Task List (unsorted) ===")
    for pet_name, task in scheduler.get_tasks(owner):
        print(f"  {pet_name:5} | {task.time} | {task.description}")

    print(f"\n=== Sorted by Time ===")
    for pet_name, task in scheduler.sort_by_time(owner):
        print(f"  {task.time} | {pet_name:5} | {task.description} [{task.status}]")

    print(f"\n=== Pending Tasks Only ===")
    for pet_name, task in scheduler.filter_by_status(owner, "pending"):
        print(f"  {task.time} | {pet_name:5} | {task.description}")

    print(f"\n=== Max's Tasks Only ===")
    for pet_name, task in scheduler.filter_by_pet(owner, "Max"):
        print(f"  {task.time} | {task.description}")

    # Force a conflict: Luna now has a task at 08:00, same as Max's Morning Walk
    cat.add_task(Task("Vet Visit", "08:00", frequency="once"))
    print(f"\n=== Conflict Detection ===")
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for w in conflicts:
            print(f"  {w}")
    else:
        print("  No conflicts detected.")

    # Recurrence
    morning = dog.get_tasks()[1]   # the 08:00 Morning Walk
    next_task = morning.mark_complete()
    print(f"\n=== Recurrence ===")
    print(f"  '{morning.description}' marked '{morning.status}'.")
    if next_task:
        dog.add_task(next_task)
        print(f"  New recurring task auto-created: '{next_task.description}' at {next_task.time} ({next_task.status})")


if __name__ == "__main__":
    main()