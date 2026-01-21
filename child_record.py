# Модуль с классами для хранения данных о детях и результатах диспансеризации


from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List


class GroupType(Enum):
    JUNIOR = "младшая"
    MIDDLE = "средняя"
    SENIOR = "старшая"


class SpecialistType(Enum):
    NEUROLOGIST = "невропатолог"
    OTOLARYNGOLOGIST = "отоларинголог"
    ORTHOPEDIST = "ортопед"
    OPHTHALMOLOGIST = "окулист"


@dataclass
class HealthConclusion:
    neurologist: bool  # True = здоров, False = нуждается в лечении
    otolaryngologist: bool
    orthopedist: bool
    ophthalmologist: bool

    def count_healthy(self) -> int:
        return sum([self.neurologist, self.otolaryngologist,
                    self.orthopedist, self.ophthalmologist])

    def needs_treatment(self) -> bool:
        return not all([self.neurologist, self.otolaryngologist,
                        self.orthopedist, self.ophthalmologist])

    @classmethod
    def from_strings(cls, neuro: str, oto: str, ortho: str, ophth: str) -> 'HealthConclusion':
        return cls(
            neurologist=neuro.strip().lower() == "здоров",
            otolaryngologist=oto.strip().lower() == "здоров",
            orthopedist=ortho.strip().lower() == "здоров",
            ophthalmologist=ophth.strip().lower() == "здоров"
        )


@dataclass
class ChildRecord:
    last_name: str
    first_name: str
    birth_date: date
    group: GroupType
    health: HealthConclusion

    def __str__(self) -> str:
        return (f"{self.last_name} {self.first_name}, "
                f"родился: {self.birth_date.strftime('%d.%m.%Y')}, "
                f"группа: {self.group.value}, "
                f"здоровых заключений: {self.health.count_healthy()}/4")