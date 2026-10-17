from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Owner:
    name: str
    preferences: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    details: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Task:
    description: str
    time: datetime
    frequency: str
    status: str
    duration_minutes: int
    priority: str

    def mark_complete(self) -> None:
        pass


@dataclass
class Scheduler:
    def get_tasks(self, owner: Owner) -> list[Task]:
        pass

    def organize_tasks(self, owner: Owner) -> list[Task]:
        pass

    def generate_schedule(
        self, owner: Owner, available_minutes: int
    ) -> list[Task]:
        pass