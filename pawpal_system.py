from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time: str
    frequency: str = "daily"
    status: str = "pending"
    duration_minutes: int = 30
    priority: str = "Medium"

    def mark_complete(self):
        """Marks task complete; returns a new Task for next occurrence if recurring, else None."""
        self.status = "completed"
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
            )
        if self.frequency == "weekly":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
            )
        return None


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    details: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to the pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Returns all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    preferences: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[tuple]:
        """Retrieves all tasks across all pets as (pet_name, task) tuples."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet.name, task))
        return all_tasks


class Scheduler:
    """The brain — retrieves, sorts, filters, and validates tasks across all pets."""

    def get_tasks(self, owner: Owner) -> List[tuple]:
        """Retrieves all tasks from the owner's pets."""
        return owner.get_all_tasks()

    def sort_by_time(self, owner: Owner) -> List[tuple]:
        """Returns all tasks sorted chronologically by HH:MM time string."""
        return sorted(self.get_tasks(owner), key=lambda pt: pt[1].time)

    def filter_by_status(self, owner: Owner, status: str) -> List[tuple]:
        """Returns only tasks with the given completion status."""
        return [pt for pt in self.get_tasks(owner) if pt[1].status == status]

    def filter_by_pet(self, owner: Owner, pet_name: str) -> List[tuple]:
        """Returns only tasks belonging to the named pet."""
        return [pt for pt in self.get_tasks(owner) if pt[0] == pet_name]

    def detect_conflicts(self, owner: Owner) -> List[str]:
        """Returns warning strings for any two tasks scheduled at the exact same time."""
        seen = {}
        warnings = []
        for pet_name, task in self.sort_by_time(owner):
            if task.time in seen:
                other_pet, other_task = seen[task.time]
                warnings.append(
                    f"⚠️ Conflict at {task.time}: "
                    f"{other_pet}'s '{other_task.description}' and "
                    f"{pet_name}'s '{task.description}'"
                )
            else:
                seen[task.time] = (pet_name, task)
        return warnings

    # Keep the old name so main.py doesn't break — but now it actually SORTS:
    def organize_tasks(self, owner: Owner) -> List[tuple]:
        """Organizes all tasks chronologically (alias for sort_by_time)."""
        return self.sort_by_time(owner)