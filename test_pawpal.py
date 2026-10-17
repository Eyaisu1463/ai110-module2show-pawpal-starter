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

# ─── Phase 5: Algorithm tests ──────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    """Tasks should be sorted HH:MM ascending."""
    owner = Owner("A")
    pet = Pet("Max", "Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "18:00"))
    pet.add_task(Task("Feed", "08:00"))
    pet.add_task(Task("Play", "12:00"))

    s = Scheduler()
    ordered = [t.time for _, t in s.sort_by_time(owner)]
    assert ordered == ["08:00", "12:00", "18:00"]


def test_filter_by_status_returns_only_matching():
    """Only tasks matching the given status should return."""
    owner = Owner("A")
    pet = Pet("Max", "Dog")
    owner.add_pet(pet)
    t1 = Task("Walk", "08:00")
    t2 = Task("Feed", "12:00")
    pet.add_task(t1)
    pet.add_task(t2)
    t1.mark_complete()

    s = Scheduler()
    pending = s.filter_by_status(owner, "pending")
    completed = s.filter_by_status(owner, "completed")
    assert len(pending) == 1
    assert pending[0][1].description == "Feed"
    assert len(completed) == 1
    assert completed[0][1].description == "Walk"


def test_filter_by_pet_returns_only_that_pet():
    """Only named pet's tasks should return."""
    owner = Owner("A")
    dog = Pet("Max", "Dog")
    cat = Pet("Luna", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "08:00"))
    cat.add_task(Task("Feed", "12:00"))

    s = Scheduler()
    max_tasks = s.filter_by_pet(owner, "Max")
    assert len(max_tasks) == 1
    assert max_tasks[0][0] == "Max"


def test_recurrence_creates_next_occurrence():
    """Daily task should spawn a new pending task when completed."""
    task = Task("Feed", "08:00", frequency="daily")
    next_task = task.mark_complete()
    assert task.status == "completed"
    assert next_task is not None
    assert next_task.description == "Feed"
    assert next_task.time == "08:00"
    assert next_task.status == "pending"
    assert next_task.frequency == "daily"


def test_once_task_does_not_recur():
    """A one-time task returns None on completion."""
    task = Task("Vet Visit", "08:00", frequency="once")
    result = task.mark_complete()
    assert task.status == "completed"
    assert result is None


def test_conflict_detection_flags_duplicate_times():
    """Two tasks at the same time should produce a warning."""
    owner = Owner("A")
    dog = Pet("Max", "Dog")
    cat = Pet("Luna", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "09:00"))
    cat.add_task(Task("Feed", "09:00"))

    s = Scheduler()
    warnings = s.detect_conflicts(owner)
    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_conflict_detection_clean_when_no_overlap():
    """No warnings when all times are unique."""
    owner = Owner("A")
    pet = Pet("Max", "Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00"))
    pet.add_task(Task("Feed", "12:00"))

    s = Scheduler()
    assert s.detect_conflicts(owner) == []


def test_empty_owner_returns_empty_results():
    """Edge case: owner with no pets should return empty lists."""
    owner = Owner("A")
    s = Scheduler()
    assert s.get_tasks(owner) == []
    assert s.sort_by_time(owner) == []
    assert s.detect_conflicts(owner) == []