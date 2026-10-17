from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner
    owner = Owner(name="Alex", preferences="Prefers morning walks")

    # 2. Create at least two Pets
    dog = Pet(name="Max", species="Dog", breed="Golden Retriever", age=3)
    cat = Pet(name="Luna", species="Cat", breed="Siamese", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # 3. Add at least three Tasks with different times
    dog.add_task(Task(description="Morning Walk", time="08:00", frequency="daily"))
    dog.add_task(Task(description="Dinner & Medication", time="18:30", frequency="daily"))
    cat.add_task(Task(description="Brushing", time="14:00", frequency="weekly"))

    # 4. Use the Scheduler to display today's schedule
    scheduler = Scheduler()
    schedule = scheduler.organize_tasks(owner)

    print(f"\n--- Today's Schedule for {owner.name}'s Pets ---")
    for pet_name, task in schedule:
        print(f"Pet: {pet_name} | Task: {task.description} | Time: {task.time} | Status: {task.status}")

if __name__ == "__main__":
    main()
