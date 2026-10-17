from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    description: str
    time: str
    frequency: str = "daily"
    status: str = "pending"
    duration_minutes: int = 30
    priority: str = "Medium"

    def mark_complete(self):
        """Marks the task as completed."""
        self.status = "completed"

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
        """Retrieves all tasks across all pets, returning tuples of (pet_name, task)."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet.name, task))
        return all_tasks

class Scheduler:
    def get_tasks(self, owner: Owner) -> List[tuple]:
        """Retrieves all tasks from the owner's pets."""
        return owner.get_all_tasks()

    def organize_tasks(self, owner: Owner) -> List[tuple]:
        """Organizes and returns all tasks."""
        return self.get_tasks(owner)
