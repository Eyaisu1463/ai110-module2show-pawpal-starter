from pawpal_system import Owner, Pet, Task, Scheduler

def test_task_completion():
    task = Task(description="Feeding", time="08:00")
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "completed"

def test_pet_add_task():
    pet = Pet(name="Max", species="Dog")
    task = Task(description="Walk", time="07:00")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].description == "Walk"

def test_scheduler_organization():
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="Cat")
    owner.add_pet(pet)
    
    task = Task(description="Brush", time="12:00")
    pet.add_task(task)
    
    scheduler = Scheduler()
    schedule = scheduler.organize_tasks(owner)
    
    assert len(schedule) == 1
    assert schedule[0][0] == "Luna"
    assert schedule[0][1].description == "Brush"
